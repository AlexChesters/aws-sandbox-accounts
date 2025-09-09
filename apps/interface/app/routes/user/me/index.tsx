import { useAuth } from 'react-oidc-context'
import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'

export default function Me() {
  const auth = useAuth()

  if (!auth.user) {
    // TODO: handle error
    return <p>Error: User not authenticated</p>
  }

  console.log(auth.user.profile)

  return (
    <Paper sx={{ p: 2, m: 2 }}>
      <Typography variant="h3" component="h1" gutterBottom>My profile</Typography>

      <Typography variant="body1" gutterBottom>Email address: {auth.user.profile.email}</Typography>
    </Paper>
  )
}
