import Button from '@mui/material/Button'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogContentText from '@mui/material/DialogContentText'
import DialogTitle from '@mui/material/DialogTitle'

type AlertProps = {
  title?: string;
  message: string;
  onAcknowledge?: () => void;
}

export default function Alert({ title, message, onAcknowledge }: AlertProps) {
  return (
    <Dialog
      open={true}
      onClose={() => { }}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      {
        title && <DialogTitle id="alert-dialog-title">{title}</DialogTitle>
      }
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          {message}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onAcknowledge}>Acknowledge</Button>
      </DialogActions>
    </Dialog>
  )
}
