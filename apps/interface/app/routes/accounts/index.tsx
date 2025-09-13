import { useEffect, useState } from 'react'
import { useAuth } from 'react-oidc-context'

import type { Route } from '../accounts/+types'
import { AWSSandboxAccountsService } from '~/services/aws-sandbox-accounts-api'
import { AccountStatus, type Account, type User } from '~/models/types'
import { AccountsActionsContext } from './accounts-actions-context'

import Loading from '~/components/loading'
import AccountsSection from './components/accounts-section'
import LeaseCreationDialog from './components/lease-creation-dialog'

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
    [AccountStatus.Pending]: [],
    [AccountStatus.Leased]: [],
    [AccountStatus.Dirty]: [],
    [AccountStatus.Failed]: []
  })
  const [users, setUsers] = useState<User[]>([])
  const [showLeaseDialog, setShowLeaseDialog] = useState(false)

  const fetchUsers = async () => {
    if (auth.isAuthenticated && auth.user) {
      const service = new AWSSandboxAccountsService(auth.user.access_token)

      service.fetchAllUsers()
        .then(data => {
          setUsers(data)
        })
        .catch(error => {
          console.error('API Error when fetching users:', error)
        })
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  useEffect(() => {
    if (auth.isAuthenticated && auth.user) {
      const service = new AWSSandboxAccountsService(auth.user.access_token)

      service.fetchAllAccounts()
        .then(data => {
          setAccounts(data)
          setLoading(false)
        })
        .catch(error => {
          console.error('API Error when fetching accounts:', error)
          setLoading(false)
        })
    }
  }, [auth])

  const onCreateLease = async (accountId: string) => {
    console.log(`Create lease for account ID: ${accountId}`)

    if (auth.isAuthenticated && auth.user) {
      const _ = new AWSSandboxAccountsService(auth.user.access_token)

      if (!users.length) {
        await fetchUsers()
      }

      console.log('Users:', users)
      setShowLeaseDialog(true)
    }
  }

  if (loading) {
    return <Loading />
  }

  if (showLeaseDialog) {
    return <LeaseCreationDialog handleSubmit={(user: User) => { console.log('selected user:', user) }} />
  }

  // TODO: fix bug where bottom navigation covers part of the accounts list
  return (
    <main>
      <AccountsActionsContext value={{ onCreateLease }}>
        <AccountsSection status={AccountStatus.Available} accounts={accounts[AccountStatus.Available]} />
        <AccountsSection status={AccountStatus.Pending} accounts={accounts[AccountStatus.Pending]} />
        <AccountsSection status={AccountStatus.Leased} accounts={accounts[AccountStatus.Leased]} />
        <AccountsSection status={AccountStatus.Dirty} accounts={accounts[AccountStatus.Dirty]} />
        <AccountsSection status={AccountStatus.Failed} accounts={accounts[AccountStatus.Failed]} />
      </AccountsActionsContext>
    </main>
  )
}
