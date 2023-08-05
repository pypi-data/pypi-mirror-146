import os, uuid, sys
from os.path import join, split, basename
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from azure.identity import ClientSecretCredential
#from dotenv import load_dotenv


class Azure_wrapper:

    def __init__(self):

        # usar os.getenv para os atributos
        #load_dotenv()

        # credenciais
        self.account_name = os.getenv("ACCOUNT_NAME")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.tenant_id = os.getenv("TENANT_ID")

        self.file_system_name = os.getenv("FILE_SYSTEM_NAME")
        self.__root = os.getenv("DIR_NAME")

        self.initialize_storage_account_ad()

    def get_root(self):
        return self.__root

    def initialize_storage_account_ad(self):

        try:
            global service_client

            credential = ClientSecretCredential(self.tenant_id, self.client_id, self.client_secret)

            service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
                "https", self.account_name), credential=credential)

        except Exception as e:
            print(e)

    def exist_path(self, path):
        try:

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            paths = file_system_client.get_paths(path=path)

            if path in paths:
                return True

            return False

        except Exception as e:
            print(e)

    def upload(self, local_path: str, azure_path: str) -> None:

        # baseado no upload_bulk

        try:

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            dir_path = self.__root
            path_azure_base = split(azure_path)[0]

            if path_azure_base != "":
                dir_path = join(self.__root, path_azure_base)

            directory_client = file_system_client.get_directory_client(dir_path)

            file_client = directory_client.get_file_client(basename(azure_path))

            local_file = open(local_path, 'r')

            file_contents = local_file.read()

            file_client.upload_data(file_contents, overwrite=True)

        except Exception as e:
            print(e)

    def download(self, azure_file_path: str, local_save_path: str) -> None:
        try:

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            dir_path = self.__root
            path_base_azure = split(azure_file_path)[0]

            if path_base_azure != "":
                dir_path = join(self.__root, path_base_azure)

            directory_client = file_system_client.get_directory_client(dir_path)

            local_file = open(local_save_path, 'wb')

            file_client = directory_client.get_file_client(basename(azure_file_path))

            download = file_client.download_file()

            downloaded_bytes = download.readall()

            local_file.write(downloaded_bytes)

            local_file.close()

        except Exception as e:
            print(e)

    def mkdir(self, new_dir_name):
        try:

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            file_system_client.create_directory(join(self.__root, new_dir_name))

        except Exception as e:
            print(e)

    def glob(self, dir_name):
        try:

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            paths = file_system_client.get_paths(path=dir_name)

            for path in paths:
                print(path.name + '\n')

        except Exception as e:
            print(e)

    def delete_directory(self, dir_name):
        try:
            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)
            directory_client = file_system_client.get_directory_client(dir_name)

            directory_client.delete_directory()
        except Exception as e:
            print(e)

    def rename_directory(self, azure_dir_name: str, azure_new_dir_name: str) -> None:
        try:

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)
            directory_client = file_system_client.get_directory_client(join(self.__root, azure_dir_name))

            directory_client.rename_directory(new_name=directory_client.file_system_name + '/' + join(self.__root, azure_new_dir_name))

        except Exception as e:
            print(e)

    def move_directory(self, azure_path, azure_move_path):
        # Por agora, funciona só quando os diretorios estao no mesmo nivel
        new_dir_path = join(azure_move_path, azure_path)
        # print("move_directory: ", new_dir_path)
        self.rename_directory(azure_path, new_dir_path)
