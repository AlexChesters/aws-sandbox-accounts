.PHONY: ssh
ssh:
	docker exec -w /workspaces/aws-sandbox-accounts -it vscode-devcontainer_aws-sandbox-accounts bash
