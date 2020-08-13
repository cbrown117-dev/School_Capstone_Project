import {
    DEVICE_STATE_CHANGE,
    GET_DEVICES,
    GET_HVAC_SETTINGS,
    SET_HVAC_TEMP,
    TIME_INTERVAL_CHANGE,
    GET_EVENT_HISTORY,
} from '../actions'

const convertLocationDeviceArray = (devicesWithStateMappedToBoolean) => {
    return devicesWithStateMappedToBoolean.reduce((acc, location) => {
        let dlist = []
        location.devices.map(device => {
            dlist.push(device)
        })
        acc = acc.concat(dlist)
        return acc
      }, [])
}

const reducer = (state, action) => {
    const newState = { ...state };

    switch (action.type) {
        case GET_EVENT_HISTORY:
            console.log("GET EVENT HISTORY STATE UPDATE")
            console.log(action.event_history)
            return {
                ...state,
                event_history: action.event_history
            }
        case GET_HVAC_SETTINGS:
            return {
                ...state,
                hvac: action.settings
            }
        case GET_DEVICES:

            if (action.devices) state.devices.list = action.devices

            let devicesWithStateMappedToBoolean = state.devices.list.map((locationdevices) => {
                locationdevices.devices = locationdevices.devices.map((el) => {
                    if (el.state === "ON") {
                        el.state = true
                    } else {
                        el.state = false
                    }
                    return el
                })
                return locationdevices
            })

            let rawdevicelist = convertLocationDeviceArray(devicesWithStateMappedToBoolean)

            console.log("RAW DEVICE LIST")

            console.log(rawdevicelist)

            return {
                ...state,
                devices: {
                    fetching: action.fetching,
                    list: devicesWithStateMappedToBoolean
                },
                rawdevicelist: rawdevicelist
            }
        case DEVICE_STATE_CHANGE:
            let mutatedDevice = action.device
            let currDevices = state.devices

            let newDeviceState = mutatedDevice.state === "ON" ? true : false;

            console.log(mutatedDevice)

            let deviceMapped = state.devices.list.map(device =>
                device.deviceId === mutatedDevice.deviceId ? { ...device, state: newDeviceState } : device
            )

            if (mutatedDevice.geninfo) {
                return {
                    ...state,
                    devices: {
                        fetching: false,
                        list: deviceMapped
                    },
                    rawdevicelist: convertLocationDeviceArray(deviceMapped),
                    notification: {
                        visible: true,
                        message: "Device turned on and will use " + Math.round(mutatedDevice.geninfo.usage * 100) / 100 + " kWh"
                    }
                }
            } else {
                return {
                    ...state,
                    devices: {
                        fetching: false,
                        list: deviceMapped
                    },
                    rawdevicelist: convertLocationDeviceArray(deviceMapped),
                }
            }
        case "CLOSE_NOTIFICATION":
            return {
                ...state,
                notification: {
                    visible: false,
                    message: ""
                }
            }
        case TIME_INTERVAL_CHANGE:
            let value = action.value
            let unit = action.unit
            return {
                ...state,
                timeinterval: {
                    value: value,
                    unit: unit
                }
            }

        /* HERE ************** */
        case SET_HVAC_TEMP:
            return {
                ...state,
                hvac: action.device
            }

        default:
            return newState;
    }

};

export default reducer; 