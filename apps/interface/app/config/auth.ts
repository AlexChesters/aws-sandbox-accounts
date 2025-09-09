interface AuthConfig {
  authority: string;
  clientId: string;
  redirectUri: string;
  logoutRedirectUri: string;
  responseType: string;
  scope: string;
}

enum Hostname {
  Localhost = 'localhost',
  Test = 'test.sandbox.alexchesters.com',
  Live = 'sandbox.alexchesters.com'
}

const configs: Record<string, AuthConfig> = {
  [Hostname.Localhost]: {
    authority: 'https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_t4m80oL3Y',
    clientId: '3sjic4vag51jg3734gfb2s6kki',
    redirectUri: 'http://localhost:5173/auth/callback',
    logoutRedirectUri: 'http://localhost:5173/auth/logout',
    responseType: 'code',
    scope: 'email openid profile'
  },
  [Hostname.Test]: {
    authority: 'https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_t4m80oL3Y',
    clientId: '3sjic4vag51jg3734gfb2s6kki',
    redirectUri: 'http://test.sandbox.alexchesters.com/auth/callback',
    logoutRedirectUri: 'http://test.sandbox.alexchesters.com/auth/logout',
    responseType: 'code',
    scope: 'email openid profile'
  },
  [Hostname.Live]: {
    authority: 'https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_bQT90t9tf',
    clientId: '3sjic4vag51jg3734gfb2s6kki',
    redirectUri: 'http://sandbox.alexchesters.com/auth/callback',
    logoutRedirectUri: 'http://sandbox.alexchesters.com/auth/logout',
    responseType: 'code',
    scope: 'email openid profile'
  }
}

function getAuthConfig(): AuthConfig {
  const hostname = typeof window !== 'undefined' ? window.location.hostname : 'localhost'
  return configs[hostname] || configs[Hostname.Live]
}

export default getAuthConfig()
