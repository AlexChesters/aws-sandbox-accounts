import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import Paper from '@mui/material/Paper'
import BottomNavigation from '@mui/material/BottomNavigation'
import BottomNavigationAction from '@mui/material/BottomNavigationAction'
import HomeRoundedIcon from '@mui/icons-material/HomeRounded'
import AccountCircleIcon from '@mui/icons-material/AccountCircle'

interface BottomNavigationItems {
  label: string;
  icon: React.ElementType;
  destination: string;
}

const bottomNavigationItems: BottomNavigationItems[] = [
  { label: 'Home', icon: HomeRoundedIcon, destination: '/' },
  { label: 'Profile', icon: AccountCircleIcon, destination: '/user/me' }
]

export default function BottomNavigationComponent() {
  const [value, setValue] = useState(0)
  const navigate = useNavigate()

  useEffect(() => {
    navigate(bottomNavigationItems[value].destination)
  }, [value])

  return (
    <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }} elevation={3}>
      <BottomNavigation
        showLabels
        value={value}
        onChange={(_, newValue) => {
          setValue(newValue)
        }}
      >
        {bottomNavigationItems.map((item, index) => (
          <BottomNavigationAction key={index} label={item.label} icon={<item.icon />} />
        ))}
      </BottomNavigation>
    </Paper>
  )
}
