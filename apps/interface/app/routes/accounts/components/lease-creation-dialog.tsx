import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogTitle from '@mui/material/DialogTitle'
import Select from '@mui/material/Select'
import FormControl from '@mui/material/FormControl'
import MenuItem from '@mui/material/MenuItem'
import Button from '@mui/material/Button'

import { type User } from '~/models/types'

type LeaseCreationDialogProps = {
  handleSubmit: (user: User) => void
}

export default function LeaseCreationDialog (_props: LeaseCreationDialogProps) {
  const handleSubmit = () => {
    console.log('submit')

    // props.handleSubmit()
  }

  return (
    <Dialog open={true}>
      <DialogTitle>Create lease</DialogTitle>
      <DialogContent>
        <FormControl fullWidth>
          <Select
            labelId='demo-simple-select-label'
            id='demo-simple-select'
            value={10}
            label='Age'
            onChange={() => {}}
          >
            <MenuItem value={10}>Ten</MenuItem>
            <MenuItem value={20}>Twenty</MenuItem>
            <MenuItem value={30}>Thirty</MenuItem>
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
