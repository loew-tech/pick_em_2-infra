from aws_cdk import Stack
from constructs import Construct

from infrastructure.constructs.activities_table import ActivitiesTable
from infrastructure.constructs.pick_em_lambda import PickEmLambda


class PickEm2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        activities_table = ActivitiesTable(self, 'ActivitiesTable')
        self.pick_em_lambda = PickEmLambda(self, 'PickEmLambda', activities_table=activities_table.table)


