import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.stack import PickEm2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in infrastructure/stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PickEm2Stack(app, "pick-em-2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
