'use strict';

const Transport = require('azure-iot-device-mqtt').Mqtt;
const Client = require('azure-iot-device').ModuleClient;
const Message = require('azure-iot-device').Message;

// This function just pipes the messages without any change.
const pipeMessage = (client, inputName, msg) => {
  client.complete(msg, printResultFor('Receiving message'));

  const message = msg.getBytes().toString('utf8');
  console.log(message);

  if (inputName === 'nfcaccessor') {
    const messageBody = JSON.parse(message);
    const patch = messageBody;

    client.getTwin((err, twin) => {
      if (err) throw err;
      twin.properties.reported.update(patch, twinReportedCallback);
    });
  } else {
    const outputMsg = new Message(message);
    client.sendOutputEvent('output1', outputMsg, printResultFor('Sending received message'));
  }
}

const twinReportedCallback = (err) => {
  if (err) {
    throw err;
  }
  console.log('Twin state reported');
}

// Helper function to print results in the console
const printResultFor = (op) => {
  return printResult = (err, res) => {
    if (err) {
      console.log(op + ' error: ' + err.toString());
    }
    if (res) {
      console.log(op + ' status: ' + res.constructor.name);
    }
  };
}

// Executor
const run = async () => {
  try {
    const client = await Client.fromEnvironment(Transport);
    await client.open();
    console.log('IoT Hub module client initialized');

    // Act on input messages to the module.
    client.on('inputMessage', function (inputName, msg) {
      pipeMessage(client, inputName, msg);
    });

  } catch(err) {
    console.log(err);
  }
}

run();
