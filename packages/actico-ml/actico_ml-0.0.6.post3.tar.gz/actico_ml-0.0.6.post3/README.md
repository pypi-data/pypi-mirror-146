# ACTICO ML Python

With this package, a user is able to export a trained H2O ML model 
to ACTICO Model Hub or to a file path.


## Function
The package `export_util` contains the functions `release_model` and `export_model_to_file_path`

## Parameters of release_model
`api_key : string` Generated within Model Hub and required for a connection.

`model_hub_url : string` The link to model hub, e.g. "http://localhost:8080".

`model_name : string` The name of the model to be released, e.g. "credit-rf-model".

`training_frame_name : string` The name of the frame used for the training, e.g. "credit-train.hex".

`module_id : string` The module id is used to group related model projects into one logical unit, e.g. "actico.credit".

`project_id : string` The model project id is used to refer to the released machine learning model, e.g. "gm-model".

`version : string, optional` The version is used to distinguish between different iterations of a model. If left blank, an automatically generated version is used.

`sc : SparkContext, optional` The SparkContext to be used, if a Spark Pipeline should be added to the release.

`pipeline_model : PipelineModel, optional` The fitted Pipeline, that should be added to the release.

`df : DataFrame, optional` The Dataframe, that was used to fit the Pipeline.

## Parameters of export_model_to_file_path
`model_name : string` Name of the model on H2O to be exported, e.g. "credit-rf-model".

`path : string` Path to the folder to which the model is to be exported, e.g. "C:\\users\\user\\desktop\\".

`h2o_url : string, optional` URL to the H2O Server. If left empty, "http://localhost:54321" will be used.

`max_calculation_size : int, optional` This integer value sets the maximum complexity for the Shapley calculation. Higher values improve the accuracy, lower values improve the runtime. If left empty, 300000 is used.


## Example
```python
from actico_ml import export_util

export_util.release_model(api_key="API_KEY", 
                          model_hub_url="http://localhost:8080", 
                          model_name="credit-rf-model", 
                          training_frame_name="credit-train.hex", 
                          module_id="actico", 
                          project_id="credit-rf")

export_util.export_model_to_file_path(model_name="credit-rf-model", 
                                      path="C:\\users\\user\\desktop\\", 
                                      h2o_url="http://localhost:54323",
                                      max_calculation_size=1000)
```