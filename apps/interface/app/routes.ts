import { type RouteConfig, index, route } from '@react-router/dev/routes'

export default [
  route('login', 'routes/login.tsx'),
  route('auth/callback', 'routes/callback.tsx'),
  route('', 'routes/_auth.tsx', [
    index('routes/home.tsx')
  ])
] satisfies RouteConfig
