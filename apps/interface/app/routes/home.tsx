import { useAuth } from 'react-oidc-context';

import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "AWS Sandbox Accounts" }
  ];
}

export default function Home() {
  const auth = useAuth();

  console.log(auth)

  return (
    <main>
      <h1>Hello, world!</h1>
    </main>
  );
}
