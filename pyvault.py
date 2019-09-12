import requests
import hvac
import re


## Inputs
# vault url
# token
# path to copy
# path to paste

class HashicorpVault:
    client = None
    token = None

    def __init__(self, vault_ip, username, password):
        self.connect_to_vault(vault_ip, username, password)

    def get_secrets_data_from_path(self, path):
        response = self.client.read(path=path)
        data = response["data"]
        return data

    def get_secret_from_path(self, path, secret_key="secret"):
        data = self.get_secrets_data_from_path(path)
        secret = data[secret_key]
        return secret

    def copy_secrets(self, source_path, destination_path):
        source_paths = self.get_source_paths(source_path)

        for path in source_paths:
            data = self.get_secrets_data_from_path(path)
            dest_path = self.get_destination_path(source_path, destination_path, path)
            self.client.write(dest_path, None, **data)

    def is_directory(self, path: str):
        """
        Determines if a path is a directory or not by checking for a / at the end of a path

        :type path: str
        """
        if path.endswith('/'):
            return True
        else:
            return False

    def join_path(self, path: str, path_tail: str):
        path_with_slashes = path + '/' + path_tail
        cleaned_path = path_with_slashes.replace('//', '/')
        return cleaned_path

    def get_source_paths(self, path: str, source_paths=[]):
        response = self.client.list(path=path)
        paths_array = response['data']['keys']

        for path_tail in paths_array:
            full_path = self.join_path(path, path_tail)

            if self.is_directory(path=full_path):
                # crawl path again
                self.get_source_paths(full_path, source_paths)
            else:
                # this is the end, add it to the copy list
                source_paths.append(full_path)
        return source_paths

    def get_destination_paths(self, source_path_root, destination_path_root, paths):
        destination_paths = []
        for path in paths:
            dest_path = path.replace(source_path_root, destination_path_root)
            destination_paths.append(dest_path)

        return destination_paths

    def get_destination_path(self, source_path_root, destination_path_root, path):
        dest_path = path.replace(source_path_root, destination_path_root)
        return dest_path

    def connect_to_vault(self, vault_ip, username, password):

        authentication_url = "http://{}:8200/v1/auth/okta/login/{}".format(vault_ip, username)
        body = {
            'password': password}
        token_response = requests.post(url=authentication_url, json=body)
        data = token_response.json()
        token = data["auth"]["client_token"]
        self.token = token
        client = hvac.Client(
            url='http://{}:8200'.format(vault_ip),
            token=token
        )
        client.is_authenticated()
        self.client = client

    def read(self, path):
        return self.client.read(path)

    def write(self, path: str, data: dict):
        self.client.write(path, None, **data)

    @staticmethod
    def get_matching_paths(paths: list, pattern: str) -> list:
        matching_paths = []
        for path in paths:
            if re.match(pattern, path):
                matching_paths.append(path)
        return matching_paths

    def get_name_from_path(self, path):
        name = path.split('/').pop()
        return name

    def get_name_and_secret_list_of_dict_from_paths(self, paths: list) -> list:
        # for each node under the /oidc get the name and secret value
        name_and_secret_list_of_dict = []
        for path in paths:
            name = self.get_name_from_path(path)
            secret = self.get_secret_from_path(path)
            dictionary = {
                "name": name,
                "secret": secret
            }
            name_and_secret_list_of_dict.append(dictionary)
        return name_and_secret_list_of_dict

    def get_oidc_tokens_from_vault(self, environment):
        secret_paths = self.get_secret_paths_for_environment(environment, "/unique")
        tokens_dict = self.get_oidc_tokens_for_environment(environment, secret_paths)
        return tokens_dict

    def get_oidc_tokens_for_environment(self, environment: str, secret_paths: list) -> dict:
        oidc_pattern = 'secret\/environments\/' + environment + '\/unique\/.*\/oidc\/'
        oidc = self.get_matching_paths(secret_paths, oidc_pattern)
        oidc_list_to_update = self.get_name_and_secret_list_of_dict_from_paths(oidc)
        return oidc_list_to_update

    def get_secret_paths_for_environment(self, environment: str, child_path="/unique") -> list:
        services_root_path = "secret/environments/" + environment + child_path
        services = self.get_source_paths(services_root_path)
        return services

    def get_mongo_password_for_environment(self, environment, username):
        path = "secret/environments/" + environment + "/shared/mongoDB/" + username
        secret = self.get_secret_from_path(path)
        return secret
