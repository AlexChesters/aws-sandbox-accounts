import { createContext } from 'react'

type AccountsActionsContextType = {
  onCreateLease: (accountId: string) => void
}
export const AccountsActionsContext = createContext<AccountsActionsContextType>({
  onCreateLease: (_accountId: string) => {}
})
