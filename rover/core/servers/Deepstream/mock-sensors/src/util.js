const yaml = require('js-yaml')
const fs = require('fs')

function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min; //The maximum is inclusive and the minimum is inclusive 
}

function getRandomFloatInclusive(min, max) {
    let r = Math.random() < 0.5 ? ((1-Math.random()) * (max-min) + min) : (Math.random() * (max-min) + min);
    return r.toFixed(4) // round to 4 decimal places
}

function getDeepstreamEndpoints() {
    try {
        const mockConfig = yaml.safeLoad(fs.readFileSync('./mockConfig.yml', 'utf8'))
        return mockConfig.deepstream
    }
    catch (e) {
        console.error(e)
    }
}

module.exports = {
    getRandomFloatInclusive,
    getRandomIntInclusive,
    getDeepstreamEndpoints
}