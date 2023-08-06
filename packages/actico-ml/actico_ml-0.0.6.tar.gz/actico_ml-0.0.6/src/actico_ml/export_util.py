import logging
import shutil
import sys
import tempfile
from json import JSONEncoder
from os.path import exists
from zipfile import ZipFile

import h2o
import requests
from scipy.stats import qmc

logging.basicConfig(level='INFO',
                    format='%(asctime)s %(levelname)s %(message)s')


def release_model(api_key, model_hub_url, model_name,
    training_frame_name, module_id, project_id, version=None, sc=None,
    pipeline_model=None, df=None):
  params = {"trainingFrameName": training_frame_name, "moduleId": module_id,
            "projectId": project_id, "version": version}
  files = None

  if pipeline_model is not None:
    with tempfile.NamedTemporaryFile() as tmp:
      pipeline_model.write().overwrite().save(tmp.name)
      sc.parallelize([df.schema.json()]).coalesce(1).saveAsTextFile(
          tmp.name + "/schema-before")
      sc.parallelize([pipeline_model.transform(df).schema.json()]).coalesce(
          1).saveAsTextFile(tmp.name + "/schema-after")
      shutil.make_archive(tmp.name, 'zip', tmp.name)
    files = {'pipeline': open(tmp.name + ".zip", 'rb')}
  is_successful = False

  try:
    r = requests.post(
        model_hub_url + "/machine-learning/v1/models/" +
        model_name + "/release",
        headers={'Authorization': 'ApiKey ' + api_key}, params=params,
        files=files)
    r.raise_for_status()
    if r.status_code == 200:
      is_successful = True
  except requests.exceptions.HTTPError as e:
    logging.warning(e.response.text)
  return is_successful


def export_model_to_file_path(
    model_name,
    path,
    h2o_url="http://localhost:54321",
    max_calculation_size=300000):
  __check_for_valid_path(model_name, path)

  h2o_estimator_to_export, \
  h2o_model_meta_informations, \
  h2o_training_frame_name, \
  h2o_training_frame_all_rows, \
  h2o_training_frame_meta_informations = \
    __initialize_h2o_and_load_frames_and_models(
        model_name, h2o_url)

  excluded_columns = __get_ignored_and_response_columns(h2o_estimator_to_export)

  sobol_indices = __create_sobol_indices(max_calculation_size,
                                         h2o_training_frame_meta_informations)
  if sobol_indices:
    destination_frame_name = __create_destination_frame_name(
        h2o_training_frame_name)
    h2o_training_frame_sampled = __create_new_sampled_frame(
        destination_frame_name,
        h2o_training_frame_name,
        sobol_indices)
    actico_input_frame_for_json = __create_actico_frame(
        h2o_training_frame_sampled, excluded_columns)
  else:
    actico_input_frame_for_json = __create_actico_frame(
        h2o_training_frame_all_rows, excluded_columns)

  actico_input_model_for_json = __create_actico_model(
      h2o_estimator_to_export,
      h2o_model_meta_informations)
  path_to_mojo_zip = __write_mojo_to_disk(h2o_estimator_to_export,
                                          path)
  __enrich_mojo_with_json_frame_and_model(actico_input_frame_for_json,
                                          actico_input_model_for_json,
                                          path_to_mojo_zip)
  logging.info("The export of the mojo is completed.")


def __check_for_valid_path(model_name, path):
  logging.info("Check if given path is valid.")
  if (exists(path + model_name + '.zip')):
    logging.critical(
        "A file at the given path already exists. "
        "Please remove or rename the existing file.")
    sys.exit(1)
  else:
    logging.info("The given path is valid. Continue export.")


def __get_ignored_and_response_columns(h2o_estimator):
  logging.info("Retrieve ignored columns and response column. ")
  try:
    excluded_columns = []
    if (h2o_estimator.actual_params.get('ignored_columns') != None):
      excluded_columns.extend(
          h2o_estimator.actual_params.get('ignored_columns'))
    if (h2o_estimator.actual_params.get('response_column') != None):
      excluded_columns.append(
          h2o_estimator.actual_params.get('response_column'))
  except Exception:
    logging.error("An error occured while retrieving", exc_info=True)
    sys.exit(1)
  return excluded_columns


def __initialize_h2o_and_load_frames_and_models(model_name, h2o_url):
  logging.info("Connect to H2O server on URL: %s " % h2o_url)
  h2o.connect(url=h2o_url)

  logging.info("Retrieve necessary information from H2O.")
  try:
    h2o_model_to_export = h2o.get_model(model_name)
    h2o_training_frame_name = h2o_model_to_export.parms.get(
        "training_frame").get(
        "actual_value").get(
        "name")
    h2o_training_frame_meta_informations = h2o.get_frame(
        h2o_training_frame_name,
        light=True)
    h2o_model_meta_informations = h2o.api("GET /3/Models/%s" % model_name)
    h2o_training_frame_all_rows = h2o.api("GET /3/Frames/%s?row_count=%s" % (
      h2o_training_frame_name, h2o_training_frame_meta_informations.nrows))
  except Exception:
    logging.error("An error occured while retrieving data from H2O: ",
                  exc_info=True)
    sys.exit(1)

  return h2o_model_to_export, \
         h2o_model_meta_informations, \
         h2o_training_frame_name, \
         h2o_training_frame_all_rows, \
         h2o_training_frame_meta_informations


def __create_actico_frame(h2o_frame, excluded_columns):
  logging.info("Create ACTICO Frame based on H2O training frame.")
  columns = []
  try:
    for idx, val in enumerate(h2o_frame.get('frames')[0].get('columns')):
      if (val.get('label') in excluded_columns):
        continue
      columns.append(
          Column(val.get('label'),
                 val.get('type'),
                 val.get('zero_count'),
                 val.get('missing_count'),
                 val.get('mins')[0],
                 val.get('maxs')[0],
                 val.get('mean'),
                 val.get('sigma'),
                 val.get('domain_cardinality'),
                 val.get('domain'),
                 val.get('data')))

    actico_frame = Frame(h2o_frame.get('frames')[0].get('frame_id').get('name'),
                         h2o_frame.get('frames')[0].get('rows'),
                         h2o_frame.get('frames')[0].get('num_columns'),
                         h2o_frame.get('frames')[0].get('byte_size'),
                         True,
                         columns)
  except Exception:
    logging.error(
        "An error occured while creating the actico frame. "
        "This frame is mandatory for the export thus the export has to get "
        "aborted.", exc_info=True)
    sys.exit(1)
  return actico_frame


def __create_actico_model(h2o_model, h2o_additional_model_information):
  logging.info("Create training parameters dictionary.")
  actual_params = dict()
  for key in h2o_model.actual_params:
    actual_params[key] = str(h2o_model.actual_params[key])

  logging.info("Create default parameters dictionary.")
  default_params = dict()
  for key in h2o_model.default_params:
    default_params[key] = str(h2o_model.actual_params[key])

  try:
    training_link = h2o_additional_model_information.get('models')[
      0].get('output').get(
        'training_metrics')._metric_json
  except Exception:
    logging.warning(
        "The field _metric_json does not exist. "
        "Falling back to alternative. The integrity of the exported model "
        "could be unstable.")
    training_link = h2o_additional_model_information.get('models')[
      0].get('output').get(
        'training_metrics')

  try:
    train_model_category = h2o_additional_model_information.get('models')[
      0].get('output').get('model_category')
    train_max_criteria = training_link. \
      get('max_criteria_and_metric_scores') if \
      train_model_category == 'Binomial' else None
    train_model_id = h2o_model.actual_params.get('model_id')
    train_frame = h2o_model.actual_params.get('training_frame')
    train_description = training_link.get('description')
    train_scoring_time = training_link.get('scoring_time')

    training_score = Score(
        __get_score_type(train_model_category),
        train_max_criteria,
        train_model_id,
        train_frame,
        train_description,
        train_model_category,
        train_scoring_time)
  except Exception:
    logging.warning(
        "An error occured while retrieving the training score. "
        "Falling back to alternative. The integrity of the exported model "
        "could be unstable.", exc_info=True)
    training_score = None

  logging.info("Check if validation frame exists")
  if (h2o_additional_model_information.get('models')[0].get('output').get(
      'validation_metrics') != None):
    logging.info("Validation frame exists. Retrieve validation Score.")
    try:
      validation_link = h2o_additional_model_information.get('models')[
        0].get('output').get(
          'validation_metrics')._metric_json
    except Exception:
      logging.warning(
          "The field _metric_json does not exist. "
          "Falling back to alternative. The integrity of the exported model "
          "could be unstable.", exc_info=True)
      validation_link = h2o_additional_model_information.get('models')[
        0].get('output').get(
          'validation_metrics')

    try:
      vali_model_category = h2o_additional_model_information.get('models')[
        0].get('output').get(
          'model_category')
      vali_max_criteria = validation_link.get(
          'max_criteria_and_metric_scores') if \
        vali_model_category == 'Binomial' else None
      vali_model_id = h2o_model.actual_params.get('model_id')
      vali_frame = h2o_model.actual_params.get('validation_frame')
      vali_description = h2o_model.actual_params.get(
          'validation_frame'), validation_link.get('description')
      vali_scoring_time = validation_link.get('scoring_time')

      validation_score = Score(
          __get_score_type(vali_model_category),
          vali_max_criteria,
          vali_model_id,
          vali_frame,
          vali_description,
          vali_model_category,
          vali_scoring_time)
    except Exception:
      logging.warning(msg=
                      "An error occured while retrieving the validation score. "
                      "Falling back to alternative. "
                      "The integrity of the exported model "
                      "could be unstable.", exc_info=True)
      validation_score = None
  else:
    logging.info("Validation frame does not exist.")
    validation_score = None

  logging.info("Create ACTICO Model")
  try:
    model_id = h2o_model.actual_params.get('model_id')
    model_algo_full_name = h2o_additional_model_information.get('models')[
      0].get('algo_full_name')
    model_train_frame = h2o_model.actual_params.get('training_frame')
    model_vali_frame = h2o_model.actual_params.get('validation_frame')
    model_end_time = h2o_model.end_time
    model_category = h2o_additional_model_information.get('models')[0].get(
        'output').get('model_category')
    model_names = h2o_additional_model_information.get('models')[0].get(
        'output').get('names')
    model_column_types = h2o_additional_model_information.get('models')[0].get(
        'output').get('column_types')
    model_response_column = h2o_model.actual_params.get('response_column')
    model_variable_importance = h2o_additional_model_information.get('models')[
      0].get('output').get('variable_importances')

    actico_model = Model(model_id,
                         __convert_algorithm_name(h2o_model.algo),
                         model_algo_full_name,
                         model_train_frame,
                         model_vali_frame,
                         model_end_time,
                         model_category,
                         model_names,
                         model_column_types,
                         model_response_column,
                         model_variable_importance,
                         actual_params,
                         default_params,
                         training_score,
                         validation_score
                         )
  except Exception:
    logging.error(
        "An error occured while creating the ACTICO model. "
        "Falling back to alternative. The integrity of the exported model "
        "could be unstable.", exc_info=True)
    actico_model = None
  return actico_model


def __convert_algorithm_name(h2o_algorithm_name):
  logging.info("Convert algorithm name.")
  if (h2o_algorithm_name == 'drf'): return 'RF'
  if (h2o_algorithm_name == 'gbm'): return 'GB'
  if (h2o_algorithm_name == 'glm'): return 'GLM'
  if (h2o_algorithm_name == 'kmeans'): return 'KMEANS'
  if (h2o_algorithm_name == 'xgboost'): return 'XGB'
  if (h2o_algorithm_name == 'isolationforest'): return 'IF'
  logging.warning("The type of algorithm %s is unknown." % h2o_algorithm_name)
  return ("UNKOWN")


def __get_score_type(model_category):
  logging.info("Get score type based on model category")
  if (model_category == 'Binomial'): return 'ScoreBinomial'
  if (model_category == 'Multinomial'): return 'ScoreMultinomial'
  if (model_category == 'Regression'): return 'ScoreRegression'
  if (model_category == 'Clustering'): return 'ScoreClustering'
  logging.warning(
      "The given model category is not officially supported. "
      "Falling back to alternative. The integrity of the exported model "
      "could be unstable.")
  return 'Score unknown'


def __enrich_mojo_with_json_frame_and_model(actico_frame, actico_model,
    path_to_mojo):
  logging.info("Enrich mojo with ACTICO metadata")
  try:
    json_frame = __transform_actico_object_to_json(actico_frame)
    json_model = __transform_actico_object_to_json(actico_model)
    with ZipFile(path_to_mojo, 'a') as zip_archive:
      zip_archive.writestr('actico\\frame.json', json_frame)
      zip_archive.writestr('actico\\model.json', json_model)
    zip_archive.close()
  except Exception:
    logging.error(
        "An error occured while enriching the mojo with ACTICO metadata. "
        "The created Mojo will not contain ACTICO metadata thus will not be "
        "compatible with ACTICO Environments.", exc_info=True)
    sys.exit(1)


def __write_mojo_to_disk(h2o_model, path):
  logging.info("Write the h2o mojo to disk.")
  try:
    mojo_path = h2o_model.save_mojo(path=path)
  except Exception:
    logging.error('An error occured while writing the mojo to disk.',
                  exc_info=True)
    sys.exit(1)
  return mojo_path


def __transform_actico_object_to_json(actico_object):
  return Encoder().encode(actico_object)


def __create_sobol_indices(max_calculation_size, h2o_frame):
  logging.info("Check if Sobol sequencing is needed.")
  number_of_columns = h2o_frame.ncols
  number_of_rows = h2o_frame.nrows
  number_of_rows_for_sobol = __find_next_higher_power_of_two(
      round(max_calculation_size / number_of_columns))

  if number_of_rows_for_sobol > number_of_rows:
    logging.info(
        "Based on the given max calculation size Sobol sequencing is not "
        "needed. Instead, the complete frame will be saved to the mojo.")
    return []

  logging.info("Sobol sequencing is needed, "
               "because the max calculation size is not high enough to  "
               "include the complete frame.")
  sampler = qmc.Sobol(d=1, scramble=False, seed=42)
  sample = sampler.random(n=number_of_rows_for_sobol)

  return [round(x[0] * number_of_rows) for x in sample]


def __create_destination_frame_name(frame_name):
  import uuid
  uuid = uuid.uuid1()
  return str(uuid) + '-' + frame_name


def __create_new_sampled_frame(destination_frame_name,
    existing_frame_name,
    row_indices):
  logging.info("Create a new frame based on the Sobol sequence.")
  row_indices.sort()
  h2o.rapids(
      "(assign {destination_frame_subset_name}"
      "(rows {existing_frame_name} {row_indices}))".format(
          destination_frame_subset_name=destination_frame_name,
          existing_frame_name=existing_frame_name, row_indices=row_indices))

  return h2o.api("GET /3/Frames/%s?row_count=%s" % (destination_frame_name,
                                                    h2o.get_frame(
                                                        destination_frame_name,
                                                        light=True).nrows))


def __find_next_higher_power_of_two(n):
  k = 1
  while k < n:
    k = k << 1
  return k


class Frame:
  def __init__(
      self,
      name,
      numberOfRows,  # NOSONAR
      numberOfColumns,  # NOSONAR
      sizeInBytes,  # NOSONAR
      parsed,
      columns):
    self.name = name
    self.numberOfRows = numberOfRows  # NOSONAR
    self.numberOfColumns = numberOfColumns  # NOSONAR
    self.sizeInBytes = sizeInBytes  # NOSONAR
    self.parsed = parsed
    self.columns = columns


class Column:
  def __init__(
      self,
      name,
      dataType,  # NOSONAR
      numberOfZeros,  # NOSONAR
      numberOfMissingValues,  # NOSONAR
      minimumValue,  # NOSONAR
      maximumValue,  # NOSONAR
      meanValue,  # NOSONAR
      sigmaValue,  # NOSONAR
      cardinality,
      domains,
      data):
    self.name = name
    self.dataType = dataType.upper()  # NOSONAR
    self.numberOfZeros = numberOfZeros  # NOSONAR
    self.numberOfMissingValues = numberOfMissingValues  # NOSONAR
    self.minimumValue = minimumValue  # NOSONAR
    self.maximumValue = maximumValue  # NOSONAR
    self.meanValue = meanValue  # NOSONAR
    self.sigmaValue = sigmaValue  # NOSONAR
    self.cardinality = cardinality
    if (domains != None):
      self.domains = domains
    self.data = data


class Model:
  def __init__(
      self,  # NOSONAR
      name,  # NOSONAR
      algorithm,  # NOSONAR
      algorithmFullName,  # NOSONAR
      trainingFrameName,  # NOSONAR
      validationFrameName,  # NOSONAR
      endTime,  # NOSONAR
      modelCategory,  # NOSONAR
      columnNames,  # NOSONAR
      columnTypes,  # NOSONAR
      responseColumn,  # NOSONAR
      columnImportance,  # NOSONAR
      trainingParameters,  # NOSONAR
      defaultTrainingParameters,  # NOSONAR
      trainingScore,  # NOSONAR
      validationScore):  # NOSONAR
    self.name = name
    self.algorithm = algorithm.upper()
    self.algorithmFullName = algorithmFullName  # NOSONAR
    self.trainingFrameName = trainingFrameName  # NOSONAR
    self.validationFrameName = validationFrameName  # NOSONAR
    self.endTime = endTime  # NOSONAR
    self.modelCategory = modelCategory.upper()  # NOSONAR
    self.columnNames = columnNames  # NOSONAR
    self.columnTypes = [columnType.upper() for columnType in  # NOSONAR
                        columnTypes]
    self.responseColumn = responseColumn  # NOSONAR
    self.columnImportance = self.__two_dim_transformer(  # NOSONAR
        columnImportance)  # NOSONAR
    self.trainingParameters = trainingParameters  # NOSONAR
    self.defaultTrainingParameters = defaultTrainingParameters  # NOSONAR
    self.trainingScore = trainingScore  # NOSONAR
    if (validationScore != None):
      self.validationScore = validationScore  # NOSONAR

  def __two_dim_transformer(self, two_dim_table):
    column_importance = dict()
    columns = []
    for index in range(4):
      column = dict()
      column["name"] = two_dim_table.col_header[index]
      column["type"] = two_dim_table.col_types[index]
      column["data"] = []
      for cell_value in two_dim_table.cell_values:
        column["data"].append(cell_value[index])
      columns.append(column)
    column_importance["columns"] = columns
    return column_importance


class Score:
  def __init__(
      self,
      type,
      maxCriteriaAndMetricsScores,  # NOSONAR
      modelName,  # NOSONAR
      frameName,  # NOSONAR
      description,
      modelCategory,  # NOSONAR
      scoringTime):  # NOSONAR
    self.type = type
    if (maxCriteriaAndMetricsScores != None):
      self.maxCriteriaAndMetricsScores = self.__two_dim_transformer(  # NOSONAR
          maxCriteriaAndMetricsScores)
    self.modelName = modelName  # NOSONAR
    self.frameName = frameName  # NOSONAR
    if (description != None):
      self.description = description
    self.modelCategory = modelCategory  # NOSONAR
    self.scoringTime = scoringTime  # NOSONAR

  def __two_dim_transformer(self, two_dim_table):
    maxCriteriaAndMetricsScores = dict()  # NOSONAR
    columns = []
    for index in range(4):
      column = dict()
      column["name"] = two_dim_table.col_header[index]
      column["type"] = two_dim_table.col_types[index]
      column["data"] = []
      for cell_value in two_dim_table.cell_values:
        column["data"].append(cell_value[index])
      columns.append(column)
    maxCriteriaAndMetricsScores["columns"] = columns
    return maxCriteriaAndMetricsScores


class Encoder(JSONEncoder):
  def default(self, o):
    return o.__dict__
