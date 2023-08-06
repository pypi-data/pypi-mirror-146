import os
import unittest
from wsqluse.wsqluse import Wsqluse
from gravity_core_api.wserver_update_commands import functions


class TestCase(unittest.TestCase):
    sql_shell = Wsqluse(dbname=os.environ.get('DBNAME'),
                        password=os.environ.get('DBPASS'),
                        user=os.environ.get('DBUSER'),
                        host=os.environ.get('DBHOST'))

    def test_check_new_client(self):
        data = {'full_name': 'test_carrier_6',
                'inn': '12345689',
                'kpp': '123412'}
        response = functions.clients_execute(self.sql_shell, data)
        print(response)


if __name__  == '__main__':
    unittest.main()

