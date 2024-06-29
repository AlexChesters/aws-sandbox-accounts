import os
import sys
import argparse
from pathlib import Path

from ruamel.yaml import YAML

parser = argparse.ArgumentParser()
parser.add_argument("--account-id", required=True)
args = parser.parse_args()

yaml = YAML()
script_dir = Path(__file__).parent.resolve()

account_id = args.account_id

sandbox_account_ids = [
    "905418121097", # alpha
    "891377354273", # bravo
    "471112670300" # charlie
]

if account_id not in sandbox_account_ids:
    print(f"[ERROR] - {account_id} is not a valid sandbox account, valid accounts are {sandbox_account_ids}")
    sys.exit(1)

with open(os.path.join(script_dir, "aws-nuke.template.yml"), "r", encoding="utf-8") as f:
    data = yaml.load(f)

with open(os.path.join(script_dir, "aws-nuke.yml"), "w", encoding="utf=8") as f:
    data["accounts"][account_id] = data["accounts"].pop("REPLACE_ME")
    yaml.dump(data, f)
