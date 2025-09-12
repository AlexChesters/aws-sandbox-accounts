import { type RouteConfig, index, route } from '@react-router/dev/routes'

export default [
  route('auth/login', 'routes/auth/login.tsx'),
  route('auth/callback', 'routes/auth/callback.tsx'),
  route('', 'routes/_auth.tsx', [
    index('routes/accounts/index.tsx'),
    route('user/me', 'routes/user/me/index.tsx')
  ])
] satisfies RouteConfig
