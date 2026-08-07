from aws_cdk import Stack, CfnOutput
from constructs import Construct

from infrastructure.constructs.activities_table import ActivitiesTable
from infrastructure.constructs.pick_em_api import PickEmApi
from infrastructure.constructs.pick_em_lambda import PickEmLambda


class PickEm2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        activities_table = ActivitiesTable(self, 'ActivitiesTable')

        pick_em_lambda = PickEmLambda(self, 'PickEmLambda', activities_table=activities_table.table)

        pick_em_api = PickEmApi(self, "PickEmApi", function=pick_em_lambda.function)

        CfnOutput(
            self,
            "ApiUrl",
            value=pick_em_api.url,
        )


