import { useEffect } from 'react'
import { useAuth } from 'react-oidc-context'

export default function LoginPage() {
  const auth = useAuth()

  useEffect(() => {
    if (!auth.isAuthenticated && !auth.isLoading) {
      auth.signinRedirect()
    }
  }, [auth])

  if (auth.isLoading) {
    return <div>Loading…</div>
  }

  if (auth.error) {
    return <div>Error: {auth.error.message}</div>
  }

  if (auth.isAuthenticated) {
    return <div>You are already signed in</div>
  }

  return null
}
