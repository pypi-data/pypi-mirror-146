from typing import Dict, List, Optional, Literal
from datetime import datetime


def get_example_event_json(subject: str, message: str, message_attributes: dict = None):
    """Helper method to generate example events given a message and a subject"""
    if not message:
        message = "example message"
    if not subject:
        subject = "example subject"
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:us-east-1::privateapi",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                    "TopicArn": "arn:aws:sns:us-east-1:12345678912:privateapi",
                    "Subject": subject,
                    "Message": message,
                    "Timestamp": "1970-01-01T00:00:00.000Z",
                    "SignatureVersion": "1",
                    "Signature": "Tb9Y/BZnBDbDwqj3yEOnjHuuIulXDHKZgHo3VT8bClqHwglWMBABnWOfUFFsJWaQLWRE8MIDPWSr0IR0gVHpTicmA9XWpMGhLy0KBnWuRF/FEQU886SdZz3TJW94lX1vGDZFJX6LA8ZpwQFJ69bVf2WemSCcPnzPFaVnSp+2W4fTMRIreRwGvAQW1HSHObowmRqtSz7ZBmDFRjyF9wuPte0KyWwJh9m9Z/zhIFkJfNUBMM+hSafxVqVUrHKcSO1vnAi7eFeIzJzpQHiXaZEKCmPMD4NVAeuqF3CHjfbd6n4Jwe1dcVP+o69fuXyADqrV1kGtHpLBAlGk9MRyIeWWoQ==",
                    "SigningCertUrl": "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:12345678912:powertools265:5e4c8d5d-383c-4aa1-90aa-d849f068e7dc",
                    "MessageAttributes": {
                        "Test": {
                            "DataType": "String",
                            "StringValue": "TestString"
                        }
                    }
                }
            }
        ]
    }
    if message_attributes:
        event["Records"][0]["Sns"]["MessageAttributes"] = message_attributes
    return event


def get_message_attributes_dict(string: str = None) -> dict:
    """Given a string, return the dictionary representation of the SNS message attribute"""
    return {"DataType": "String", "StringValue": string}


def translate_dict_to_message_attributes(kv_pair: dict) -> dict:
    results = {}
    for key, value in kv_pair.items():
        results[key] = get_message_attributes_dict(string=value)
    return results

