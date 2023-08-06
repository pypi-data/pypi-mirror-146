"""Tests covering the S3ConfigSecret class."""
from kubernetes.client import (
    ApiException,
    CoreV1Api,
)
import pytest

from netapp_dataops.k8s.data_movers.s3 import S3ConfigSecret


@pytest.fixture(scope='function')
def secret_manager(k8s_client):
    """Fixture to provide a secret name and cleanup a secret.

    :param k8s_client: Fixture providing the K8s client.
    :return: The name of the secret to create.
    """
    secret_name = "test-s3-secret-create-1"
    yield secret_name

    api_instance = CoreV1Api(api_client=k8s_client)
    try:
        api_instance.delete_namespaced_secret(name=secret_name, namespace='default')
    except ApiException:
        pass


def test_s3_config_secret_create_default_namespace(k8s_client, secret_manager):
    """Test the creation of an S3 secret with the default namespace parameter.

    Requirements:
        * A working Kubernetes cluster

    Test Steps:
        * Create a secret using the S3ConfigSecret class.
        * Verify the secret is created in K8s.
        * Verify the required secret keys exist.
        * Verify the secret is created in the expected namespace.

    :param k8s_client: Fixture providing the K8s client.
    :param secret_manager: Fixture providing the secret name and managing secret cleanup.
    """

    access_key_data = "dummy_access"
    secret_key_data = "dummy_secret"
    namespace = "default"

    api_instance = CoreV1Api(api_client=k8s_client)

    existing_secrets = api_instance.list_namespaced_secret(namespace=namespace)
    existing_names = [v1secret.metadata.name for v1secret in existing_secrets.items]
    if secret_manager in existing_names:
        pytest.skip(
            "The secret named {} already exists. Delete the secret or use a different namespace.".format(secret_manager)
        )

    secret_config = S3ConfigSecret(
        name=secret_manager,
        access_key=access_key_data,
        secret_key=secret_key_data
    )

    secret_config.create()
    # TODO: If create is modified to return something we should validate what it returns

    # If this call doesn't fail then we verify the secret was created.
    secret_data = api_instance.read_namespaced_secret(name=secret_manager, namespace=namespace)

    # Verify the relevant keys are present
    assert secret_data.data['access_key']
    assert secret_data.data['secret_key']

    # Verify the default labels are present
    assert secret_data.metadata.labels['created-by'] == 'ntap-dsutil'


def test_s3_config_secret_delete(k8s_client, k8s_s3_secret, k8s_namespace, namespace_name):
    """Test the S3ConfigSecret delete method.

    Requirements:
        * A working Kubernetes cluster

    Dependencies:
        * A Secret has been created on the K8s cluster

    Test Steps:
        * Use the S3ConfigSecret delete method to delete the secret
        * Verify the secret no longer exists on the cluster

    :param k8s_client: Fixture providing the K8s client.
    :param k8s_s3_secret: Fixture providing the created S3 secret.
    :param k8s_namespace: Fixture providing the namespace to use for class instantiation.
    :param namespace_name: Fixture providing the name of the namespace used.
    """
    secret_config = S3ConfigSecret(
        name=k8s_s3_secret,
        access_key="abc",  # The values don't need to match for delete to succeed.
        secret_key="123",
        namespace=k8s_namespace
    )
    secret_config.delete()

    api_instance = CoreV1Api(api_client=k8s_client)

    with pytest.raises(ApiException) as read_error:
        api_instance.read_namespaced_secret(name=k8s_s3_secret, namespace=namespace_name)
    assert "Reason: Not Found" in str(read_error.value)
