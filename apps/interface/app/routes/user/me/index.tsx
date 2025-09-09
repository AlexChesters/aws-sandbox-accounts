import { useAuth } from 'react-oidc-context'
import Paper from '@mui/material/Paper'

export default function Me() {
  const auth = useAuth()

  if (!auth.user) {
    // TODO: handle error
    return <p>Error: User not authenticated</p>
  }

  console.log(auth.user.profile)

  return (
    <Paper sx={{ p: 2, m: 2 }}>
      <h1>My profile</h1>
    </Paper>
  )
}
