from dataclasses import dataclass
from enum import Enum
import abc
from typing import List, Union


class StrEnum(str, Enum):
    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class PredefinedAIArgType(StrEnum):
    String = 'String'
    Integer = 'Integer'
    Float = 'Float'
    Categorical = 'Categorical'
    MultipleOf2 = 'MultipleOf2'
    Bool = 'Bool'


class PredefinedAIArg:
    @abc.abstractmethod
    def get_key(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_value(self):
        raise NotImplementedError


class ArgGroup(StrEnum):
    Arg = 'Arg'
    AlgorithmHyperparameter = 'AlgorithmHyperparameter'
    ModelHyperparameter = 'ModelHyperparameter'
    SamplingHyperparameter = 'SamplingHyperparameter'
    MetricHyperparameter = 'MetricHyperparameter'


@dataclass
class PredefinedAIStringArg(PredefinedAIArg):
    key: str
    display_name: str
    description: str
    value: str
    group: ArgGroup = ArgGroup.Arg
    type: PredefinedAIArgType = PredefinedAIArgType.String

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAIBoolArg(PredefinedAIArg):
    key: str
    display_name: str
    description: str
    value: bool
    group: ArgGroup = ArgGroup.Arg
    type: PredefinedAIArgType = PredefinedAIArgType.Bool

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAIIntegerArg(PredefinedAIArg):
    key: str
    display_name: str
    description: str
    min: int
    max: int
    value: int
    unit_step: int
    group: ArgGroup = ArgGroup.Arg
    type: PredefinedAIArgType = PredefinedAIArgType.Integer

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAIFloatArg(PredefinedAIArg):
    key: str
    display_name: str
    description: str
    min: float
    max: float
    value: float
    unit_step: float
    group: ArgGroup = ArgGroup.Arg
    type: PredefinedAIArgType = PredefinedAIArgType.Float

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAIMultipleOf2Arg(PredefinedAIArg):
    key: str
    display_name: str
    description: str
    min: int
    max: int
    value: int
    unit_step: int
    group: ArgGroup = ArgGroup.Arg
    type: PredefinedAIArgType = PredefinedAIArgType.MultipleOf2

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


@dataclass
class PredefinedAICategoricalValue:
    key: str
    display_name: str
    description: str


@dataclass
class PredefinedAICategoricalArg(PredefinedAIArg):
    key: str
    display_name: str
    description: str
    values: List[PredefinedAICategoricalValue]
    value: PredefinedAICategoricalValue
    group: ArgGroup = ArgGroup.Arg
    type: PredefinedAIArgType = PredefinedAIArgType.Categorical

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value.key


@dataclass
class ModelConfig:
    key: str
    display_name: str
    description: str
    hyperparameters: List[
        Union[PredefinedAIBoolArg, PredefinedAIIntegerArg, PredefinedAIFloatArg, PredefinedAIMultipleOf2Arg, PredefinedAICategoricalArg]]

    def __post_init__(self):
        self.hyperparameter_dict = {}
        for hp in self.__getattribute__('hyperparameters'):
            self.hyperparameter_dict[hp.get_key()] = hp.get_value()


@dataclass
class StageConfig:
    args: List[
        Union[
            PredefinedAIStringArg, PredefinedAIBoolArg, PredefinedAIIntegerArg, PredefinedAIFloatArg, PredefinedAIMultipleOf2Arg, PredefinedAICategoricalArg]]


@dataclass
class PredefinedAIModelConfig:
    display_name: str
    key: str
    description: str
    model_configs: List[ModelConfig]
    train: StageConfig
    retrain: StageConfig
    inference: StageConfig
    serving: StageConfig

    def __post_init__(self):
        self.hyperparameter_dict = {}
        for model_config in self.model_configs:
            self.hyperparameter_dict[model_config.key] = {}
            for hp in model_config.hyperparameters:
                self.hyperparameter_dict[model_config.key][hp.get_key()] = hp.get_value()

        self.args_dict = {}
        for stage in ['train', 'retrain', 'inference', 'serving']:
            self.args_dict[stage] = {}
            for arg in self.__getattribute__(stage).__getattribute__('args'):
                self.args_dict[stage][arg.get_key()] = arg.get_value()

    def _get_model_hyperparameters_dict(self, model_name) -> dict:
        if model_name in self.hyperparameter_dict.keys():
            return self.hyperparameter_dict[model_name]
        raise ValueError(f'model "{model_name}" dose not exist in model_configs')

    def _get_args_dict(self, stage) -> dict:
        if stage in ['train', 'retrain', 'inference', 'serving']:
            return self.args_dict[stage]
        raise ValueError(f'stage "{stage}" dose not exist')
