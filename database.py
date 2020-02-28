import pymysql
import re
import logging


class Database:

    def __init__(self):
        # Connect to the database
        self.connection = pymysql.connect(
            host='remotemysql.com',
            user='sFHp69uV0B',
            password='mJydstQBBv',
            db='sFHp69uV0B',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def _get_record(self, query, values, is_close=True):
        result = {}
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()
                # print(result)
        finally:
            if is_close:
                self.connection.close()
        return result

    def _execute(self, query, values, is_close=True):
        lastrowid = None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                self.connection.commit()
                lastrowid = cursor.lastrowid
        except pymysql.err.IntegrityError as error:
            logging.error('IntegrityError: %s', error)
            return 0
        finally:
            if is_close:
                self.connection.close()
        return lastrowid

    def get_package_info(self, package):
        return self._get_record("""
            SELECT * FROM `Packages` WHERE `Name`=%s AND `Version`=%s
        """, (package['Package'], package['Version']))

    def save_package(self, package):
        publication = package['Date/Publication']
        # print(publication, type(publication))
        if isinstance(publication, str):
            matches = [
                match.groups() for match in re.finditer(
                    r'([\d\-\:\s]+)', publication)
            ]
            # print(matches)
            if matches:
                publication = matches[0][0].strip()
            # print(publication)
        return self._execute("""
            INSERT INTO
                `Packages` (`Name`, `Version`, `Publication`, `Title`,
                            `Description`)
            VALUES (%s, %s, %s, %s, %s)
        """, (package['Package'], package['Version'], publication,
              package['Title'], package['Description']))

    @staticmethod
    def _parse_people_info(data):
        matches = [match.groups()
                   for match in re.finditer(r'(.*)[<\[](.*)[>\]]', data)]
        name, email = data, ''
        if matches:
            name, email = matches[0]
        if '@' not in email:
            email = ''
        if '[' in name and ']' not in name:
            name = name.split('[')[0].strip()
        if '[' not in name and ']' in name:
            logging.warning('Warning: Invalid name (%s)!', name)
            return False
        name = name.strip()
        return (name, email)

    def _add_people(self, people_name, package_id, table):
        status = False
        row_id = 0
        info = self._parse_people_info(people_name)
        if not info:
            return False
        name, email = info
        sql = """
            SELECT * from `People` WHERE `Name`=%s
        """
        values = (name,)
        if email:
            sql = """
                SELECT * from `People` WHERE `Name`=%s AND `Email`=%s
            """
            values = (name, email)
        record = self._get_record(sql, values, False)
        if record:
            logging.info('Person Record Found: %s', record['id'])
            row_id = int(record['id'])
        if not row_id:
            row_id = self._execute("""
                    INSERT INTO `People` (`Name`, `Email`)
                    VALUES (%s, %s)
                """, (name, email or '-'), False)
        if row_id:
            map_row_id = self._execute("""
                INSERT INTO `{0}` (`PackageID`, `PeopleID`)
                VALUES (%s, %s)
            """.format(table), (package_id, row_id), False)
            # print(map_row_id)
            status = bool(map_row_id)
        return status

    def add_authors(self, authors, package_id):
        count = 0
        for author in authors.split(','):
            if self._add_people(author, package_id, 'Authors'):
                count += 1
        self.connection.close()
        return count

    def add_maintainers(self, maintainers, package_id):
        count = 0
        for maintainer in maintainers.split(','):
            if self._add_people(maintainer, package_id, 'Maintainers'):
                count += 1
        self.connection.close()
        return count
