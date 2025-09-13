import { useState } from 'react'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogContentText from '@mui/material/DialogContentText'
import DialogTitle from '@mui/material/DialogTitle'
import Select from '@mui/material/Select'
import FormControl from '@mui/material/FormControl'
import MenuItem from '@mui/material/MenuItem'
import Button from '@mui/material/Button'

import { type User } from '~/models/types'

type LeaseCreationDialogProps = {
  users: User[]
  handleSubmit: ({ user } : { user: User }) => void
}

export default function LeaseCreationDialog (props: LeaseCreationDialogProps) {
  const [selectedUser, setSelectedUser] = useState<User>(props.users[0])

  const handleSubmit = () => {
    props.handleSubmit({ user: selectedUser })
  }

  return (
    <Dialog open={true}>
      <DialogTitle>Create lease</DialogTitle>
      <DialogContent>
        <DialogContentText sx={{ mb: 2 }}>
          Create a lease for an account using the form below.
        </DialogContentText>
        <FormControl fullWidth>
          <Select
            value={selectedUser.userId}
            label='User'
            onChange={(event) => {
              const user = props.users.find(user => user.userId === event.target.value)
              if (user) {
                setSelectedUser(user)
              }
            }}
          >
            {props.users.map(user => (
              <MenuItem key={user.userId} value={user.userId}>{user.userName}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => {}}>Cancel</Button>
        <Button onClick={handleSubmit}>Subscribe</Button>
      </DialogActions>
    </Dialog>
  )
}
