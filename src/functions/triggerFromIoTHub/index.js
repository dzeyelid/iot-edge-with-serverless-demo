module.exports = async function (context, eventHubMessages) {
    context.log(`JavaScript eventhub trigger function called for message array ${eventHubMessages}`);

    context.bindings.signalRMessages = [{
        "target": "newMessage",
        "arguments": [ eventHubMessages ]
    }];
};