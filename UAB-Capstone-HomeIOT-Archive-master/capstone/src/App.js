import React, {Fragment} from 'react';
import { BrowserRouter as Router, Route, Switch} from 'react-router-dom';

// Redux
import { useSelector, useDispatch } from 'react-redux'; //connects global state (store) to our app
import { connect } from 'react-redux';
import './App.css';

//these are the exported functions that are called from below 
import Dashboard from './components/dashboard';
import switchBoard from './components/switchboard';
import stats from './components/stats';

//Material components
import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from './components/AppBar';

const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1),
  },
  input: {
    display: 'none',
  },
}));

//main
function App() {

  //useSelector(state => state.any reducer that is in your combineReducer function in your reducer folder(located in index.js))
  //useDispatch() allows us to call functions from the actions folders that are in index.js

  const counter = useSelector(state => state.counterReducer);
  const dispatch = useDispatch();                      
  
  //***** keep in mind anything in the return() is rendered, even comments ***** //

  const classes = useStyles();
  //so dispatch is called with the increment() that is in the actions index.js
  //same for decrement()
  return (
      <Container fixed>
        <AppBar/>
        <br/>
        <br/>       
        <br/>
        <br/>
        <br/>
        <br/>       
        <br/>
        <br/>
        <Router>
        <Fragment>
          <Switch>
            <Route exact path ='/' component={Dashboard} />
            <Route exact path ='/switchBoard' component={switchBoard} />
            <Route exact path ='/stats' component={stats} />
          </Switch>
        </Fragment>
      </Router>

      </Container>
  );
}




export default (App);
