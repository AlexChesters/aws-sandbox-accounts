import { useAuth } from 'react-oidc-context'
import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'

import authConfig from '~/config/auth'

export default function Me() {
  const auth = useAuth()

  if (!auth.user) {
    // TODO: handle error
    return <p>Error: User not authenticated</p>
  }

  const onSignOut = () => {
    auth.signoutRedirect({
      extraQueryParams: {
        client_id: authConfig.clientId,
        logout_uri: authConfig.logoutRedirectUri
      }
    })
  }

  return (
    <Paper sx={{ p: 2, m: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Typography variant="h3" component="h1" gutterBottom>My profile</Typography>
      <Typography variant="body1" gutterBottom>Email address: {auth.user.profile.email}</Typography>
      <Button sx={{ marginTop: 'auto', alignSelf: 'flex-start' }} variant="contained" onClick={onSignOut}>Sign out</Button>
    </Paper>
  )
}
