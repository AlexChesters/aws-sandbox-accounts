import { AccountStatus, type Account } from '~/models/types'

export type FetchAllAccountsResult = {
  [key in AccountStatus]: Account[]
}

export type FetchAllUsersResult = {
  userId: string
  userName: string
}[]
