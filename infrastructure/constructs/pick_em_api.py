from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_cognito as cognito,
)
from constructs import Construct


class PickEmApi(Construct):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 function: lambda_.IFunction,
                 user_pool: cognito.IUserPool) -> None:
        super().__init__(scope, construct_id)

        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self,
            "PickEmAuthorizer",
            cognito_user_pools=[user_pool],
        )

        self.api = apigateway.LambdaRestApi(
            self,
            "PickEmApi",
            handler=function,
            proxy=True,
            default_method_options=apigateway.MethodOptions(
                authorizer=authorizer,
                authorization_type=apigateway.AuthorizationType.COGNITO,
            ),
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=["http://localhost:5173"],
                allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                allow_headers=["Authorization", "Content-Type"],
            ),
        )
        self.url = self.api.url