import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'

import { AccountStatus, type Account } from '~/models/types'

type AccountsSectionProps = {
  status: AccountStatus,
  accounts: Account[]
}

export default function AccountsSection({ status, accounts }: AccountsSectionProps) {
  return (
    <Paper elevation={2} sx={{ p: 2, m: 2 }}>
      <Typography variant="h4" component="h1" className='capitalized' sx={{ mb: 1.5 }}>{status}</Typography>
      {
        accounts.length === 0 && (
          <Typography variant="body1">No {status} accounts in the pool.</Typography>
        )
      }
      <Grid container spacing={2}>
        {
          accounts.map((account) => (
            <Card variant="outlined" key={account.accountId}>
              <CardContent>
                <Typography variant="h5" component="h2">{account.name}</Typography>
                <Typography gutterBottom sx={{ color: 'text.secondary' }}>{account.accountId}</Typography>
              </CardContent>
            </Card>
          ))
        }
      </Grid>
    </Paper>
  )
}
