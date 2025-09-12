import { AccountStatus, type Account } from '~/models/types'

export type FetchAllAccountsResponse = {
  [key in AccountStatus]: Account[]
}
