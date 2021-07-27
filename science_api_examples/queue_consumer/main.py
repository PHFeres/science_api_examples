import json
import logging
from configparser import ConfigParser

from science_api.sqs.sqs_base import SqsBase


if __name__ == '__main__':
    '''
    Runs a objects to keep checking the sqs queue to run the API and post the result
    '''

    settings_path = './settings.cfg'
    parser = ConfigParser()
    parser.read(settings_path)

    sqs_setup = {
        'aws_region': parser.get('sqs_info', 'AWS_REGION'),
        'send_url': parser.get('sqs_info', 'SEND_URL'),
        'receive_url': parser.get('sqs_info', 'RECEIVE_URL'),
        'aws_access_key': parser.get('credentials', 'AWS_ACCESS_KEY_ID'),
        'aws_secret_key': parser.get('credentials', 'AWS_SECRET_ACCESS_KEY'),
    }

    s3_setup = {
        's3_access_key': parser.get('s3_aws_credentials', 'AWS_ACCESS_KEY_ID'),
        's3_secret_key': parser.get('s3_aws_credentials', 'AWS_SECRET_ACCESS_KEY'),
        's3_region': parser.get('s3_aws_credentials', 'AWS_REGION'),
        's3_bucket': parser.get('s3_aws_credentials', 'S3_BUCKET'),
        's3_input_folder': parser.get('s3_aws_credentials', 'INPUT_FOLDER'),
        's3_output_folder': parser.get('s3_aws_credentials', 'OUTPUT_FOLDER'),
    }

    watcher_setup = {
        'url': parser.get('post_info', 'URL'),
        'test_url': parser.get('post_info', 'TEST_URL')
    }

    sqs_api = SqsBase(region=sqs_setup['aws_region'],
                      aws_access_key=sqs_setup['aws_access_key'],
                      aws_secret_key=sqs_setup['aws_secret_key'],
                      send_queue_url=sqs_setup['send_url'],
                      receive_queue_url=sqs_setup['receive_url'])

    server_watcher = SqsWatcherDirect(
        post_url=watcher_setup['url'],
        io_class=SchedulerIO,
        sqs_api=sqs_api,
        test_post_url=watcher_setup['test_url'],
        logger=logging,
        s3_aws=s3_setup)

    server_watcher.run(test=False, json_data=None)
