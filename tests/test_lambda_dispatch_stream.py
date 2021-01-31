import boto3
import json
import moto
import unittest

from sqs_utils import SqsUtils


class TestDispatchStreamLambda(unittest.TestCase):

    @moto.mock_sts
    @moto.mock_sns
    @moto.mock_sqs
    def testRunWhenReceiveDynamoDBEvent(self):

        with open('resources/properties-dynamodb.json', 'r') as file:
            properties_dynamodb = json.load(file)

        with open('resources/properties-1.json', 'r') as file:
            expected_result = json.load(file)

        with open('resources/event-dynamodb-update.json', 'r') as file:
            event = json.load(file)

        event['Records'][0]['dynamodb']['NewImage'] = properties_dynamodb[0]
        event['Records'][1]['dynamodb']['NewImage'] = properties_dynamodb[1]

        topic = boto3.resource('sns').create_topic(Name='NewProperties')
        queue = boto3.resource('sqs').create_queue(QueueName='DummyQueue')
        boto3.client('sns').subscribe(
            TopicArn=topic.arn,
            Protocol='sqs',
            Endpoint=queue.attributes['QueueArn']
        )

        from dispatch_stream.core.handler import LAMBDA_HANDLER

        LAMBDA_HANDLER.run(event=event, context=None)

        messages = SqsUtils().receive_many(queue_name='DummyQueue', poll_for_seconds=0, max_batch_size=10)

        actual_result = [json.loads(json.loads(message)['Message']) for message in messages]

        self.assertListEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
