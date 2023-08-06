"""This is for root pytest configuration."""
import pytest
import yaml

from test_scripts.fixtures.kubernetes import (
    k8s_cleanup_jobs,
    k8s_client,
    k8s_namespace,
    k8s_pvc,
    k8s_s3_secret,
    k8s_storage_class,
    mover_image,
    namespace_name,
    pvc_with_data,
)
from test_scripts.fixtures.s3 import (
    s3_bucket_empty,
    s3_bucket_full,
    s3_resource,
)


def pytest_addoption(parser):
    parser.addoption("--configuration", action="store", default=None,
                     help="Specify path to test configuration yaml file.")


@pytest.fixture(scope="session")
def config_data(pytestconfig) -> dict:
    file_name = pytestconfig.getoption("configuration")
    with open(file_name) as config_file:
        # The value of Loader may need to be adjusted
        # Change away from SafeLoader with caution.
        # See https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
        file_content = yaml.load(config_file, Loader=yaml.SafeLoader)
    yield file_content
