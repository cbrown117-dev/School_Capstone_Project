import React, { Component } from "react";
import { connect } from "react-redux";

import LinearProgress from "@material-ui/core/LinearProgress";
import Switch from "@material-ui/core/Switch";
import Button from "@material-ui/core/Button";

import { fetchDevices, setDeviceState, setTimeInterval, getEventHistory } from "../actions";

import * as moment from "moment";

import { makeStyles } from '@material-ui/core/styles';

import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import TextField from '@material-ui/core/TextField';
import Snackbar from '@material-ui/core/Snackbar';

import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';

import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

import Toolbar from '@material-ui/core/Toolbar';
import AppBar from '@material-ui/core/AppBar';

var translation = {
    "microwave": "電子レンジ",
    "refrigerator": "冷蔵庫",
    "stove": "レンジ",
    "oven": "オーブン",
    "dishwasher": "食器洗い機",
    "kitchen_door": "キッチンドア",
    "kitchen_window": "キッチン窓",
    "main_hvac": "メイン",
    "garage_door": "ガレージのドア",
    "water_heater": "湯沸かし器",
    "living_room_tv": "リビングルームテレビ",
    "living_room_light": "リビングルームライト",
    "main_door": "メインドア",
    "livingroom_window": "リビングルーム窓",
    "Bedroom1_light": "ベッドルーム1ライト",
    "bedroom1_tv": "ベッドルーム1ライトテレビ",
    "bedroom1_window": "ベッドルーム1窓",
    "Bedroom2_light": "ベッドルーム2ライト",
    "bedroom2_tv": "ベッドルーム2ライト",
    "bedroom_window": "ベッドルーム2窓",
    "bathroom1_exhaust_fan": "浴室排気1ファン",
    "bathroom1_light": "浴室排気1",
    "bathroom1_bath_water_meter": "浴室排気1",
    "bathroom2_exhaust_fan": "浴室排気2ファン",
    "bathroom2_light": "浴室排気2ライト",
    "bathroom2_shower_water_meter": "浴室排気2水道メーター",
    "washer": "洗濯機",
    "washer_water_meter": "水道メーター",
    "dryer": "ドライヤー",
    "kitchen_light": "キッチンライト"
}

function DeviceItem(props) {

    let [state, setState] = React.useState({
        checked: props.device.state,
    });

    let handleDeviceStateChange = (dispatch, device) => {
        return event => {
            console.log(
                "Device state mutated for ID: " +
                device.deviceId +
                " setting to " +
                event.target.checked
            );
            let checked = event.target.checked;
            device.state = checked;
            setState({ ...state, checked: checked });
            dispatch(setDeviceState(device.deviceId, checked, moment().add(props.timeinterval.value, props.timeinterval.unit).toISOString()));
        };
    }


    return (
        // <Grid xs={12}>
        //   <Switch
        //         checked={state.checked}
        //         onChange={handleDeviceStateChange(
        //             props.dispatch,
        //             props.device
        //         )}
        //     />
        //     {props.device.state ? "ON" : "OFF"}
        // </Grid>

        <TableRow key={props.device.name}>
            <TableCell component="th" scope="row">
                {props.device.name} / {translation[props.device.name]}
            </TableCell>
            <TableCell align="right">
                <Switch
                    checked={state.checked}
                    onChange={handleDeviceStateChange(
                        props.dispatch,
                        props.device
                    )}
                />
            </TableCell>
        </TableRow>
    );
}

function DeviceList(props) {
    const timeinterval = props.timeinterval
    const dispatch = props.dispatch;
    const rawList = props.devicelist;

    const deviceList = rawList.map(device => {
        return (
            <DeviceItem
                timeinterval={timeinterval}
                dispatch={dispatch}
                device={device}
                key={device.deviceId}
            />
        );
    });

    return (
        <Table aria-label="simple table">

            <TableBody>
                {deviceList}
            </TableBody>
        </Table>
    );
}

const expansionStyles = makeStyles(theme => ({
    root: {
        width: '100%',
    },
    heading: {
        fontSize: theme.typography.pxToRem(15),
        fontWeight: theme.typography.fontWeightRegular,
    },
}));

function LocationList(props) {
    const classes = expansionStyles();
    const timeinterval = props.timeinterval
    const dispatch = props.dispatch;
    const rawList = props.locationList;

    const deviceList = rawList.map(location => {
        console.log(location)
        return (
            <Grid item xs={12} key={location.name}>
                <ExpansionPanel>
                    <ExpansionPanelSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography className={classes.heading}>{location.name}</Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails>
                        <DeviceList
                            key={location.name}
                            timeinterval={timeinterval}
                            dispatch={dispatch}
                            devicelist={location.devices}
                        />
                    </ExpansionPanelDetails>
                </ExpansionPanel>
            </Grid>
        );
    });

    return deviceList;
}

class IntervalSelector extends Component {
    constructor(props) {
        super(props)
        this.dispatch = this.props.dispatch
    }

    render() {
        return (
            <div>
                <Grid container spacing={0}>
                    <Grid item xs={6}>
                        <TextField
                            id="filled-number"
                            label="Number"
                            type="number"
                            InputLabelProps={{
                                shrink: true,
                            }}
                            margin="normal"
                            value={this.props.timeinterval.value}
                            onChange={(e) => {
                                this.dispatch(setTimeInterval(e.target.value, this.props.timeinterval.unit))
                            }}
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <InputLabel shrink id="demo-simple-select-placeholder-label-label">
                            Time Unit
                            </InputLabel>
                        <Select
                            labelId="demo-simple-select-placeholder-label-label"
                            id="demo-simple-select-placeholder-label"
                            value={this.props.timeinterval.unit}
                            onChange={(e) => {
                                this.dispatch(setTimeInterval(this.props.timeinterval.value, e.target.value))
                            }}
                        >
                            <MenuItem value={"minutes"}>Minutes</MenuItem>
                            <MenuItem value={"hours"}>Hours</MenuItem>
                        </Select>
                    </Grid>
                </Grid>
            </div>
        )
    }
}

class EventHistory extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <Table aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell align="right">Device Name</TableCell>
                        <TableCell align="right">State</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {this.props.eventHistory.map((event) => {
                        console.log("Mapping event " + event.device_name)
                        return (
                            <TableRow key={event.date}>
                                <TableCell align="right">{event.date}</TableCell>
                                <TableCell align="right">{event.device_name} / {translation[event.device_name]}</TableCell>
                                <TableCell align="right">{event.state}</TableCell>
                            </TableRow>
                        )
                    })}
                </TableBody>
            </Table>
        )
    }
}

class switchBoard extends Component {

    constructor(props) {
        super(props)
    }

    componentDidMount() {
        console.log("Component mounted, loading devices");

        const { dispatch } = this.props;
        dispatch(fetchDevices());
        dispatch(getEventHistory())
    }

    handleClose() {
        const { dispatch } = this.props;
        dispatch({
            type: "CLOSE_NOTIFICATION"
        });
    }

    render() {
        let loadingBar;

        if (this.props.devices.fetching) {
            loadingBar = <LinearProgress />;
        }

        return (
            <div className="swichboard">
                <Snackbar
                    anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                    open={this.props.notification.visible}
                    onClose={(e) => {
                        this.handleClose()
                    }}
                    ContentProps={{
                        'aria-describedby': 'message-id',
                    }}
                    message={this.props.notification.message}
                />

                {loadingBar}
                <Grid container spacing={3}>
                    <Grid item xs={6}>
                        <InputLabel shrink id="demo-simple-select-placeholder-label-label">
                            Time Interval
                        </InputLabel>
                        <IntervalSelector timeinterval={this.props.timeinterval} dispatch={this.props.dispatch}></IntervalSelector>
                    </Grid>

                    <Grid item xs={6}></Grid>

                    <Grid item xs={6}>
                        <AppBar position="static">
                            <Toolbar variant="dense">
                                <Typography variant="h6" >
                                    Switch History
                                </Typography>
                            </Toolbar>
                        </AppBar>

                    </Grid>

                    <Grid item xs={6}>
                        <AppBar position="static">
                            <Toolbar variant="dense">
                                <Typography variant="h6" >
                                    Device Switches
                                </Typography>
                            </Toolbar>
                        </AppBar>
                    </Grid>

                    <Grid item xs={6}>
                        <EventHistory eventHistory={this.props.event_history} />
                    </Grid>
                    <Grid item xs={6}>
                        <LocationList
                            timeinterval={this.props.timeinterval}
                            dispatch={this.props.dispatch}
                            locationList={this.props.devicelist}
                        />
                    </Grid>
                </Grid>
            </div>
        );
    }
}

//for every page you need a mapStateToProps for every component
const mapStateToProps = state => {
    return {
        notification: state.notification,
        timeinterval: state.timeinterval,
        age: state.age,
        oven: state.oven,
        frontDoor: state.frontDoor,
        devices: state.devices,
        devicelist: state.devices.list,
        event_history: state.event_history
    };
};

//
const mapDispatchToProps = dispatch => {
    return {
        TURNED_ON_OVEN: () => dispatch({ type: "OVEN_ON" }),
        TURNED_OFF_OVEN: () => dispatch({ type: "OVEN_OFF" }),
        dispatch: dispatch
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(switchBoard);
