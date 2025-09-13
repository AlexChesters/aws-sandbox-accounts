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
import InputLabel from '@mui/material/InputLabel'

import { type User } from '~/models/types'

export interface Duration {
  value: string
  label: string
}

type LeaseCreationDialogProps = {
  users: User[]
  handleSubmit: ({ user, duration } : { user: User, duration: Duration }) => void
  handleCancel: () => void
}

const DURATIONS: Duration[] = [
  {
    label: '5 minutes',
    value: '5m'
  },
  {
    label: '30 minutes',
    value: '30m'
  },
  {
    label: '1 hour',
    value: '1h'
  },
  {
    label: '3 hours',
    value: '3h'
  },
  {
    label: '6 hours',
    value: '6h'
  },
  {
    label: '12 hours',
    value: '12h'
  },
  {
    label: '24 hours',
    value: '24h'
  },
  {
    label: '3 days',
    value: '3d'
  },
  {
    label: '7 days',
    value: '7d'
  }
]

export default function LeaseCreationDialog (props: LeaseCreationDialogProps) {
  const [selectedUser, setSelectedUser] = useState<User>(props.users[0])
  const [selectedDuration, setSelectedDuration] = useState<Duration>(DURATIONS[4])

  const handleSubmit = () => {
    props.handleSubmit({ user: selectedUser, duration: selectedDuration })
  }

  return (
    <Dialog open={true}>
      <DialogTitle>Create lease</DialogTitle>
      <DialogContent>
        <DialogContentText sx={{ mb: 2 }}>
          Create a lease for an account using the form below.
        </DialogContentText>
        <FormControl fullWidth>
          <InputLabel id='user-select-label'>User</InputLabel>
          <Select
            labelId='user-select-label'
            value={selectedUser.userId}
            label='User'
            onChange={(event) => {
              const user = props.users.find(user => user.userId === event.target.value)
              if (user) {
                setSelectedUser(user)
              }
            }}
          >
            {
              props.users.map(user => (
                <MenuItem key={user.userId} value={user.userId}>{user.userName}</MenuItem>
              ))
            }
          </Select>
        </FormControl>
        <FormControl fullWidth sx={{ mt: 2 }}>
          <InputLabel id='duration-select-label'>Duration</InputLabel>
          <Select
            labelId='duration-select-label'
            value={selectedDuration.value}
            label='Duration'
            onChange={(event) => {
              const duration = DURATIONS.find(duration => duration.value === event.target.value)
              if (duration) {
                setSelectedDuration(duration)
              }
            }}
          >
            {
              DURATIONS.map(duration => (
                <MenuItem key={duration.value} value={duration.value}>{duration.label}</MenuItem>
              ))
            }
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.handleCancel}>Cancel</Button>
        <Button onClick={handleSubmit}>Subscribe</Button>
      </DialogActions>
    </Dialog>
  )
}
