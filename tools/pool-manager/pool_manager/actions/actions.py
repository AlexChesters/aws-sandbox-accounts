from pool_manager.db.db import list_accounts
from pool_manager.utils.logger import Logger

logger = Logger()

class Actions:
    def __init__(self, table_name):
        self.table_name = table_name

    def list_accounts(self):
        results = list_accounts(self.table_name)
        logger.plain(results)
