# soco-trainer-plugin
The soco-trainer-plugin is to help to add new training method to soco-core-trainer.   

## Install
```commandline
pip install soco_trainer_plugin
```
## Define configs
There are two files to modify in the configs folder: config.yaml and hparams.json
The config.yaml is for Environment variables and hparams is for model training. Each ML model, there are different parameters  

```json
{
  "configs": [
    {
      "task_type": "multi_label_text",
      "params": {
        "lr": {
          "name": "learning rate",
          "default": 1e-4,
          "type": "float"
        },
        "n_training_steps": {
          "name": "n_training_steps",
          "default": 10000,
          "type": "int"
        },
        "batch_size": {
          "name": "batch_size",
          "default": 8,
          "type": "int"
        },
        "tokenizer": {
          "name": "bert-base-cased",
          "default": "bert-base-cased",
          "type": "str"
        },
         "max_token_len": {
          "name": "max_token_len",
          "default": 30,
          "type": "int"
        },
        "number_of_classes": {
          "name": "number_of_classes",
          "default": 6,
          "type": "int"
        },
        "train_data": {
          "name": "toxic",
          "default": "toxic",
          "type": "str"
        },
        "seed": {
          "name": "random seed",
          "default": 777,
          "type": "int"
        },
        "workers": {
          "name": "parallel worker threads",
          "default": 4,
          "type": "int"
        },
        "max_epochs": {
          "name": "max_epochs",
          "default": 5,
          "type": "int"
        },
        "fast_dev_run": {
          "name": "fast dev run",
          "default": false,
          "type": "bool"
        }
      }
    }
  ]
}

```


## Implement Trainer
In order to make the trainer plugin, you need to use the TrainerPlugin as Inheritance in your trainer code. It is required to input three parameters: redis_url, mongo_url, and mlflow_tracking_url
First, you need to implement the start_train function 1) call self.setup(params, task_id, op_id) to convert from your json params to object params, and it will return the tracker and data_processor. The tracker is used for logging in the training studio and data_processor is used to get data from the training data db.  

Here is the example code: 

```python 
from soco_trainer_plugin.trainer_plugin import TrainerPlugin

class Trainer(TrainerPlugin):
    def __init__(self, redis_url, mongo_url, mlflow_tracking_url=None):
        super().__init__(redis_url, mongo_url, mlflow_tracking_url)

    def start_train(self, task_id: str, op_id: str, params: dict, task_type: str):
        params, data_processor, tracker = self.setup(params, task_id, op_id)        
        if task_type == "multi_label_text":
            data_module = CustomDataModule(hparams=params,data_processor=data_processor)
            qa_model = MultiLabelText(hparams=params, tracker=tracker)
            trainer = pl.Trainer.from_argparse_args(params)
            trainer.fit(qa_model, data_module)
```

Second, you need to implement your own DataModule using params and data_processor: 
the data_processor contains several functions:
- data_processor.get_train_examples(training_data_name): this will retrieve all training data
- data_processor.get_test_examples(test_data_name): this will retrieve all test data
- data_processor.get_sample(training_data_name): this will sample one from training data

Third, please add logger in your model file. You need to pass hparams and tracker. 
hparams can be used to specify training details such as batch_size, learning rate, etc. the tracker should be used for logging the training.

```python
class Model(pl.LightningModule):
    def __init__(self, hparams, tracker):
```
When starting the train, you need to put self.tracker.start_tracking(max_epochs) and self.logger.log_hyperparams to save hyperparameters in details. 
```python
def on_train_start(self):
    if self.tracker:
        self.tracker.start_tracking(self.param.max_epochs)
    self.logger.log_hyperparams(vars(self.param))
```
Each training step, you should put the self.log()
```python
    def training_step(self, batch, batch_idx):
    
        self.log("train_loss", loss, prog_bar=True, logger=True)
```
At the end of each training epoch, please update the tracker as the code below:
```python
def training_epoch_end(self, outputs):
    if self.tracker:
        self.tracker.update_done(self.current_epoch)
```
## Run Plugin Server
```python
from soco_trainer_plugin.plugin_server import PluginServer
from trainer.trainer import Trainer
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

trainer = Trainer(redis_url="redis://:Soco2020@redis-14541.c13.us-east-1-3.ec2.cloud.redislabs.com:14541/0",
                  mongo_url="mongodb://68.77.252.175:32000/trainer")

server = PluginServer(trainer,
                      host="0.0.0.0",
                      port=8006,
                      max_batch_size=500,
                      param="hparams.json",
                      debug=False,
                      redis_url="redis://:Soco2020@redis-14541.c13.us-east-1-3.ec2.cloud.redislabs.com:14541/0",
                      mongo_url="mongodb://68.77.252.175:32000/trainer")
server.run_server()
```
If you run the trainer plugin server, the following api endpoints will be active:
- GET /v1/trainer/ping: ping to check if the plugin is available. 
- GET /v1/trainer/params:  The trainer master server will know which params of this plugins are available. 
- POST /v1/trainer/start_train: This will make starting the training
- POST /v1/trainer/predict: This is for prediction for each model
- POST /v1/trainer/models: this will return all available models and paths
- GET /v1/k8s/console_logs: this will return the console logs while training 
  

## Run Plugin Worker
```python
from soco_trainer_plugin.plugin_worker import PluginWorker
worker = PluginWorker("redis://:Soco2020@redis-14541.c13.us-east-1-3.ec2.cloud.redislabs.com:14541/0")
worker.run_worker()
```
The worker will train the model based on start_train signal from plugin server. It is recommended to install in the GPU machine. 

# Test your plugin
```commandline
cd test
python server_test.py
```
