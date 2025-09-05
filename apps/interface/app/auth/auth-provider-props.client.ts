import type { AuthProviderProps } from 'react-oidc-context'
import { WebStorageStateStore } from 'oidc-client-ts'

import authConfig from '../config/auth'

export default {
  authority: authConfig.authority,
  client_id: authConfig.clientId,
  redirect_uri: authConfig.redirectUri,
  response_type: authConfig.responseType,
  scope: authConfig.scope,
  userStore: new WebStorageStateStore({ store: window.localStorage }),
  onSigninCallback: () => {
    // Clean up OIDC params from the URL
    window.history.replaceState({}, document.title, window.location.pathname)
    // Redirect to the originally intended path, if present
    const redirectPath = window.localStorage.getItem('postLoginRedirectPath')
    if (redirectPath) {
      window.localStorage.removeItem('postLoginRedirectPath')
      window.location.replace(redirectPath)
    } else {
      window.location.replace('/')
    }
  }
} satisfies AuthProviderProps
