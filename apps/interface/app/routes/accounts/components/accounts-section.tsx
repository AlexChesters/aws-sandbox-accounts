import { useContext } from 'react'

import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import Button from '@mui/material/Button'
import AssignmentAddIcon from '@mui/icons-material/AssignmentAdd'

import { AccountStatus, type Account } from '~/models/types'
import AccountCard from './accounts-section/account-card'
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
        accounts.length > 0 && status == AccountStatus.Available && (
          <Button
            size='small'
            sx={{ mb: 2 }}
            variant='contained'
            startIcon={<AssignmentAddIcon />}
            onClick={() => onCreateLease()}
          >
            Create lease
          </Button>
        )
      }
      {
        accounts.length === 0 && (
          <Typography variant='body1'>No {status} accounts in the pool.</Typography>
        )
      }
      <Grid container spacing={2}>
        {
          accounts.map((account) => {
            return (
              <AccountCard key={account.accountId} account={account} />
            )
          })
        }
      </Grid>
    </Paper>
  )
}

