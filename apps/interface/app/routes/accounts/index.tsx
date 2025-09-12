import { useEffect, useState } from 'react'
import { useAuth } from 'react-oidc-context'

import type { Route } from '../accounts/+types'
import { AWSSandboxAccountsService } from '~/services/aws-sandbox-accounts-api'
import { AccountStatus, type Account } from '~/models/types'

import Loading from '~/components/loading'
import AccountsSection from './components/accounts-section'

export function meta(_: Route.MetaArgs) {
  return [
    { title: 'AWS Sandbox Accounts' }
  ]
}

export default function Accounts() {
  const auth = useAuth()
  const [loading, setLoading] = useState(true)
  const [accounts, setAccounts] = useState<Record<AccountStatus, Account[]>>({
    [AccountStatus.Available]: [],
    [AccountStatus.Leased]: [],
    [AccountStatus.Dirty]: [],
    [AccountStatus.Failed]: []
  })

  useEffect(() => {
    if (auth.isAuthenticated && auth.user) {
      const service = new AWSSandboxAccountsService(auth.user.access_token)

      service.fetchAllAccounts()
        .then(data => {
          console.log('API Response:', data)
          setAccounts(data)
          setLoading(false)
        })
        .catch(error => {
          console.error('API Error:', error)
          setLoading(false)
        })
    }
  }, [auth])

  if (loading) {
    return <Loading />
  }

  return (
    <main>
      <AccountsSection status={AccountStatus.Available} accounts={accounts[AccountStatus.Available]} />
      <AccountsSection status={AccountStatus.Leased} accounts={accounts[AccountStatus.Leased]} />
      <AccountsSection status={AccountStatus.Dirty} accounts={accounts[AccountStatus.Dirty]} />
      <AccountsSection status={AccountStatus.Failed} accounts={accounts[AccountStatus.Failed]} />
    </main>
  )
}
