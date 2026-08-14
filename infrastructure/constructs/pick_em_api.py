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
            proxy=False,
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

        integration = apigateway.LambdaIntegration(function)

        # /categories
        categories = self.api.root.add_resource("categories")
        categories.add_method("GET", integration)

        # /categories/{category_id}
        category = categories.add_resource("{category_id}")
        category.add_method("GET", integration)

        # /activities/{category_id}
        activities = self.api.root.add_resource("activities")
        category_activities = activities.add_resource("{category_id}")
        category_activities.add_method("POST", integration)

        # /activities/{category_id}/{activity_id}
        activity = category_activities.add_resource("{activity_id}")
        activity.add_method("PUT", integration)
        activity.add_method("DELETE", integration)

        # /pick
        pick = self.api.root.add_resource("pick")
        pick.add_method("POST", integration)

        self.url = self.api.url