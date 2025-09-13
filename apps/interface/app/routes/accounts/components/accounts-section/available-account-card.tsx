import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'

import { type Account } from '~/models/types'

type AvailableAccountCard = {
  account: Account
}

export default function AvailableAccountCard({ account }: AvailableAccountCard) {
  return (
    <Card variant='outlined' key={account.accountId}>
      <CardContent>
        <Typography variant='h5' component='h2'>{account.name}</Typography>
        <Typography gutterBottom sx={{ color: 'text.secondary' }}>{account.accountId}</Typography>
      </CardContent>
    </Card>
  )
}
