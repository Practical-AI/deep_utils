from logging import Logger
from typing import Union, Dict
from deep_utils.utils.logging_utils.logging_utils import log_print, value_error_log
import minio


class MinIOUtils:
    @staticmethod
    def get_client(endpoint, access_key, secret_key):
        client = minio.Minio(endpoint, access_key, secret_key)
        return client

    @staticmethod
    def get(client, bucket_name, object_name, logger: Union[None, Logger] = None):
        """
        Get object from client. This function is created for compatibility otherwise no extra functionality provided compared to the main module.
        :param client:
        :param bucket_name:
        :param object_name:
        :param logger:
        :return:
        """
        obj = client.get_object(bucket_name, object_name)
        log_print(
            logger=logger,
            message=f"Successfully got object: {object_name} from bucket: {bucket_name}",
        )
        return obj

    @staticmethod
    def fget(
            client, bucket_name, object_name, file_path, logger: Union[None, Logger]
    ):
        """
        Get file object from client. This function is created for compatibility otherwise no extra functionality provided compared to the main module.
        :param client:
        :param bucket_name:
        :param object_name:
        :param file_path: Where to save the file
        :param logger:
        :return:
        """
        obj = client.fget_object(bucket_name, object_name, file_path)
        log_print(
            logger=logger,
            message=f"Successfully got object: {object_name} from bucket: {bucket_name}",
        )
        return obj

    @staticmethod
    def put(
            client,
            bucket_name,
            object_name,
            data,
            create=True,
            logger: Union[Logger, None] = None,
    ):
        """
        put an object inside a bucket
        :param client:
        :param bucket_name:
        :param object_name:
        :param data: data-file to be stored in
        :param create: create te bucket in case it doesn't exist, default is True.
        :param logger: a logger instance
        :return:
        """
        MinIOUtils.create_bucket(client, bucket_name, create, logger, )
        try:
            length = len(data.read())
            data.seek(0)
            part_size = 0
        except:
            length = -1
            part_size = data.__sizeof__()
        result = client.put_object(
            bucket_name,
            object_name,
            data,
            length=length,
            part_size=part_size
        )
        log_print(
            logger=logger,
            message=f"Successfully put object: {object_name} into bucket: {bucket_name}",
        )
        return result

    @staticmethod
    def fput(
            client,
            bucket_name,
            object_name,
            file_path,
            create=True,
            logger: Union[Logger, None] = None,
    ):
        """
        put a file inside a bucket
        :param client:
        :param bucket_name:
        :param object_name:
        :param file_path: file to be stored in the given bucket
        :param create: create te bucket in case it doesn't exist, default is True.
        :param logger: a logger instance
        :return:
        """
        MinIOUtils.create_bucket(client, bucket_name, create, logger)

        result = client.fput_object(
            bucket_name,
            object_name,
            file_path,
        )
        log_print(
            logger=logger,
            message=f"Successfully put file: {object_name} into bucket: {bucket_name}",
        )
        return result

    @staticmethod
    def create_bucket(client, bucket_name, create=True, logger=None) -> bool:
        """
        This method is used to find the requested bucket and create it in case the user desires it.
        :param bucket_name:
        :param create:
        :param logger:
        :param client:
        :return:
        """
        found = client.bucket_exists(bucket_name)
        if found:
            log_print(logger=logger,
                      message=f"Bucket {bucket_name} already exists")
        elif not found and create:
            client.make_bucket(bucket_name)
            log_print(logger=logger,
                      message=f"Successfully Created bucket: {bucket_name}")
        else:
            value_error_log(
                logger=logger, message='f"Error in creating minio bucket"')
        return found

    @staticmethod
    def check_connection(host, status_key="MINIO_STATUS") -> Dict[str, str]:
        import requests
        # check minio
        status = dict()
        try:
            status = requests.get(f"http://{host}/minio/health/live").ok
            status[status_key] = "Alive" if status else "Down"
        except:
            status[status_key] = "Down"
        return status

    @staticmethod
    def _get_policy(bucket_name):
        policy = {"Statement": [{"Action": ["s3:GetBucketLocation"],
                                 "Effect": "Allow", "Principal": {"AWS": ["*"]},
                                 "Resource": [f"arn:aws:s3:::{bucket_name}"]},
                                {"Action": ["s3:GetObject"],
                                 "Effect": "Allow", "Principal": {"AWS": ["*"]},
                                 "Resource": [f"arn:aws:s3:::{bucket_name}/*"]}], "Version": "2012-10-17"}
        return policy

    @staticmethod
    def make_bucket_public(client, bucket_name, logger=None, verbose=1):
        import json
        found = MinIOUtils.create_bucket(client, bucket_name)
        if not found:
            client.set_bucket_policy(bucket_name, json.dumps(MinIOUtils._get_policy(bucket_name)))
            log_print(logger=logger, message=f"Successfully Made bucket: {bucket_name} public", verbose=verbose)
