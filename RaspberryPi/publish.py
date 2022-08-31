# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import schedule
import time as t
import json

import ADC0832
import time

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "atxonn7h8olt2-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "../certs/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.pem.crt"
PATH_TO_PRIVATE_KEY = "../certs/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "../certs/AAAAAAAAAAAAAAA.pem"
MESSAGE = "analog value"
TOPIC = "pub/moisture"


def job():
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=ENDPOINT,
                cert_filepath=PATH_TO_CERTIFICATE,
                pri_key_filepath=PATH_TO_PRIVATE_KEY,
                client_bootstrap=client_bootstrap,
                ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
                client_id=CLIENT_ID,
                clean_session=False,
                keep_alive_secs=6
                )
    print("Connecting to {} with client ID '{}'...".format(
            ENDPOINT, CLIENT_ID))
    # Make the connect() call
    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    # Publish message to server desired number of times.
    print('Begin Publish')
    ADC0832.setup()
    # data = "{} [{}]".format(MESSAGE, i+1)
    res = ADC0832.getResult()
    moistureValue = 255 - res;
    message = {"moistureValue" : moistureValue}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'pub/moisture'")
    t.sleep(5)
    print('Publish End')
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()

# 実行間隔を登録
schedule.every().day.at("07:00").do(job) 
schedule.every().day.at("19:00").do(job)

# 登録した時間になったらjob関数を実行
while True:
    schedule.run_pending()
    time.sleep(1)
  


