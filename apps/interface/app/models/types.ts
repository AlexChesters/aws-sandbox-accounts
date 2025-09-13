export enum AccountStatus {
  Available = 'available',
  Leased = 'leased',
  Pending = 'pending',
  Dirty = 'dirty',
  Failed = 'failed'
}

export interface Account {
  accountId: string
  name: string
  status: string
}

export interface User {
  userId: string
  userName: string
}
