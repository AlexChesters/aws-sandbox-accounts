from pool_manager.db.db import DBClient
from pool_manager.utils.logger import Logger

class Actions:
    def __init__(self):
        self.logger = Logger()
        self.db_client = DBClient()

    def list_accounts(self):
        results = self.db_client.list_accounts()
        self.logger.plain(results)

    def remove_account(self, account_id: str):
        self.db_client.remove_account(account_id)
