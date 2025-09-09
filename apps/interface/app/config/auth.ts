interface AuthConfig {
  authority: string,
  clientId: string,
  redirectUri: string,
  logoutRedirectUri: string,
  responseType: string,
  scope: string
}

export default {
  authority: 'https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_t4m80oL3Y',
  clientId: '3sjic4vag51jg3734gfb2s6kki',
  redirectUri: 'http://localhost:5173/auth/callback',
  logoutRedirectUri: 'http://localhost:5173/auth/logout',
  responseType: 'code',
  scope: 'email openid profile'
} satisfies AuthConfig
