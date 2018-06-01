const { getClient, getRecord } = require('../common/deepstream');

async function main() {
    let elapsedTime = 0;
    let interval = null;
    const client = await getClient('homebase');
    const stopwatchRecord = await getRecord(client, 'homebase/stopwatch');

    client.event.subscribe('homebase/stopwatch:start', () => {
        if (!interval) {
            interval = setInterval(() => {
                elapsedTime += 1;
                stopwatchRecord.set({ elapsedTime, active: true });
            }, 1000)
        }
    });

    client.event.subscribe('homebase/stopwatch:stop', () => {
        clearInterval(interval);
        interval = null;
        stopwatchRecord.set('active', false);
    });

    client.event.subscribe('homebase/stopwatch:clear', () => {
        clearInterval(interval);
        interval = null
        elapsedTime = 0
        stopwatchRecord.set({ elapsedTime, active: false });
    });
}

main();