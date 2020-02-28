import database
import debian.deb822
import logging
import os
import requests
import shutil
import tarfile

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.DEBUG)

PACKAGE_URL = "https://cran.r-project.org/src/contrib/PACKAGES"
DESCRIPTION_TAR_URL = "https://cran.r-project.org/src/contrib/"


class IndexPackages:

    @staticmethod
    def _parse_package(package):
        pkg_generator = debian.deb822.Deb822.iter_paragraphs(package)
        return list(pkg_generator)[0]

    def _extract_package(self, package):
        filename = '%s_%s.tar.gz' % (package['Package'], package['Version'])
        response = requests.get(
            DESCRIPTION_TAR_URL + filename, allow_redirects=True)
        if response.status_code != 200:
            return False
        open(filename, 'wb').write(response.content)
        tar = tarfile.open(filename)
        tar.extractall()
        tar.close()
        os.remove(filename)
        return True

    def _save_package(self, package):
        if not self._extract_package(package):
            return False
        desc_filename = package['Package'] + '/DESCRIPTION'
        if not os.path.isfile(desc_filename):
            logging.error('No DESCRIPTION file found in package %s',
                          package['Package'])
            return False

        with open(desc_filename, 'r') as file_obj:
            package_detail = self._parse_package(
                file_obj.read().encode('utf-8'))
            package_id = database.Database().save_package(package_detail)
            if not package_id:
                package_id = database.Database().get_package_info(
                    package_detail).get('id', 0)

            # Still fail to generate information from Database
            if not package_id:
                return False

            # Save Maintainer and Authors
            if package_detail.get('Maintainer'):
                database.Database().add_maintainers(
                    package_detail['Maintainer'], package_id)
            if package_detail.get('Author'):
                database.Database().add_authors(
                    package_detail['Author'], package_id)

        shutil.rmtree(package['Package'])
        return True

    def get_packages(self, limit=50):
        response = requests.get(PACKAGE_URL)
        if response.status_code != 200:
            logging.error('Error: Fail to fetch packages')
            return

        packages = []
        for package in response.text.split('\n\n')[:limit]:
            package_dict = self._parse_package(package)
            if not package_dict:
                logging.error('Error: Fail to parse package!')
                continue
            package_name = '%s_%s' % (
                package_dict['Package'], package_dict['Version'])
            if not self._save_package(package_dict):
                logging.error('Error: Failed to save %s package!',
                              package_name)
                continue
            logging.info('Package %s is saved!', package_name)
            packages.append(package_name)
        return packages


if __name__ == '__main__':
    PACKAGE = IndexPackages()
    print(PACKAGE.get_packages())
