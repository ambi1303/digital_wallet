import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Box,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import {
  AccountCircle,
  Dashboard as DashboardIcon,
  AccountBalance as WalletIcon,
  ExitToApp as LogoutIcon,
} from '@mui/icons-material';

const Navigation: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleClose();
    logout();
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Digital Wallet
        </Typography>

        {user && (
          <>
            {isMobile ? (
              <>
                <IconButton
                  size="large"
                  edge="end"
                  color="inherit"
                  onClick={handleMenu}
                >
                  <AccountCircle />
                </IconButton>
                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                >
                  <MenuItem onClick={() => { handleClose(); navigate('/'); }}>
                    <DashboardIcon sx={{ mr: 1 }} /> Dashboard
                  </MenuItem>
                  <MenuItem onClick={() => { handleClose(); navigate('/deposit'); }}>
                    <WalletIcon sx={{ mr: 1 }} /> Deposit
                  </MenuItem>
                  <MenuItem onClick={() => { handleClose(); navigate('/withdraw'); }}>
                    <WalletIcon sx={{ mr: 1 }} /> Withdraw
                  </MenuItem>
                  <MenuItem onClick={() => { handleClose(); navigate('/transfer'); }}>
                    <WalletIcon sx={{ mr: 1 }} /> Transfer
                  </MenuItem>
                  <MenuItem onClick={handleLogout}>
                    <LogoutIcon sx={{ mr: 1 }} /> Logout
                  </MenuItem>
                </Menu>
              </>
            ) : (
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  color="inherit"
                  onClick={() => navigate('/')}
                  startIcon={<DashboardIcon />}
                >
                  Dashboard
                </Button>
                <Button
                  color="inherit"
                  onClick={() => navigate('/deposit')}
                  startIcon={<WalletIcon />}
                >
                  Deposit
                </Button>
                <Button
                  color="inherit"
                  onClick={() => navigate('/withdraw')}
                  startIcon={<WalletIcon />}
                >
                  Withdraw
                </Button>
                <Button
                  color="inherit"
                  onClick={() => navigate('/transfer')}
                  startIcon={<WalletIcon />}
                >
                  Transfer
                </Button>
                <Button
                  color="inherit"
                  onClick={handleLogout}
                  startIcon={<LogoutIcon />}
                >
                  Logout
                </Button>
              </Box>
            )}
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navigation; 