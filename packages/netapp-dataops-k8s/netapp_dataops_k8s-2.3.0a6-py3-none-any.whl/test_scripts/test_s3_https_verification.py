"""Tests for S3 data mover HTTPS verification."""
import os
import time

import pytest

from netapp_dataops.k8s.data_movers.s3 import S3DataMover


def test_s3_data_mover_with_https_verification_of_user_ca(s3_resource,
                                                          pvc_with_data,
                                                          k8s_s3_secret,
                                                          k8s_namespace,
                                                          config_data):
    """Test S3 data mover with HTTPS verification with user provided CA.

    Requirements:

    Dependencies:
        * Use of an S3 service utilizing HTTPS with a TLS certificate that is not trusted
            without a user provided CA (self-signed or private CA).

    :param s3_resource:
    :param config_data:
    """
    s3_protocol = config_data['s3_protocol']
    if s3_protocol != "https":
        pytest.skip(f"This test requires use of HTTPS but {s3_protocol} was specified in the configuration.")

    s3_verify_certs = config_data['s3_verify_certs']
    if not s3_verify_certs:
        pytest.skip(
            f"This test requires that certificate verification is enabled but verification is set to {s3_verify_certs}"
        )

    # TODO: Move configmap setup to fixture?
    ca_files = config_data['trusted_ca_certs']
    if not ca_files:
        pytest.skip("Trusted CA certificates are required but were not provided in the test configuration.")

    ca_map_names = []
    for cert in ca_files:
        filename = os.path.basename(cert)
        print(f"Creating config map for CA certificate {cert} using name {filename}")
        cert_map = k8s.CAConfigMap(name=filename, certificate_file=cert, namespace=k8s_namespace)
        cert_map_name = cert_map.create()
        ca_map_names.append(cert_map_name)

    data_mover = S3DataMover(
        credentials_secret=k8s_s3_secret,
        s3_host=config_data['s3_host'],
        s3_port=config_data['s3_port'],
        use_https=True,
        verify_certificates=True,
        ca_config_maps=ca_map_names,
        namespace=k8s_namespace
    )

    object_name = "one.txt"
    put_job = data_mover.put_object(bucket="gmarks2", pvc=pvc_with_data, object_=object_name)
    job_completed = False
    for x in range(15):
        is_running = bool(data_mover.get_job_status(job=put_job).active)
        if not is_running:
            job_completed = True
            break
        time.sleep(2)
    print(f"Job {put_job} completed? {job_completed}")