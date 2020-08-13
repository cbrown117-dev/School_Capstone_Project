import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';

import Typography from '@material-ui/core/Typography';

import BugsDialog from './BugsDialog'

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

export default function ButtonAppBar() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="fixed" style={{ margin: 0}}>
        <Toolbar>
        <img src={require('../images/logo.png')} alt="Logo" height="100px"/>
        <Typography variant="h6" className={classes.title}>
            HomeIOT
        </Typography>
          <Button color='inherit' to='/' href='/'>Dashboard</Button>
          <Button color="inherit" to='/stats' href='/stats'>Stats </Button>
          <Button color="inherit" to='/switchboard' href='/switchboard'>Switch Board </Button>
          <BugsDialog/>
        </Toolbar>
      </AppBar>
    </div>
  );
}