# database.py tests

import database
import unittest


class MockCursorMethods:

    lastrowid = 1

    def execute(self, _query, _values):
        return self.lastrowid

    def fetchone(self):
        return {'id': 1}


class MockCursor:

    def __enter__(self):
        return MockCursorMethods()

    def __exit__(self, _unused1, _unused2, _unused3):
        pass


class MockConnection:

    def __init__(self, **kwargs):
        pass

    def cursor(self):
        return MockCursor()

    def __enter__(self):
        pass

    def close(self):
        pass

    def commit(self):
        pass


class TestDatabase(unittest.TestCase):

    package = {'Package': 'fake', 'Version': '1.0.0',
               'Date/Publication': '2019-11-09 16:20:02 UTC',
               'Title': 'Fake Title', 'Description': 'Fake',
               'Author': 'john,jane,fake]', 'Maintainer': 'John'}

    def setUp(self):
        database.pymysql.connect = MockConnection

    def test_get_package_info(self):
        record = database.Database().get_package_info(self.package)
        self.assertEqual(record['id'], 1)

    def test_save_package(self):
        status = database.Database().save_package(self.package)
        self.assertTrue(status)

    def test_add_authors(self):
        total_success = database.Database().add_authors(
            self.package['Author'], -1)
        self.assertEqual(total_success, 2)  # outof 3

    def test_add_maintainers(self):
        total_success = database.Database().add_maintainers(
            self.package['Maintainer'], -1)
        self.assertEqual(total_success, 1)


if __name__ == '__main__':
    unittest.main()
