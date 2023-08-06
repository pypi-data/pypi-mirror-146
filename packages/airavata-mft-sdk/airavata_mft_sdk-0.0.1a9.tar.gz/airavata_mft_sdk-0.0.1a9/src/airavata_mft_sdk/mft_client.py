import grpc
import airavata_mft_sdk.MFTTransferApi_pb2_grpc as transfer_grpc
import airavata_mft_sdk.resource.ResourceService_pb2_grpc as resource_grpc
import airavata_mft_sdk.azure.AzureStorageService_pb2_grpc as azure_grpc
import airavata_mft_sdk.box.BoxStorageService_pb2_grpc as box_grpc
import airavata_mft_sdk.dropbox.DropboxStorageService_pb2_grpc as dropbox_grpc
import airavata_mft_sdk.ftp.FTPStorageService_pb2_grpc as ftp_grpc
import airavata_mft_sdk.gcs.GCSStorageService_pb2_grpc as gcs_grpc
import airavata_mft_sdk.local.LocalStorageService_pb2_grpc as local_grpc
import airavata_mft_sdk.s3.S3StorageService_pb2_grpc as s3_grpc
import airavata_mft_sdk.scp.SCPStorageService_pb2_grpc as scp_grpc
import airavata_mft_sdk.storagesecretmap.StorageSecretMap_pb2_grpc as storage_secret_map_grpc

import airavata_mft_sdk.azure.AzureSecretService_pb2_grpc as azure_secret_grpc
import airavata_mft_sdk.box.BoxSecretService_pb2_grpc as box_secret_grpc
import airavata_mft_sdk.dropbox.DropboxSecretService_pb2_grpc as dropbox_secret_grpc
import airavata_mft_sdk.ftp.FTPSecretService_pb2_grpc as ftp_secret_grpc
import airavata_mft_sdk.gcs.GCSSecretService_pb2_grpc as gcs_secret_grpc
import airavata_mft_sdk.s3.S3SecretService_pb2_grpc as s3_secret_grpc
import airavata_mft_sdk.scp.SCPSecretService_pb2_grpc as scp_secret_grpc


class MFTClient:

    def __init__(self, transfer_api_host = "localhost",
                 transfer_api_port = 7004,
                 transfer_api_secured = False,
                 resource_service_host = "localhost",
                 resource_service_port = 7002,
                 resource_service_secured = False,
                 secret_service_host = "localhost",
                 secret_service_port = 7003,
                 secret_service_secured = False,):

        if (not transfer_api_secured):
            self.transfer_api_channel = grpc.insecure_channel('{}:{}'.format(transfer_api_host, transfer_api_port))
        # TODO implement secure channel
        self.transfer_api = transfer_grpc.MFTTransferServiceStub(self.transfer_api_channel)

        if (not resource_service_secured):
            self.resource_channel = grpc.insecure_channel('{}:{}'.format(resource_service_host, resource_service_port))
        # TODO implement secure channel
        self.resource_api = resource_grpc.GenericResourceServiceStub(self.resource_channel)
        self.azure_storage_api = azure_grpc.AzureStorageServiceStub(self.resource_channel)
        self.box_storage_api = box_grpc.BoxStorageServiceStub(self.resource_channel)
        self.dropbox_storage_api = dropbox_grpc.DropboxStorageServiceStub(self.resource_channel)
        self.ftp_storage_api = ftp_grpc.FTPStorageServiceStub(self.resource_channel)
        self.gcs_storage_api = gcs_grpc.GCSStorageServiceStub(self.resource_channel)
        self.local_storage_api = local_grpc.LocalStorageServiceStub(self.resource_channel)
        self.s3_storage_api = s3_grpc.S3StorageServiceStub(self.resource_channel)
        self.scp_storage_api = scp_grpc.SCPStorageServiceStub(self.resource_channel)
        self.storage_secret_map_api = storage_secret_map_grpc.StorageSecretServiceStub(self.resource_channel)


        if (not secret_service_secured):
            self.secret_channel = grpc.insecure_channel('{}:{}'.format(secret_service_host, secret_service_port))
        # TODO implement secure channel
        self.azure_secret_api = azure_secret_grpc.AzureSecretServiceStub(self.secret_channel)
        self.box_secret_api = box_secret_grpc.BoxSecretServiceStub(self.secret_channel)
        self.dropbox_secret_api = dropbox_secret_grpc.DropboxSecretServiceStub(self.secret_channel)
        self.ftp_secret_api = ftp_secret_grpc.FTPSecretServiceStub(self.secret_channel)
        self.gcs_secret_api = gcs_secret_grpc.GCSSecretServiceStub(self.secret_channel)
        self.s3_secret_api = s3_secret_grpc.S3SecretServiceStub(self.secret_channel)
        self.scp_secret_api = scp_secret_grpc.SCPSecretServiceStub(self.secret_channel)



