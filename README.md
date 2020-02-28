# Instructions

1. Please setup your `virtualenv` and run `pip install -r requirements.txt`
2. For tests, `python3 database_tests.py` and `python3 package_tests.py`
3. `python3 package.py` to start reading packages from [R-PACKAGES](https://cran.r-project.org/src/contrib/PACKAGES) and update database.
4. For cronjob setup at 12 PM, `python3 cronjob.py`

# Module Explanation

1. `package.py` - Read Package, Extract Package information from `.tar.gz` files.
2. `database.py` - Connect to Free MySQL, Save Package information provided by `package.py`
3. `package_tests.py` - Test `get_packages` public method
4. `database_tests.py` - Test `get_package_info`, `save_package`, `add_authors` and `add_maintainers` public methods
5. `_fake_test_package.tar.gz` - Test file for package unittest
6. `database_tables.sql` - Schema file to setup database locally or any other server. Currently, it is hosted to free mysql https://remotemysql.com/
7. `requirements.txt` - Provided list of python libraries used
8. `cronjob.py` - Python cronjob setup at 12 PM everyday
