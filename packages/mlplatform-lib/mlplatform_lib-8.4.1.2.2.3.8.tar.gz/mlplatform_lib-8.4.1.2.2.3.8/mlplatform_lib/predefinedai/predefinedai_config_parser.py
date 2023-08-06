import yaml
from mlplatform_lib.predefinedai.predefinedai_data_config import PredefinedAIDataConfig, DataConfigurationType, ColumnDict, Column
from mlplatform_lib.predefinedai.predefinedai_model_config import PredefinedAIModelConfig
from mlplatform_lib.utils.dataclass_utils import from_dict
import argparse
import json
import sys
from typing import List, Union, Dict


class PredefinedAIConfigParser:
    def __init__(self, data_config_path=None, model_config_path=None):
        parser = argparse.ArgumentParser()
        parser.add_argument("--data_config", type=str, default=None)
        parser.add_argument("--model_config", type=str, default=None)
        _args = parser.parse_args()

        if _args.data_config is not None:
            data_config_dict = json.loads(_args.data_config)
        elif data_config_path is not None:
            with open(data_config_path) as data_config_file:
                data_config_dict = yaml.safe_load(data_config_file)
        else:
            raise ValueError('data_config must be in args')

        if _args.model_config is not None:
            model_config_dict = json.loads(_args.model_config)
        elif model_config_path is not None:
            with open(model_config_path) as model_config_file:
                model_config_dict = yaml.safe_load(model_config_file)
        else:
            raise ValueError('model_config must be in args')

        self.data_config_list: List[PredefinedAIDataConfig] = [from_dict(PredefinedAIDataConfig, data_config_d) for
                                                               data_config_d in data_config_dict]
        self.model_config: PredefinedAIModelConfig = from_dict(PredefinedAIModelConfig, model_config_dict)

    def get_data_config_from_data_key(self, data_key) -> PredefinedAIDataConfig:
        try:
            return list(filter(lambda x: x.__getattribute__('key') == data_key, self.data_config_list))[0]
        except IndexError:
            raise ValueError(f'data_key "{data_key}" do not exist in data_config')

    def get_data_config_dict_from_data_key(self, data_key) -> Dict[str, Union[ColumnDict, List[ColumnDict]]]:
        data_config_dict = {}
        data_config = self.get_data_config_from_data_key(data_key)
        for config in data_config.configurations:
            if config.type == DataConfigurationType.Column:
                if config.value is None:
                    data_config_dict[config.key] = None
                else:
                    data_config_dict[config.key] = {'name': config.value.name, 'type': config.value.type}
            elif config.type == DataConfigurationType.Columns:
                data_config_dict[config.key] = []
                if config.value is None:
                    continue
                for value in config.value:
                    data_config_dict[config.key].append({'name': value.name, 'type': value.type})
        return data_config_dict

    def get_all_data_config_dict(self) -> Dict[str, Dict[str, Union[ColumnDict, List[ColumnDict]]]]:
        all_data_config_dict = {}
        data_keys = [data_config.key for data_config in self.data_config_list]
        for data_key in data_keys:
            all_data_config_dict[data_key] = self.get_data_config_dict_from_data_key(data_key)
        return all_data_config_dict

    def get_model_name(self) -> str:
        return self.model_config.key

    def get_sub_model_name_list(self) -> List[str]:
        return [mc.key for mc in self.model_config.model_configs]

    def get_model_hyperparameters_dict(self, model_name: str) -> dict:
        return self.model_config._get_model_hyperparameters_dict(model_name)

    def get_train_args_dict(self) -> dict:
        return self._get_stage_args_dict('train')

    def get_retrain_ars_dict(self) -> dict:
        return self._get_stage_args_dict('retrain')

    def get_inference_args_dict(self) -> dict:
        return self._get_stage_args_dict('inference')

    def get_serving_args_dict(self) -> dict:
        return self._get_stage_args_dict('serving')

    def _get_stage_args_dict(self, stage) -> dict:
        return self.model_config._get_args_dict(stage)
