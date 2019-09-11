import os

import requests
import hvac


## Inputs
# vault url
# token
# path to copy
# path to paste

def copy_secrets(client, source_path, destination_path):
    source_paths = get_source_paths(client, source_path)

    for path in source_paths:
        response = client.read(path=path)
        data = response["data"]
        dest_path = get_destination_path(source_path, destination_path, path)
        client.write(dest_path, None, **data)


# Will have to do some sort of recurse probably, and maybe build an object as I go
def is_directory(path: str):
    """
    Determines if a path is a directory or not by checking for a / at the end of a path

    :type path: str
    """
    if path.endswith('/'):
        return True
    else:
        return False


def join_path(path: str, path_tail: str):
    path_with_slashes = path + '/' + path_tail
    cleaned_path = path_with_slashes.replace('//', '/')
    return cleaned_path


def get_source_paths(client, path: str, source_paths=[]):
    response = client.list(path=path)
    paths_array = response['data']['keys']

    for path_tail in paths_array:
        full_path = join_path(path, path_tail)

        if is_directory(path=full_path):
            # crawl path again
            get_source_paths(client, full_path, source_paths)
        else:
            # this is the end, add it to the copy list
            source_paths.append(full_path)
    return source_paths


import unittest


def get_destination_paths(source_path_root, destination_path_root, paths):
    destination_paths = []
    for path in paths:
        dest_path = path.replace(source_path_root, destination_path_root)
        destination_paths.append(dest_path)

    return destination_paths


def get_destination_path(source_path_root, destination_path_root, path):
    dest_path = path.replace(source_path_root, destination_path_root)
    return dest_path


def connect_to_vault(vault_ip, username, password):
    global client
    authentication_url = "http://{}:8200/v1/auth/okta/login/{}".format(vault_ip, username)
    body = {
        'password': password}
    token_response = requests.post(url=authentication_url, json=body)
    data = token_response.json()
    token = data["auth"]["client_token"]
    print('##vso[task.setvariable variable=output_vault_token;]%s' % token)
    client = hvac.Client(
        url='http://{}:8200'.format(vault_ip),
        token=token
    )
    client.is_authenticated()
    return client


class TestVaultCopier(unittest.TestCase):

    def setUp(self) -> None:
        url = "http://10.101.0.251:8200/v1/auth/okta/login/rb.boley"

        body = {
            'password': '.dotHack1234'}

        token_response = requests.post(url=url, json=body)
        data = token_response.json()
        token = data["auth"]["client_token"]

        print('##vso[task.setvariable variable=output_vault_token;]%s' % token)

        self.client = hvac.Client(
            url='http://10.101.0.251:8200',
            token=token
        )
        self.client.is_authenticated()

    def test_correct_amount_of_slashes_when_there_are_child_folders(self):
        expected = ['secret/environments/qa/other/azure_backup_storage_key',
                    'secret/environments/qa/other/azure_data_storage_key', 'secret/environments/qa/shared/cert/private',
                    'secret/environments/qa/shared/cert/public', 'secret/environments/qa/shared/ftp',
                    'secret/environments/qa/shared/mongoDB/admin', 'secret/environments/qa/shared/mongoDB/metricbeat',
                    'secret/environments/qa/shared/mongoDB/readOnly', 'secret/environments/qa/shared/redis',
                    'secret/environments/qa/shared/sql/saNodeQA', 'secret/environments/qa/shared/ssh/private',
                    'secret/environments/qa/shared/ssh/public', 'secret/environments/qa/unique/bs/adminPass',
                    'secret/environments/qa/unique/bs/ftp/james.roller',
                    'secret/environments/qa/unique/bs/mongoDB/readOnly',
                    'secret/environments/qa/unique/bs/mongoDB/readWrite',
                    'secret/environments/qa/unique/bs/oidc/svc-bs', 'secret/environments/qa/unique/bs/oidc/uiBS',
                    'secret/environments/qa/unique/bs/sql/saBsDev',
                    'secret/environments/qa/unique/ioea/mongoDB/readOnly',
                    'secret/environments/qa/unique/ioea/mongoDB/readWrite',
                    'secret/environments/qa/unique/larch/oidc/uiLarch',
                    'secret/environments/qa/unique/lateFees/ftp/james.roller',
                    'secret/environments/qa/unique/lateFees/mongoDB/readOnly',
                    'secret/environments/qa/unique/lateFees/mongoDB/readWrite',
                    'secret/environments/qa/unique/lateFees/oidc/svc-late-fees',
                    'secret/environments/qa/unique/lateFees/oidc/uiLateFees',
                    'secret/environments/qa/unique/lateFees/sql/saLateFeesDev',
                    'secret/environments/qa/unique/loans/mongoDB/readOnly',
                    'secret/environments/qa/unique/loans/mongoDB/readWrite',
                    'secret/environments/qa/unique/loans/oidc/svc-loans',
                    'secret/environments/qa/unique/loans/sql/saLoansDev',
                    'secret/environments/qa/unique/nmls/mongoDB/readOnly',
                    'secret/environments/qa/unique/nmls/mongoDB/readWrite',
                    'secret/environments/qa/unique/noi/mongoDB/readOnly',
                    'secret/environments/qa/unique/noi/mongoDB/readWrite',
                    'secret/environments/qa/unique/noi/oidc/svc-noi', 'secret/environments/qa/unique/noi/sql/saNOIdev',
                    'secret/environments/qa/unique/oidc/cookie/1', 'secret/environments/qa/unique/oidc/cookie/2',
                    'secret/environments/qa/unique/oidc/mongoDB/readOnly',
                    'secret/environments/qa/unique/oidc/mongoDB/readWrite',
                    'secret/environments/qa/unique/oidc/oidc/uiOIDC',
                    'secret/environments/qa/unique/oidc/sql/saOIDCDev',
                    'secret/environments/qa/unique/pdfrender/mongoDB/readOnly',
                    'secret/environments/qa/unique/pdfrender/mongoDB/readWrite',
                    'secret/environments/qa/unique/tincompliance/mongoDB/readOnly',
                    'secret/environments/qa/unique/tincompliance/mongoDB/readWrite',
                    'secret/environments/qa/unique/tinvalid/mongoDB/readOnly',
                    'secret/environments/qa/unique/tinvalid/mongoDB/readWrite',
                    'secret/environments/qa/unique/transactions/mongoDB/readOnly',
                    'secret/environments/qa/unique/transactions/mongoDB/readWrite',
                    'secret/environments/qa/unique/transactions/oidc/svc-transactions',
                    'secret/environments/qa/unique/transactions/sql/saTransactionsDev',
                    'secret/environments/qa/unique/vendor-hometrust/mongoDB/readOnly',
                    'secret/environments/qa/unique/vendor-hometrust/mongoDB/readWrite']

        copy_root_path = 'secret/environments/qa'
        actual = get_source_paths(self.client, copy_root_path, [])
        self.assertEqual(str(expected), str(actual))

    def test_correct_amount_of_slashes_when_there_are_child_folders(self):
        expected = ['secret/environments/dev-boley/diag_storage_account',
                    'secret/environments/dev-boley/diag_storage_account2']
        copy_root_path = 'secret/environments/dev-boley'
        actual = get_source_paths(self.client, copy_root_path, [])
        self.assertEqual(str(expected), str(actual))

    def test_can_copy_a_secret_secret(self):
        path = 'secret/environments/qa/unique/transactions/oidc/svc-transactions'
        dest_path = 'secret/environments/qa2/unique/transactions/oidc/svc-transactions'
        response = self.client.read(path=path)
        data = response["data"]

        self.client.write(dest_path, None, **data)

    def test_can_update_paths_to_be_new_place(self):
        source_paths = ['secret/environments/qa/other/azure_backup_storage_key',
                        'secret/environments/qa/other/azure_data_storage_key',
                        'secret/environments/qa/shared/cert/private']
        expected = ['secret/environments/qa2/other/azure_backup_storage_key',
                    'secret/environments/qa2/other/azure_data_storage_key',
                    'secret/environments/qa2/shared/cert/private']
        source_path_root = 'secret/environments/qa'
        destination_path_root = 'secret/environments/qa2'

        actual = get_destination_paths(source_path_root, destination_path_root, source_paths)

        self.assertEqual(str(expected), str(actual))

    def test_can_update_one_path_to_a_new_place(self):
        source_paths = 'secret/environments/qa/other/azure_backup_storage_key'
        expected = 'secret/environments/qa2/other/azure_backup_storage_key'
        source_path_root = 'secret/environments/qa'
        destination_path_root = 'secret/environments/qa2'

        actual = get_destination_path(source_path_root, destination_path_root, source_paths)

        self.assertEqual(str(expected), str(actual))


if __name__ == '__main__':
    # unittest.main()

    vault_ip = '10.101.0.251'
    username = 'rb.boley'
    password = ''

    client = connect_to_vault(vault_ip, username, password)
    copy_secrets(client, 'secret/environments/qa', 'secret/environments/qa2')
