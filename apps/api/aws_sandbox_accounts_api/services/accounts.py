from aws_sandbox_accounts_api.models.account import Account, AccountStatus

def get_all_accounts() -> list[Account]:
    for status in AccountStatus:
        print(f"fetching accounts with status: {status.value}")

    return []
