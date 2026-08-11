from aws_cdk import aws_cognito as cognito
from constructs import Construct

from infrastructure.config_constants.constants import PICK_EM_USERS, PICK_EM_WEB_CLIENT


class PickEmAuth(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.user_pool = cognito.UserPool(
            self,
            'PickEmUserPool',
            user_pool_name=PICK_EM_USERS,
            sign_in_aliases=cognito.SignInAliases(
                username=True,
                email=True
            ),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True
            )
        )

        self.client = self.user_pool.add_client(
            PICK_EM_WEB_CLIENT,
            auth_flows=cognito.AuthFlow(
                user_srp=True,
                user_password=True,
            ),
            generate_secret=False
        )