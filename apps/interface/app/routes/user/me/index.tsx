import { useAuth } from 'react-oidc-context'

import authConfig from '~/config/auth'
import UserComponent from '~/routes/user/me/components/user'
import Alert from '~/components/alert'

export default function Me() {
  const auth = useAuth()

  const onSignOut = () => {
    auth.signoutRedirect({
      extraQueryParams: {
        client_id: authConfig.clientId,
        logout_uri: authConfig.logoutRedirectUri
      }
    })
  }

  if (!auth.user || !auth.user.profile.email) {
    return <Alert
      message="Something went wrong, unfortunately we'll need to log you out."
      onAcknowledge={onSignOut}
    />
  }

  return (
    <UserComponent user={{ emailAddress: auth.user.profile.email }} onSignOut={onSignOut} />
  )
}
