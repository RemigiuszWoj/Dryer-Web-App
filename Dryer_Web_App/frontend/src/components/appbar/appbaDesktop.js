
import { AppBar } from "@mui/material";
import React, { Component } from "react";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link } from "react-router-dom";


import HotTubIcon from '@mui/icons-material/HotTub';
import HomeIcon from '@mui/icons-material/Home'
import LocalOfferIcon from '@mui/icons-material/LocalOffer'
import ListAltIcon from '@mui/icons-material/ListAlt'
import ContactPhoneIcon from '@mui/icons-material/ContactPhone';


function appBarLabel(label) {
    return (
      <Toolbar >
        <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          {label}
        </Typography>
      </Toolbar>
    );
  }

const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

const darkTheme = createTheme({
    palette: {
      mode: 'dark',
      primary: {
        main: '#1976d2',
      },
    },
  });

export default function AppBarDesktop( { mathes }) {

    return (
        <div> 
            <div>
                <ThemeProvider theme={darkTheme}>
                    <AppBar color="primary">
                        <Toolbar >
                            <IconButton
                                color="inherit"
                                aria-label="open drawer"
                                edge="start"
                                onClick={handleDrawerToggle}
                                sx={{ mr: 2, display: { sm: 'none' } }}
                            >
                                <MenuIcon />
                            </IconButton>
                            <Typography
                                    variant="h6"
                                    component="div"
                                    sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
                                >
                                    Dryer Web App
                                    <HotTubIcon />
                                        <Button sx={{ color: '#fff' }} endIcon={<HomeIcon />}>
                                            Home Page
                                        </Button> 
                                        <Button sx={{ color: '#fff' }} endIcon={<LocalOfferIcon />}>
                                            Ofer
                                        </Button>
                                        <Button sx={{ color: '#fff' }} endIcon={<ListAltIcon />}>
                                            Order
                                        </Button>
                                        <Button sx={{ color: '#fff' }} endIcon={<ContactPhoneIcon />}>
                                            Contact
                                        </Button>

                                </Typography>
                        </Toolbar>
                    </AppBar>
                </ThemeProvider>
                
            </div>

        </div>
    );

}