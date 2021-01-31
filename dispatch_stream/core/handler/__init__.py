import logging
from dataclasses import dataclass
from typing import Any, AnyStr, Dict

from lambda_handler import LambdaHandler
from .. import DispatchStreamLambdaCore


@dataclass(init=False)
class DispatchStreamLambda(LambdaHandler):

    logger: logging.Logger

    def __init__(self, logger):

        super().__init__(logger=logger)
        self.core = DispatchStreamLambdaCore(
            logger=self.logger
        )

    def run(self, event: Any, context: Any) -> Dict[AnyStr, Any]:

        records = [
            record['dynamodb']['NewImage']
            for record in event['Records'] if record['eventName'] in ('INSERT', 'MODIFY')
        ]
        objects = self.core.load_dynamodb_objects(dynamodb_objects=records)
        self.core.publish_objects(objects=objects)


LAMBDA_HANDLER = DispatchStreamLambda(
    logger=logging.getLogger()
)
