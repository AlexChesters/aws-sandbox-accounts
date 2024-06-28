from pool_manager.db.db import DBClient
from pool_manager.utils.logger import Logger

class Actions:
    def __init__(self, table_name):
        self.logger = Logger()
        self.table_name = table_name
        self.db_client = DBClient()

    def list_accounts(self):
        results = self.db_client.list_accounts(self.table_name)
        self.logger.plain(results)
