import { APIClient } from '~/networking/aws-sandbox-accounts-api'
import { AccountStatus } from '~/models/types'
import type { FetchAllAccountsResult, FetchAllUsersResult } from './types'

export class AWSSandboxAccountsService {
  #apiClient: APIClient

  constructor(accessToken: string) {
    this.#apiClient = new APIClient(accessToken)
  }

  async fetchAllAccounts(): Promise<FetchAllAccountsResult> {
    const apiResponse = await this.#apiClient.fetchAllAccounts()
    const accounts: FetchAllAccountsResult = {
      [AccountStatus.Available]: [],
      [AccountStatus.Pending]: [],
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
      accounts[accountStatus] = accountIds.map((account) => ({
        accountId: account.account_id,
        name: account.name,
        status: account.status
      }))
    }

    return accounts
  }

  async fetchAllUsers(): Promise<FetchAllUsersResult> {
    const apiResponse = await this.#apiClient.fetchAllUsers()

    return apiResponse.map((user) => ({
      userId: user.user_id,
      userName: user.user_name
    }))
  }
}
