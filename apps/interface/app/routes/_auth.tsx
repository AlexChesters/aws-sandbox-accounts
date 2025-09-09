import { Outlet, useLocation, Navigate } from 'react-router'
import { useAuth } from 'react-oidc-context'

export default function AuthLayout() {
  const auth = useAuth()
  const location = useLocation()

  if (auth.isLoading) {
    return <div>Loading...</div>
  }

  if (!auth.isAuthenticated) {
    return (
      <Navigate
        to="/auth/login"
        state={{ from: location }}
        replace
      />
    )
  }

  return <Outlet />
}
