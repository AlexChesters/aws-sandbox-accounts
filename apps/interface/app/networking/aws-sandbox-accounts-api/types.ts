interface AccountDTO {
  account_id: string
  name: string
  status: string
}
export type FetchAllAccountsResponse = {
  [key: string]: AccountDTO[]
}
