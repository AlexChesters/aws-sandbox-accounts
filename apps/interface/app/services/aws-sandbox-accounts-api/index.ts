import { APIClient } from '~/networking/aws-sandbox-accounts-api'

enum AccountStatus {
  Available = 'available',
  Leased = 'leased',
  Dirty = 'dirty',
  Failed = 'failed'
}
interface Account {
  accountId: string
}
type FetchAllAccountsResponse = {
  [key in AccountStatus]: Account[]
}

export class AWSSandboxAccountsService {
  #apiClient: APIClient

  constructor(accessToken: string) {
    this.#apiClient = new APIClient(accessToken)
  }

  async fetchAllAccounts(): Promise<FetchAllAccountsResponse> {
    const apiResponse = await this.#apiClient.fetchAllAccounts()
    const accounts: FetchAllAccountsResponse = {
      [AccountStatus.Available]: [],
      [AccountStatus.Leased]: [],
      [AccountStatus.Dirty]: [],
      [AccountStatus.Failed]: []
    }

    for (const [status, accountIds] of Object.entries(apiResponse)) {
      const accountStatus = Object.values(AccountStatus).find(
        (enumValue) => enumValue.toLowerCase() === status.toLowerCase()
      ) as AccountStatus | undefined

      if (!accountStatus) {
        console.warn(`Unknown account status: ${status}`)
        continue
      }
      accounts[accountStatus] = accountIds.map((accountId) => ({
        accountId
      }))
    }

    return accounts
  }
}
