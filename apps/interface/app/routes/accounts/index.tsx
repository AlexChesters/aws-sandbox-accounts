import { useEffect } from 'react'
import { useAuth } from 'react-oidc-context'

import type { Route } from '../+types/home'
import { APIClient } from '~/services/aws-sandbox-accounts-api'

export function meta(_: Route.MetaArgs) {
  return [
    { title: 'AWS Sandbox Accounts' }
  ]
}

export default function Accounts() {
  const auth = useAuth()

  useEffect(() => {
    if (auth.isAuthenticated && auth.user) {
      const apiClient = new APIClient(auth.user?.access_token)

      apiClient.fetchAllAccounts()
        .then(data => {
          console.log('API Response:', data)
        })
        .catch(error => {
          console.error('API Error:', error)
        })
    }
  }, [auth])

  return (
    <main>
      <h1>Hello, world!</h1>
    </main>
  )
}
