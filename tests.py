# database.py tests

import package
import unittest
import database_tests

from unittest import mock


class TestPackage(unittest.TestCase):

    def setUp(self):
        package.database.pymysql.connect = database_tests.MockConnection

    @mock.patch('package.requests.get')
    def test_get_packages(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = 'Package: _test_package\nVersion: 1.0'
        zip_data = ''
        with open('_fake_test_package.tar.gz', 'rb') as file_obj:
            zip_data = file_obj.read()
        mock_get.return_value.content = zip_data

        packages = package.IndexPackages().get_packages(1)
        self.assertEqual(len(packages), 1)


if __name__ == '__main__':
    unittest.main()
