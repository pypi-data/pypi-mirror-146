import json
import logging

import boto3
from botocore.exceptions import ClientError
from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model

QUEUE_NAME = config("AWS_SQS_QUEUE_NAME", default=None)
AWS_REGION = getattr(settings, "AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = getattr(settings, "AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = getattr(settings, "AWS_SECRET_ACCESS_KEY", None)
APP_UNIQUE_CODE = getattr(settings, "APP_UNIQUE_CODE", None)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_client():
    """
    Get a boto3 client for SQS
    """
    return boto3.client(
        "sqs",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def get_queue_url():
    """
    Get the URL of our SQS queue
    """
    sqs_client = get_client()

    try:
        response = sqs_client.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]
    except ClientError as e:
        logger.exception(e)
        raise

    return response


def create_user_notification(index_name: str, user_data: dict):
    """
    Create a message in our SQS queue
    """

    sqs_client = get_client()
    queue_url = get_queue_url()

    msg_body = {"index": index_name, "user_data": user_data}

    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(msg_body),
        )
    except ClientError as e:
        logger.exception(e)
        raise

    json_msg = json.dumps(response, indent=4)

    logger.info(
        (
            f"""
        Message sent to the queue {queue_url}.
        Message attributes: \n{json_msg}"""
        )
    )


def read_queue_messages(max_messages=120):
    """
    Read messages from our SQS queue
    """

    sqs_client = get_client()
    queue_url = get_queue_url()

    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=20,
        )
    except ClientError as e:
        logger.exception(e)
        raise

    json_msg = json.dumps(response, indent=4)

    logger.info(
        (
            f"""
        Messages received from the queue {queue_url}.
        Message attributes: \n{json_msg}"""
        )
    )

    return response


def delete_message(receipt_handle):
    """
    Delete a message from our SQS queue
    """

    sqs_client = get_client()
    queue_url = get_queue_url()

    try:
        response = sqs_client.delete_message(
            QueueUrl=queue_url, ReceiptHandle=receipt_handle
        )
    except ClientError as e:
        logger.exception(e)
        raise

    json_msg = json.dumps(response, indent=4)

    logger.info(
        (
            f"""
        Message deleted from the queue {queue_url}.
        Message attributes: \n{json_msg}"""
        )
    )


def process_messages_queue():
    messages = read_queue_messages()

    for msg in messages["Messages"]:
        try:
            msg_body = json.loads(msg["Body"])
        except json.decoder.JSONDecodeError as e:
            logger.exception(e)
            delete_message(msg["ReceiptHandle"])
            continue

        index_name = msg_body["index"]
        user_data = msg_body["user_data"]

        if index_name == APP_UNIQUE_CODE:
            User = get_user_model()

            User.objects.update_or_create(**user_data)

            delete_message(msg["ReceiptHandle"])
