export class APIClient {
  baseUrl: string = 'https://test.api.sandbox.alexchesters.com'
  #requestHeaders: Record<string, string>

  constructor(accessToken: string) {
    this.#requestHeaders = {
      Authorization: `Bearer ${accessToken}`,
      Client: 'AWS Sandbox Accounts Interface'
    }
  }

  async fetchAllAccounts() {
    const res = await fetch(
      `${this.baseUrl}/accounts`,
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
}
