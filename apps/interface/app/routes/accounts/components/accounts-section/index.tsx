import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'

import { AccountStatus, type Account } from '~/models/types'

type AccountsSectionProps = {
  status: AccountStatus,
  accounts: Account[]
}

export default function AccountsSection({ status, accounts }: AccountsSectionProps) {
  return (
    <Paper elevation={2} sx={{ p: 2, m: 2 }}>
      <Typography variant="h4" component="h1" className='capitalized'>{status}</Typography>
      {
        accounts.length === 0 && (
          <Typography variant="body1">No {status} accounts in the pool.</Typography>
        )
      }
      {
        accounts.map((account) => (
          <div key={account.accountId}>
            <Typography variant="body1">Account ID: {account.accountId}</Typography>
            <hr />
          </div>
        ))
      }
    </Paper>
  )
}
