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
