import { useContext } from 'react'

import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'

import { AccountStatus, type Account } from '~/models/types'
import AvailableAccountCard from './accounts-section/available-account-card'
import { AccountsActionsContext } from '../accounts-actions-context'

type AccountsSectionProps = {
  status: AccountStatus,
  accounts: Account[]
}

export default function AccountsSection({ status, accounts }: AccountsSectionProps) {
  const { onCreateLease } = useContext(AccountsActionsContext)

  return (
    <Paper elevation={2} sx={{ p: 2, m: 2 }}>
      <Typography variant='h4' component='h1' className='capitalized' sx={{ mb: 1.5 }}>{status}</Typography>
      {
        accounts.length === 0 && (
          <Typography variant='body1'>No {status} accounts in the pool.</Typography>
        )
      }
      <Grid container spacing={2}>
        {
          accounts.map((account) => {
            switch (status) {
              case AccountStatus.Available:
                return (
                  <AvailableAccountCard key={account.accountId} account={account} onCreateLease={onCreateLease} />
                )
            }
          })
        }
      </Grid>
    </Paper>
  )
}

