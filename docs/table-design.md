# Table design
This document covers the single-table design for this system.

## Table design

### Main table
| partition key - pk          | data                                                                         |
| --------------------------- | ---------------------------------------------------------------------------- |
| account_id#111111111111     | available                                                                    |
| account_id#222222222222     | leased                                                                       |
| account_id#333333333333     | initial                                                                      |
| lease_id#abc123-def456      | {"state": "active", "account": "111111111111", "user": "bill.bob@gmail.com"} |
| user_id#bill.bob@gmail.com  | {"lease": "abc123-def456", "account": "111111111111" }                       |
| account_status#available    |                                                                              |
| account_status#leased       |                                                                              |
| account_status#initial      | [222222222222]                                                               |
| account_status#all          | [111111111111,222222222222,333333333333]                                     |
| lease_status#active         | [abc123-def456]                                                              |

## Access patterns
- Listing all accounts in the pool, regardless of lease state
  - Query - `pk=account_status#all`
- Listing all accounts in the pool without an active lease
  - Query - `pkaccount_status#available`
- Listing all accounts in the pool in the initial state
  - Query - `pk=account_status#initial`
- Removing an account from the pool
  - Delete - `pk=account_id#<ACCOUNT_ID>`
  - Update - `pk=account_status#all` to remove `<ACCOUNT_ID>` from the `data` attribute
- Adding an account to the pool
  - Put - `pk=account_id#<ACCOUNT_ID>,data#initial`
  - Update - `pk=account_status#all` to add `<ACCOUNT_ID>` to the `data` attribute
  - Update - `pk=account_status#initial` to add `<ACCOUNT_ID>` to the `data` attribute
- Marking an account as available
  - Update - `pk=account_id#<ACCOUNT_ID>` to set `available` as the `data` attribute
  - Update - `pk=account_status#available` to add `<ACCOUNT_ID>` to the `data` attribute
  - Update all other `account_status#*` items to remove the account ID from everywhere else
- Listing all active leases
  - Query - `pk=lease_status#active`
- Retrieving information about a specific lease (e.g. the user that lease is assigned too)
  - Query - `pk=lease_id#<LEASE_ID>`
- Retrieving information about a specific user (e.g. a lease that user currently has)
  - Query - `pk=user_id#<USER_ID>`
- Creating a lease
  - Put - `pk=lease_id#<UUID>,data#{"state": "active", "account": "<ACCOUNT_ID">, "user": "<USER_ID>"}`
  - Update - `pk=lease_status#active` to add `<ACCOUNT_ID>` to the `data` attribute
- Deleting a lease
  - Delete `pk=lease_id#<UUID>`
  - Update - `pk=lease_status#active` to remove `<ACCOUNT_ID>` from the `data` attribute
- Adding a user
  - Put - `pk=user_id#<USER_ID>`
