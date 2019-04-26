# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# import random
import time
import sys
import nfc
import json
# pylint: disable=E0611
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider, DeviceMethodReturnValue
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT

# Callback received when the message that we're forwarding is processed.
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )


def send_reported_state_callback(status_code, hubManager):
    print ( "" )
    print ( "Confirmation for reported state called with:" )
    print ( "    status_code: %d" % status_code )


def module_twin_callback(update_state, payload, hubManager):
    print ( "" )
    print ( "Twin callback called with:" )
    print ( "    updateStatus: %s" % update_state )
    print ( "    payload: %s" % payload )


def module_method_callback(method_name, payload, hubManager):
    print('received method call:')
    print('\tmethod name:', method_name)
    print('\tpayload:', str(payload))
    retval = DeviceMethodReturnValue()
    retval.status = 200
    retval.response = "{\"key\":\"value\"}"
    return retval


def run_nfc_once(hubManager):
    try:
        clf = nfc.ContactlessFrontend('usb')
        rdwr_options = {
            'on-startup': hubManager.on_rdwr_startup,
            'on-connect': hubManager.on_rdwr_connect}

        result = clf.connect(rdwr=rdwr_options)

        state = {'nfc': {'is_connected': False}}
        hubManager.forward_event_to_output(state, 0)

        return result
    finally:
        clf.close()


class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)

        self.client.set_module_method_callback(module_method_callback, self)
        self.client.set_module_twin_callback(module_twin_callback, self)

    def run(self):
        while run_nfc_once(self):
            print ( "** RESTERT **" )

    # Forwards the message received onto the next stage in the process.
    def forward_event_to_output(self, event, send_context):
        if type(event) != 'str':
            event = json.dumps(event)
        message = IoTHubMessage(event)

        self.client.send_event_async(
            'nfcaccessor', message, send_confirmation_callback, send_context)

    def send_reported_state(self, reported_state):
        reported_state = json.dumps(reported_state)
        self.client.send_reported_state(
             reported_state, len(reported_state),
             send_reported_state_callback, self)

    def on_rdwr_startup(self, targets):
        return targets

    def on_rdwr_connect(self, tag):
        print ( tag )
        state = {'nfc': {
            'is_connected': True,
            'tag': {
                'product': tag.product,
                'id': tag.identifier.encode("hex").upper()}}}
        self.forward_event_to_output(state, 0)
        return tag


def main(protocol):
    try:
        print ( "\nPython %s\n" % sys.version )
        print ( "IoT Hub Client for Python" )

        hub_manager = HubManager(protocol)
        hub_manager.run()

        print ( "Starting the IoT Hub Python sample using protocol %s..." %hub_manager.client_protocol )
        print ( "The sample is now waiting for messages and will indefinitely.  Press Ctrl-C to exit. ")

        while True:
            time.sleep(1)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubModuleClient sample stopped" )

if __name__ == '__main__':
    main(PROTOCOL)
