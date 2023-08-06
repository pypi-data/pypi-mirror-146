from abc import ABC, abstractmethod
from soco_trainer_plugin.progress_tracker import ProgressTracker
from pytorch_lightning.loggers import MLFlowLogger
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
import random
import numpy as np
import os
import torch
from soco_trainer_plugin.core.database.data_processor_base import ProcessorBase


class TrainerPlugin(ABC):
    def __init__(self, redis_url, mongo_url, tracking_url):
        self.CREATE = "init"
        self.UPDATE = "update"
        self.DELETE = "delete"
        self.redis_url = redis_url
        self.mongo_url = mongo_url
        self.tracker = None
        self.tracking_url = tracking_url

    @abstractmethod
    def start_train(self, task_id, op_id, params, task_type):
        pass

    @abstractmethod
    def predict(self, task_id: str, model_id: str, params: dict, input: str):
        pass

    def get_model_path(self, task_id, model_id="best.ckpt"):
        root_dir = os.path.dirname(os.path.realpath(__file__)).replace('soco_trainer_plugin', '')
        return f"{root_dir}/trained_models/{task_id}/{model_id}"

    def setup(self, params, task_id, op_id, root_dir=None):
        if not root_dir:
            root_dir = os.path.dirname(os.path.realpath(__file__)).replace('soco_trainer_plugin', '')
        if "seed" in params:
            self.seed_everything(params["seed"])
        params = Dict2Obj(params)
        tracker = ProgressTracker(task_id, op_id, self.CREATE, redis_url=self.redis_url,
                                       mongo_url=self.mongo_url) if task_id else None
        self.tracking_url = "file:./mlruns" if not self.tracking_url else self.tracking_url
        task_id = "test" if not task_id else task_id
        mlf_logger = MLFlowLogger(experiment_name=task_id, tracking_uri=self.tracking_url)
        checkpoint_callback = ModelCheckpoint(
            dirpath=os.path.join(root_dir,"trained_models",task_id),
            filename="best",
            save_top_k=1,
            verbose=True,
            monitor="val_loss",
            mode="min"
        )
        early_stopping_callback = EarlyStopping(monitor='val_loss', patience=2)
        params.callbacks = [checkpoint_callback,early_stopping_callback]

        params.logger = mlf_logger
        data_processor = ProcessorBase(mongo_url=self.mongo_url)
        return params, data_processor, tracker

    @staticmethod
    def seed_everything(seed):
        '''
        Seeds all the libraries for reproducability
        :param int seed: Seed
        :return:
        '''
        random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False


class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """

    # ----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])
