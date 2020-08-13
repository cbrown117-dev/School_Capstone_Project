import React, { Fragment, useState, useEffect, Component } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Chart from 'react-apexcharts'

import { makeStyles, withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import Checkbox from '@material-ui/core/Checkbox';

import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Box from '@material-ui/core/Box';


import MomentUtils from '@date-io/moment';
import { MuiPickersUtilsProvider } from '@material-ui/pickers';
import { DatePicker } from "@material-ui/pickers";
import * as moment from 'moment';
import API from '../services/api';

//TODO: Round numbers
//TODO: Change date picker to true month instead of going back one

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <div>{children}</div>}
    </Typography>
  );
}

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));

class YearMonthPicker extends Component {

  handleDateChange = (date) => {
    this.setState({ date });
    this.props.onDateChanged(date)
  };

  constructor(props) {
    super(props)

    console.log("Datepicker set props mindate " + this.props.minDate)
    this.state = { date: Date.now(), minDate: this.props.minDate, maxDate: this.props.maxDate };

  }

  render() {
    return (
      <Fragment>
        <DatePicker
          openTo="month"
          views={["year", "month"]}
          label="Year and Month"
          helperText="Choose month"
          minDate={this.props.minDate}
          maxDate={this.props.maxDate}
          value={this.state.date}
          onChange={this.handleDateChange}
        />
      </Fragment>
    );
  }
}

class UsageGraph extends Component {

  constructor(props) {
    super(props);

    this.state = {
      options: {
        stroke: {
          curve: 'smooth'
        },
        markers: {
          size: 0
        },
        xaxis: {
          type: 'datetime',
        },
        title: {
          text: props.title,
          align: 'center',
          margin: 10,
          offsetX: 0,
          offsetY: 0,
          floating: false,
          style: {
            fontSize: '20px',
            color: '#263238'
          },
        },
        yaxis: {
          labels: {
            formatter: function(val) {
              return val.toFixed(2)
            }
          }
      }
      }
    }
  }

  render() {

    return (
      <div className="line">
        <Chart options={this.state.options} series={this.props.series} type="line" width="100%" />
      </div>
    );
  }
}

class StatsPage extends Component {

  constructor(props) {
    super(props);

    this.state = {
      tab: 0,
      showrunningtotals: true,
      generating: false,
      jpyusd: 1,
      minDate: new Date(),
      maxDate: new Date(),
      selected_date: new Date(),
      usagedata: {
        electricity: {
          kwh: 10,
        },
        water: {
          gallons: 0,
        },
        eom_predictions: {
          water: 0,
          electricity: 0,
        },
        average_daily: {
          electricity: 0,
          water: 0,
        }
      },
      graph: [
        {
          data: []
        },
        {
          data: []
        },
        {
          data: []
        },
        {
          data: []
        }
      ]
    }
  }

  getUSDJPYConversion() {
    let endpoint = "http://data.fixer.io/api/latest?access_key=95a9d4132546bd3bff1c0750a4d33775"

    fetch(endpoint)
      .then(response => response.json())
      .then(data => {
        this.state.jpyusd = data["rates"]["JPY"]
        this.setState(this.state)
      })
      .catch(err => {
        this.state.jpyusd = 108.72
        this.setState(this.state)
      });
  }

  componentDidMount() {
    this.getUSDJPYConversion()
    this.loadStatistics(new Date())
  }

  kwh_to_dollars = (kwh) => kwh * 0.12
  ft3_to_dollars = (ft3) => {
    let gals = (2.52 / 100) * ft3
    console.log(gals)
    return gals
  }
  calculate_current_cost = () => this.kwh_to_dollars(this.state.usagedata.electricity.kwh) + this.ft3_to_dollars(this.state.usagedata.water.gallons)
  calculate_estimated_cost = () => this.kwh_to_dollars(this.state.usagedata.eom_predictions.electricity) + this.ft3_to_dollars(this.state.usagedata.eom_predictions.water)

  mainGraphFilterHandler() {
    console.log(this.state.graph)
    console.log("THINGS CHANGING HERE")
    if (this.state.showrunningtotals) {
      return this.state.graph
    }
    else {
      return this.state.graph.filter(el => {
        return !el.rtot
      })
    }

  }

  generateNextDay() {
    API.get(`usage/generate_next`)
      .then(
        response => response.data,
        error => console.log('An error occurred.', error)
      )
      .then(json => {
        this.setState({ generating: false })
        this.loadStatistics(new Date())
      })
  }

  // Handle month change events
  loadStatistics(date) {
    console.log(date)

    let currdate = moment(date).startOf('month')
    let isostring = currdate.format("YYYY-MM-DD")

    console.log("LOADING STATISTICS FOR " + date)

    API.get(`usage/usagestats?start=${isostring}`)
      .then(
        response => response.data,
        error => console.log('An error occurred.', error)
      )
      .then(json => {
        console.log(json)
        let stats = json.stats
        let graphing = json.graphing
        let temphistory = json.temphistory


        this.setState({
          tab: this.state.tab,
          generating: this.state.generating,
          jpyusd: this.state.jpyusd,
          minDate: moment(json.range.start),
          maxDate: moment(json.range.end),
          selected_date: this.state.selected_date,
          usagedata: {
            electricity: {
              kwh: stats.totals.electricity,
            },
            water: {
              gallons: stats.totals.water,
            },
            eom_predictions: {
              water: graphing.month_end_predict.water,
              electricity: graphing.month_end_predict.electric,
            },
            average_daily: {
              electricity: stats.dailyaverage.electricity,
              water: stats.dailyaverage.water,
            }
          },
          graph: [
            {
              name: 'Daily Electric (kWh)',
              data: graphing.electric.raw,
            },
            {
              name: 'Daily Water (ft^3)',
              data: graphing.water.raw,
            },
            {
              rtot: true,
              name: 'Electric Running Total',
              data: graphing.electric.runningtotal,
            },
            {
              rtot: true,
              name: 'Water Running Total',
              data: graphing.water.runningtotal,
            }
          ],
          temphistory: [
            {
              name: 'Internal Temp (°F)',
              data: temphistory.internal,
            },
            {
              name: 'External Temp (°F)',
              data: temphistory.external,
            },
          ]
        });
      })

  }

  render() {
    const { classes } = this.props;
    const current_cost = this.calculate_current_cost()
    const predicted_cost = this.calculate_estimated_cost()


    return (
      <div className={classes.root}>
        <Grid container spacing={3}>

          <Grid item xs={3}>
            <Paper className={classes.paper}>
              <MuiPickersUtilsProvider utils={MomentUtils}>
                <YearMonthPicker minDate={this.state.minDate} maxDate={this.state.maxDate} onDateChanged={(e) => this.loadStatistics(e)}></YearMonthPicker>
              </MuiPickersUtilsProvider>
            </Paper>
          </Grid>

          <Grid item xs={3}>
            <Paper className={classes.paper}>
              <Typography variant="h5" component="h3">
                Electricity / 電
              </Typography>
              <Typography variant="h5" component="p">
                {Math.round(this.state.usagedata.electricity.kwh * 100) / 100} kWh
            </Typography>
            </Paper>
          </Grid>

          <Grid item xs={3}>
            <Paper className={classes.paper}>
              <Typography variant="h5" component="h3">
                Water / 水
            </Typography>
            <Typography variant="h5" component="p">
                {Math.round(this.state.usagedata.water.gallons * 100) / 100} ft^3
            </Typography>
            </Paper>
          </Grid>

          <Grid item xs={3}>
            <Paper className={classes.paper}>
              <Typography variant="h5" component="h3">
                Total Cost To Date
            </Typography>
              <Typography component="p">
                ${Math.round(current_cost * 100) / 100} / ¥{Math.round((current_cost * this.state.jpyusd) * 100) / 100}
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={3}>
            <Paper className={classes.paper}>
              <Typography variant="h5" component="h3">
                Data Generation
            </Typography>

              <Grid container spacing={12}>

                <Grid item xs={8}>
                  <Typography component="p">
                    <Button variant="contained" disabled={this.state.generating} color="primary" onClick={(e) => {
                      this.setState({ generating: true })

                      this.generateNextDay()
                    }
                    }>
                      Generate Next Day
                  </Button>
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  {this.state.generating && <CircularProgress color="secondary" />}
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          <Grid item xs={3}>
            <Paper className={classes.paper}>
              <Typography variant="h5" component="h3">
                Estimated Month Total
            </Typography>
            <Typography variant="h5" component="p">
                ${Math.round(predicted_cost * 100) / 100}
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={3}>
            <Paper className={classes.paper}>
              <Typography variant="h5" component="h3">
                Avg. Daily Electric
              </Typography>
              <Typography variant="h5" component="p">
                {Math.round(this.state.usagedata.average_daily.electricity * 100) / 100} kWh
            </Typography>
            </Paper>
          </Grid>

          <Grid item xs={3}>
            <Paper className={classes.paper}>
              <Typography variant="h5" component="h3">
                Avg. Daily Water
              </Typography>
              <Typography variant="h5" component="p">
                {Math.round(this.state.usagedata.average_daily.water * 100) / 100} ft^3
            </Typography>
            </Paper>
          </Grid>


          <Grid item xs={12}>
            <AppBar position="static">
              <Tabs centered value={this.state.tab} onChange={(e, newvalue) => {
                this.setState({ tab: newvalue })
              }} aria-label="simple tabs example">
                <Tab label="Utility Usage" />
                <Tab label="Temperature" />
              </Tabs>
            </AppBar>
            <TabPanel value={this.state.tab} index={0}>
              <Grid item xs={12}>
                <Grid item xs={2}>
                  <Paper className={classes.paper}>
                    <Checkbox
                      checked={this.state.showrunningtotals}
                      onChange={(e) => {
                        console.log(e.target.checked)
                        this.setState({ ...this.state, showrunningtotals: e.target.checked });
                      }}
                      value="showrunningtotals"
                      inputProps={{
                        'aria-label': 'Show Running Totals',
                      }}
                    /> Show Running Total
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                  <Paper className={classes.paper}>
                    <UsageGraph title="Power & Water Usage" series={this.mainGraphFilterHandler()} />
                  </Paper>
                </Grid>
              </Grid>
            </TabPanel>
            <TabPanel value={this.state.tab} index={1}>
               <Grid item xs={12}>
                <Grid item xs={12}>
                  <Paper className={classes.paper}>
                    <UsageGraph title="Temperature History" series={this.state.temphistory} />
                  </Paper>
                </Grid>
              </Grid>
            </TabPanel>
          </Grid>
        </Grid>
      </div >
    );
  }
}


export default withStyles(useStyles)(StatsPage)