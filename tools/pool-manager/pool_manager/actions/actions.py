import sys

import inquirer

from pool_manager.db.db import DBClient
from pool_manager.utils.logger import Logger

class Actions:
    def __init__(self):
        self.logger = Logger()
        self.db_client = DBClient()

    def list_accounts(self):
        results = self.db_client.list_accounts()
        self.logger.plain(results)

    def remove_account(self):
        current_accounts = self.db_client.list_accounts()

        if not current_accounts:
            self.logger.error("no accounts in the pool")
            sys.exit(1)

        print(current_accounts)

        # answers = inquirer.prompt([
        #     inquirer.List(
        #         "account",
        #         message="Choose an action",
        #         choices=[
        #             ("List accounts in the pool", actions.list_accounts),
        #             ("Remove an account from the pool", actions.remove_account)
        #         ]
        #     )]
        # )

        # self.db_client.remove_account(account_id)
