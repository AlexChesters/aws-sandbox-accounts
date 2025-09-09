import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'

interface UserModel {
  emailAddress: string;
}
type UserProps = {
  user: UserModel;
  onSignOut: () => void;
}

export default function User ({ user, onSignOut }: UserProps) {
  return (
    <Paper sx={{ p: 2, m: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Typography variant="h3" component="h1" gutterBottom>My profile</Typography>
      <Typography variant="body1" gutterBottom>Email address: {user.emailAddress}</Typography>
      <Button sx={{ marginTop: 'auto', alignSelf: 'flex-start' }} variant="contained" onClick={onSignOut}>Sign out</Button>
    </Paper>
  )
}
