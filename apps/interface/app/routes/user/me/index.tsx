import { useAuth } from 'react-oidc-context'

import authConfig from '~/config/auth'
import UserComponent from '~/routes/user/me/components/user'

export default function Me() {
  const auth = useAuth()

  if (!auth.user || !auth.user.profile.email) {
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
    <UserComponent user={{ emailAddress: auth.user.profile.email }} onSignOut={onSignOut} />
  )
}
