interface AccountDTO {
  account_id: string
  name: string
  status: string
}
export type FetchAllAccountsResponse = {
  [key: string]: AccountDTO[]
}

interface UserDTO {
  user_id: string
  user_name: string
}
export type FetchAllUsersResponse = UserDTO[]
