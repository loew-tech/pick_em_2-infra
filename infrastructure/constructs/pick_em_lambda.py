from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
)
from constructs import Construct

from common.constants.constants import PICK_EM_TABLE_2


class PickEmLambda(Construct):
    """
    Lambda function serving as Pick'em api

    The Lambda is granted read/write access to activities table
    and receives the table name through an environment variable.
    """

    def __init__(self, scope: Construct, construct_id: str, activities_table: dynamodb.ITable):
        super().__init__(scope, construct_id)

        self.function = lambda_.Function(
            self,
            "PickEmLambda",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.handler",
            code=lambda_.Code.from_asset("lambda_asset"),
            environment={
                PICK_EM_TABLE_2: activities_table.table_name,
            },
            reserved_concurrent_executions=3
        )

        activities_table.grant_read_write_data(self.function)
