from aws_cdk import aws_apigateway as apigateway, aws_lambda as lambda_
from constructs import Construct


class PickEmApi(Construct):

    def __init__(self, scope: Construct, construct_id: str, function: lambda_.IFunction) -> None:
        super().__init__(scope, construct_id)

        api = apigateway.LambdaRestApi(
            self,
            "PickEmApi",
            handler=function,
            proxy=True
        )

        self.url = api.url