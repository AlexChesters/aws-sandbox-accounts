export enum AccountStatus {
  Available = 'available',
  Leased = 'leased',
  Dirty = 'dirty',
  Failed = 'failed'
}

export interface Account {
  accountId: string
}
