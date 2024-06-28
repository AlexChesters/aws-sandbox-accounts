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
        # TODO: verify account has no leases before deleting
        current_accounts = self.db_client.list_accounts()

        if not current_accounts:
            self.logger.error("no accounts in the pool")
            sys.exit(1)

        answers = inquirer.prompt([
            inquirer.List(
                "account_id",
                message="Choose an account to remove",
                choices=[account.account_id for account in current_accounts]
            )]
        )

        self.db_client.remove_account(answers["account_id"])

    def add_account(self):
        answers = inquirer.prompt([
            inquirer.Text(
                "account_id",
                message="Enter the account ID"
            )]
        )

        self.db_client.add_account(answers["account_id"])
