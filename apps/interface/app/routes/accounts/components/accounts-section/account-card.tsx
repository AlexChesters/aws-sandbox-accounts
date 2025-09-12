import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardActions from '@mui/material/CardActions'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import AssignmentAddIcon from '@mui/icons-material/AssignmentAdd'

import { AccountStatus, type Account } from '~/models/types'

type AccountCardProps = {
  account: Account
  status: AccountStatus
}

export default function AccountCard({ account, status }: AccountCardProps) {
  return (
    <Card variant='outlined' key={account.accountId}>
      <CardContent>
        <Typography variant='h5' component='h2'>{account.name}</Typography>
        <Typography gutterBottom sx={{ color: 'text.secondary' }}>{account.accountId}</Typography>

        {
          status == AccountStatus.Available && (
            <CardActions>
              <Button size='small' variant='contained' startIcon={<AssignmentAddIcon />}>Create lease</Button>
            </CardActions>
          )
        }
      </CardContent>
    </Card>
  )
}
