import inquirer

from pool_manager.actions.actions import Actions

actions = Actions()
answers = inquirer.prompt([
    inquirer.List(
        "action",
        message="Choose an action",
        choices=[
            ("List accounts in the pool", actions.list_accounts),
            ("Remove an account from the pool", actions.remove_account)
        ]
    )]
)

action_fn: callable = answers["action"]
action_fn()
