import { createContext } from 'react'

type AccountsActionsContextType = {
  onCreateLease: () => void
}
export const AccountsActionsContext = createContext<AccountsActionsContextType>({
  onCreateLease: () => {}
})
