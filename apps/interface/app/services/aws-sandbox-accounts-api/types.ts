import { AccountStatus, type Account } from '~/models/types'

export type FetchAllAccountsResult = {
  [key in AccountStatus]: Account[]
}
