# AWS Sandbox Accounts

This is a monorepo for managing AWS sandbox accounts for learning and experimentation. After a period of use these
accounts are recreated (using `aws-nuke`) to ensure a clean state for the next user.

## General instructions

Always think before answering, breaking the problem down into logical steps.

## Project structure

- apps/ : Microservice applications
  - account-cleaner/ : Step Function responsible for running `aws-nuke` to reset accounts to a clean state
  - account-manager/ : Step Function responsible for finding dirty accounts and cleaning them
  - auth-client/ : Lambda function to manage user access to accounts
  - db-client/ : Lambda function to manage the DynamoDB database
  - interface/ : Front-end web application written in React and TypeScript
  - lease-creator/ : Step Function responsible for creating new account leases
  - lease-janitor/ : Step Function responsible for cleaning up expired leases
