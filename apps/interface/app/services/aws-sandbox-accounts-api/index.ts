import { APIClient } from '~/networking/aws-sandbox-accounts-api'

export class AWSSandboxAccountsService {
  #apiClient: APIClient

  constructor(accessToken: string) {
    this.#apiClient = new APIClient(accessToken)
  }

  async fetchAllAccounts() {
    return this.#apiClient.fetchAllAccounts()
  }
}
