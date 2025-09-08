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
    window.location.replace('/')
  }
} satisfies AuthProviderProps
