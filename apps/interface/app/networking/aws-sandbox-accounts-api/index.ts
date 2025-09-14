import type { FetchAllAccountsResponse, FetchAllUsersResponse, CreateLeaseResponse } from './types'

export class APIClient {
  #baseUrl: string = 'https://test.api.sandbox.alexchesters.com'
  #requestHeaders: Record<string, string>

  constructor(accessToken: string) {
    this.#requestHeaders = {
      Authorization: `Bearer ${accessToken}`,
      Client: 'AWS Sandbox Accounts Interface'
    }
  }

  async fetchAllAccounts(): Promise<FetchAllAccountsResponse> {
    const res = await fetch(
      `${this.#baseUrl}/accounts`,
      {
        headers: {
          ...this.#requestHeaders
        }
      }
    )
    if (!res.ok) {
      throw new Error('Network response was not ok')
    }

    return res.json()
  }

  async fetchAllUsers(): Promise<FetchAllUsersResponse> {
    const res = await fetch(
      `${this.#baseUrl}/users`,
      {
        headers: {
          ...this.#requestHeaders
        }
      }
    )
    if (!res.ok) {
      throw new Error('Network response was not ok')
    }

    return res.json()
  }

  async createLease(userId: string, duration: string): Promise<CreateLeaseResponse> {
    const res = await fetch(
      `${this.#baseUrl}/leases`,
      {
        method: 'POST',
        headers: {
          ...this.#requestHeaders,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, duration })
      }
    )
    if (!res.ok) {
      throw new Error('Network response was not ok')
    }

    return res.json()
  }
}
