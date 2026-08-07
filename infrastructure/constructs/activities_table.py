from aws_cdk import RemovalPolicy, aws_dynamodb as dynamodb


from constructs import Construct

from common.constants.constants import PK, SK


class ActivitiesTable(Construct):
    """
    DynamoDB table for user activities.

    Primary access pattern:
        PK = USER#<user_id>
        SK = CATEGORY#<category>#ACTIVITY#<activity_id>

    This allows:
        - Query all activities for a user
        - Query all activities in a category
        - Store multiple activities per category
    """

    def __init__(self, scope: Construct, construct_id: str) -> None:
        super().__init__(scope, construct_id)

        self._table = dynamodb.Table(
            self,
            'ActivitiesTable',
            partition_key=dynamodb.Attribute(
                name=PK,
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name=SK,
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

    @property
    def table(self) -> dynamodb.ITable:
        return self._table