import pytest
import os
from container_hub import get_backend
from container_hub.carriers.docker.backend import DockerBackend
from container_hub.carriers.marathon.backend import MarathonBackend
from simple_settings import LazySettings


@pytest.fixture
def docker_simple_settings():
    # os.environ.update({"SIMPLE_SETTINGS": "tests.test_files.docker_settings"})
    yield LazySettings("tests.test_files.docker_settings")


@pytest.fixture
def marathon_simple_settings():
    yield LazySettings("tests.test_files.marathon_settings")


def test_loading_docker_backend(docker_simple_settings):
    backend = get_backend(docker_simple_settings)
    assert isinstance(backend, DockerBackend)


def test_loading_marathon_backend(marathon_simple_settings):
    backend = get_backend(marathon_simple_settings)
    assert isinstance(backend, MarathonBackend)
