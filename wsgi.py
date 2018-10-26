from flask import Flask
from flask.logging import default_handler

import os
import logging

import s3
import producer

application = Flask(__name__)

ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.setLevel(application.logger.level)
ROOT_LOGGER.addHandler(default_handler)

@application.route("/", methods=['GET', 'POST']) # using 'GET' temporarily to trigger the microservice by hitting the route in the browser
def wake_up():
    server = os.environ.get('KAFKA_SERVER')
    topic = os.environ.get('KAFKA_TOPIC')

    aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_bucket = os.environ.get('AWS_S3_BUCKET_NAME')

    application.logger.info('Saving data to bucket %s', aws_bucket)
    filesystem = s3.connect(aws_key, aws_secret)
    s3.save_data(filesystem, aws_bucket, "Data going to bucket")

    application.logger.info('Publishing message "data_available" on topic %s', topic)
    producer.publish_message(server, topic, 'data_available')
    return 'aiops-publisher activated!'

if __name__ == '__main__':
    application.run()
