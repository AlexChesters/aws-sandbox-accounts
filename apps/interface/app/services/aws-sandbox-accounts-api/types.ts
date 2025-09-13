import { AccountStatus, type Account, type User } from '~/models/types'

export type FetchAllAccountsResult = {
  [key in AccountStatus]: Account[]
}

export type FetchAllUsersResult = User[]
