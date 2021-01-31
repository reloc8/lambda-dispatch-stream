import json
import logging
from dataclasses import dataclass
from typing import Any, AnyStr, Dict, List

from dynamodb_utils import DynamoDBUtils
from sns_utils import SnsUtils


@dataclass(init=False)
class DispatchStreamLambdaCore:

    logger: logging.Logger

    def __init__(self, logger: logging.Logger):

        self.dynamodb_utils = DynamoDBUtils(logger=logger)
        self.sns_utils = SnsUtils(logger=logger)

    def load_dynamodb_objects(self, dynamodb_objects: List[Dict[AnyStr, Any]]) -> List[Dict[AnyStr, Any]]:

        return [self.dynamodb_utils.load_object(dynamodb_object=object_) for object_ in dynamodb_objects]

    def publish_objects(self, objects: List[Dict[AnyStr, Any]]):

        for object_ in objects:
            self.sns_utils.send_message(
                message=json.dumps(object_),
                topic_name='NewProperties'
            )
