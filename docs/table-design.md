# Table design
This document covers the single-table design for this system.

## Table design

### Main table
| partition key - pk       | sort key - sk      | status     | lease               |
| ------------------------ | ------------------ | ---------- | ------------------- |
| account                  | 111111111111       | available  |                     |
| account                  | 222222222222       | leased     |                     |
| lease                    | abc123-def456      | active     |                     |
| user                     | bill.bob@gmail.com |            | lease-abc123-def456 |

### Status LSI
| partition key - pk | sort key - status | status     | lease               |
| ------------------ | ----------------- | ---------- | ------------------- |
| account            | 111111111111      | available  |                     |
| account            | 222222222222      | leased     | lease-abc123-def456 |

## Access patterns
- Listing all accounts in the pool, regardless of lease state
  - Query main table - `pk=account`
- Listing all accounts in the pool without an active lease
  - Query status LSI - `pk=account&status=available`
- Removing an account from the pool
  - Delete from main table `pk=account&sk=<ACCOUNT_ID>`
- Adding an account to the pool
  - Put to main table `pk=account&sk=<ACCOUNT_ID>`
- Listing all active leases
  - Query main table - `pk=lease`
- Retrieving information about a specific lease (e.g. the user that lease is assigned too)
  - Query main table - `pk=lease-<lease_id>`
- Retrieving information about a specific user (e.g. a lease that user currently has)
  - Query main table - `pk=user-<user_id>`
- Creating a lease
  - Put to main table `pk=lease&sk=<UUID>`
- Deleting a lease
  - Delete from main table `pk=lease&sk=<UUID>`
