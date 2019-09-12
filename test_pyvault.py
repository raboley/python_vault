import unittest
import pyvault


class TestVaultCopier(unittest.TestCase):

    def setUp(self) -> None:
        vault_ip = ''
        username = ''
        password = ''

        self.hcvault = pyvault.HashicorpVault(vault_ip, username, password)

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
        actual = self.hcvault.get_source_paths(copy_root_path, [])
        self.assertEqual(str(expected), str(actual))

    def test_correct_amount_of_slashes_when_there_are_child_folders(self):
        expected = ['secret/environments/dev-boley/diag_storage_account2']
        copy_root_path = 'secret/environments/dev-boley'
        actual = self.hcvault.get_source_paths(copy_root_path, [])
        self.assertEqual(str(expected), str(actual))

    def test_can_copy_a_secret_secret(self):
        path = 'secret/environments/qa/unique/transactions/oidc/svc-transactions'
        dest_path = 'secret/environments/qa2/unique/transactions/oidc/svc-transactions'
        response = self.hcvault.read(path=path)
        data = response["data"]

        self.hcvault.write(dest_path, data)

    def test_can_update_paths_to_be_new_place(self):
        source_paths = ['secret/environments/qa/other/azure_backup_storage_key',
                        'secret/environments/qa/other/azure_data_storage_key',
                        'secret/environments/qa/shared/cert/private']
        expected = ['secret/environments/qa2/other/azure_backup_storage_key',
                    'secret/environments/qa2/other/azure_data_storage_key',
                    'secret/environments/qa2/shared/cert/private']
        source_path_root = 'secret/environments/qa'
        destination_path_root = 'secret/environments/qa2'

        actual = self.hcvault.get_destination_paths(source_path_root, destination_path_root, source_paths)

        self.assertEqual(str(expected), str(actual))

    def test_can_update_one_path_to_a_new_place(self):
        source_paths = 'secret/environments/qa/other/azure_backup_storage_key'
        expected = 'secret/environments/qa2/other/azure_backup_storage_key'
        source_path_root = 'secret/environments/qa'
        destination_path_root = 'secret/environments/qa2'

        actual = self.hcvault.get_destination_path(source_path_root, destination_path_root, source_paths)

        self.assertEqual(str(expected), str(actual))

    def test_can_update_one_path_to_a_new_place(self):
        # arrange
        source_path = 'secret/environments/dev/unique/autopost/oidc/svc-autopost'
        expected = 'secret/environments/qa/unique/autopost/oidc/svc-autopost'

        source_path_root = 'secret/environments/dev/unique/autopost'
        destination_path_root = 'secret/environments/qa/unique/autopost'

        # act
        self.hcvault.copy_secrets(source_path_root, destination_path_root)

        # assert
        # actual = self.hcvault.get_destination_path(source_path_root, destination_path_root, source_path)
        # self.assertEqual(str(expected), str(actual))

    def test_can_find_matching_patterns_in_array_of_paths(self):
        paths = ['secret/environments/dev/unique/autopost/mongoDB/readOnly',
                 'secret/environments/dev/unique/autopost/mongoDB/readWrite',
                 'secret/environments/dev/unique/autopost/oidc/svc-autopost',
                 'secret/environments/dev/unique/autopost/oidc/uiAutopost']
        expected_paths = ['secret/environments/dev/unique/autopost/oidc/svc-autopost',
                          'secret/environments/dev/unique/autopost/oidc/uiAutopost']

        pattern = 'secret\/environments\/dev\/unique\/.*\/oidc\/'

        actual_paths = self.hcvault.get_matching_paths(paths, pattern)

        self.assertListEqual(expected_paths, actual_paths)

    def test_can_find_matching_patterns_in_array_of_paths(self):
        paths = ['secret/environments/dev/unique/autopost/mongoDB/readOnly',
                 'secret/environments/dev/unique/autopost/mongoDB/readWrite',
                 'secret/environments/dev/unique/autopost/oidc/svc-autopost',
                 'secret/environments/dev/unique/autopost/oidc/uiAutopost']
        expected_paths = ['secret/environments/dev/unique/autopost/oidc/svc-autopost',
                          'secret/environments/dev/unique/autopost/oidc/uiAutopost']

        pattern = 'secret\/environments\/dev\/unique\/.*\/oidc\/'

        actual_paths = self.hcvault.get_matching_paths(paths, pattern)

        self.assertListEqual(expected_paths, actual_paths)

    def test_can_find_matching_patterns_in_array_of_paths_when_oidc_is_present_as_well(self):
        paths = ['secret/environments/dev/unique/oidc/mongoDB/readWrite',
                 'secret/environments/dev/unique/autopost/mongoDB/readOnly',
                 'secret/environments/dev/unique/autopost/mongoDB/readWrite',
                 'secret/environments/dev/unique/autopost/oidc/svc-autopost',
                 'secret/environments/dev/unique/autopost/oidc/uiAutopost']
        expected_paths = ['secret/environments/dev/unique/autopost/oidc/svc-autopost',
                          'secret/environments/dev/unique/autopost/oidc/uiAutopost']

        pattern = 'secret\/environments\/dev\/unique\/.*\/oidc\/'

        actual_paths = self.hcvault.get_matching_paths(paths, pattern)

        self.assertListEqual(expected_paths, actual_paths)

    def test_gets_vault_path_final_name(self):
        path = 'secret/environments/dev/unique/autopost/oidc/svc-autopost'
        expected_name = 'svc-autopost'

        actual_name = self.hcvault.get_name_from_path(path)

        self.assertEqual(expected_name, actual_name)

    def test_can_get_list_of_dict_from_multiple_paths(self):
        paths = ['secret/environments/dev/unique/oidc/mongoDB/readWrite',
                 'secret/environments/dev/unique/autopost/mongoDB/readOnly',
                 'secret/environments/dev/unique/autopost/mongoDB/readWrite',
                 'secret/environments/dev/unique/autopost/oidc/svc-autopost',
                 'secret/environments/dev/unique/autopost/oidc/uiAutopost']
        expected_paths = ['secret/environments/dev/unique/autopost/oidc/svc-autopost',
                          'secret/environments/dev/unique/autopost/oidc/uiAutopost']

        pattern = 'secret\/environments\/dev\/unique\/.*\/oidc\/'

        actual_paths = self.hcvault.get_matching_paths(paths, pattern)

        self.assertListEqual(expected_paths, actual_paths)


if __name__ == '__main__':
    unittest.main()
