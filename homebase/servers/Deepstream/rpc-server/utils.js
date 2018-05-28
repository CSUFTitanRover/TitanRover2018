const {
    ADD_COORDINATE,
    DELETE_ALL_COORDINATES,
    DELETE_COORDINATE,
    POP_COORDINATE,
    JOINT_1_ADDRESS,
    JOINT_4_ADDRESS,
    JOINT_51_ADDRESS,
    JOINT_52_ADDRESS,
    HIGH_SPEED,
    LOW_SPEED
} = require('./constants');

function createDataString(action, data) {
    switch (action) {
        case ADD_COORDINATE:
            return `${action},${data}`
        case DELETE_ALL_COORDINATES:
            return `${action}`
        case DELETE_COORDINATE:
            return `${action},${data}`
        case POP_COORDINATE:
            return `${action}`
        default:
            // catch-all for actions that don't have a 
            // designated action symbol
            return `${action},${data}`
    }
}

function getJointNameFromAddress(address) {
    switch (address) {
        case JOINT_1_ADDRESS:
            return 'Joint 1'
        case JOINT_4_ADDRESS:
            return 'Joint 4'
        case JOINT_51_ADDRESS:
            return 'Joint 5.1'
        case JOINT_52_ADDRESS:
            return 'Joint 5.2'
    }
}

function getSpeedNameFromValue(value) {
    switch (value) {
        case HIGH_SPEED:
            return 'High'
        case LOW_SPEED:
            return 'Low'
    }
}

module.exports = {
    createDataString,
    getJointNameFromAddress,
    getSpeedNameFromValue
}