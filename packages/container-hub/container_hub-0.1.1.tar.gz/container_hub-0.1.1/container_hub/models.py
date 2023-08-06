from pathlib import Path
from dataclasses import dataclass, field, fields, _MISSING_TYPE
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime
from .exceptions import InvalidConfiguration


class LogLevel(Enum):
    info = "INFO"
    debug = "DEBUG"
    warning = "WARNING"


@dataclass
class MountPoint:
    local_path: str
    mount_path: str
    read_only: bool = True


def create_klass(cls, settings, prefix: str):
    """
    Create cls from config parameters in settings.

    The fields of cls should be present in upper-case prefixed with the prefix and "_".
    """
    kwargs = {}

    for field in fields(cls):
        attr_name = f"{prefix}_{field.name.upper()}"

        if (
            isinstance(field.default, _MISSING_TYPE)
            and isinstance(field.default_factory, _MISSING_TYPE)
            and not hasattr(settings, attr_name)
        ):
            raise InvalidConfiguration(f"{attr_name} is a mandatory setting")

        if hasattr(settings, attr_name):
            kwargs[field.name] = getattr(settings, attr_name)

    # [['api', 'CLUSTER', 'v3'], ]
    if "constraints" in kwargs and isinstance(kwargs["constraints"], list):
        kwargs["constraints"] = [MarathonConstraint(*x) for x in kwargs["constraints"]]

    return cls(**kwargs)


@dataclass
class DockerBackendConfig:
    client_url: str  # URL to docker or marathon
    network_name: str  # network to use
    debug: bool = False

    @classmethod
    def from_settings(cls, settings, prefix="CONTAINER_HUB") -> "DockerBackendConfig":
        """
        Populate DockerBackendConfig from simple-settings, Django settings
        or similair object.
        """
        return create_klass(cls, settings, prefix)


@dataclass
class MarathonConstraint:
    param: str
    operator: str
    value: str


@dataclass
class MarathonBackendConfig(DockerBackendConfig):
    constraints: List[MarathonConstraint] = field(default_factory=list)

    @classmethod
    def from_settings(cls, settings, prefix="CONTAINER_HUB") -> "MarathonBackendConfig":
        """
        Populate MarathonBackendConfig from simple-settings, Django settings
        or similair object.
        """
        return create_klass(cls, settings, prefix)


@dataclass
class EnvVar:
    name: str
    value: str


@dataclass
class Label:
    name: str
    value: str


@dataclass
class ContainerConfig:
    image_name: str  # threedicore image name
    base_result_path: Path  # path for results
    sim_uid: str
    sim_ref_datetime: datetime
    end_time: int
    duration: int
    pause_timeout: int
    start_mode: str
    model_config: str
    max_cpu: int  # max CPU's to use
    session_memory: int  # max memory
    envs: List[EnvVar]
    labels: List[Label]
    max_rate: float = 0.0
    clean_up_files: bool = False
    gridadmin_download_url: Optional[str] = None
    tables_download_url: Optional[str] = None
    mount_points: List[MountPoint] = field(default_factory=list)
    redis_host: str = "redis"  # Local redis host
    container_log_level: LogLevel = LogLevel.info
