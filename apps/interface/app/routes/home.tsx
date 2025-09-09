import type { Route } from './+types/home'

export function meta(_: Route.MetaArgs) {
  return [
    { title: 'AWS Sandbox Accounts' }
  ]
}

export default function Home() {
  return (
    <main>
      <h1>Hello, world!</h1>
    </main>
  )
}
