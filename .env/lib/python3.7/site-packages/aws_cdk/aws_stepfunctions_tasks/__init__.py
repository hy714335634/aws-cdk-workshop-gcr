"""
# Tasks for AWS Step Functions

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) is a web service that enables you to coordinate the
components of distributed applications and microservices using visual workflows.
You build applications from individual components that each perform a discrete
function, or task, allowing you to scale and change applications quickly.

A [Task](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-task-state.html) state represents a single unit of work performed by a state machine.
All work in your state machine is performed by tasks.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Table Of Contents

* [Task](#task)
* [Paths](#paths)

  * [InputPath](#inputpath)
  * [OutputPath](#outputpath)
  * [ResultPath](#resultpath)
* [Parameters](#task-parameters-from-the-state-json)
* [Evaluate Expression](#evaluate-expression)
* [Batch](#batch)

  * [SubmitJob](#submitjob)
* [DynamoDB](#dynamodb)

  * [GetItem](#getitem)
  * [PutItem](#putitem)
  * [DeleteItem](#deleteitem)
  * [UpdateItem](#updateitem)
* [ECS](#ecs)

  * [RunTask](#runtask)
* [EMR](#emr)

  * [Create Cluster](#create-cluster)
  * [Termination Protection](#termination-protection)
  * [Terminate Cluster](#terminate-cluster)
  * [Add Step](#add-step)
  * [Cancel Step](#cancel-step)
  * [Modify Instance Fleet](#modify-instance-fleet)
  * [Modify Instance Group](#modify-instance-group)
* [Glue](#glue)
* [Lambda](#lambda)
* [SageMaker](#sagemaker)

  * [Create Training Job](#create-training-job)
  * [Create Transform Job](#create-transform-job)
* [SNS](#sns)
* [Step Functions](#step-functions)
* [SQS](#sqs)

## Task

A Task state represents a single unit of work performed by a state machine. In the
CDK, the exact work to be In the CDK, the exact work to be done is determined by
a class that implements `IStepFunctionsTask`.

AWS Step Functions [integrates](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html) with some AWS services so that you can call API
actions, and coordinate executions directly from the Amazon States Language in
Step Functions. You can directly call and pass parameters to the APIs of those
services.

## Paths

In the Amazon States Language, a [path](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-paths.html) is a string beginning with `$` that you
can use to identify components within JSON text.

Learn more about input and output processing in Step Functions [here](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-input-output-filtering.html)

### InputPath

Both `InputPath` and `Parameters` fields provide a way to manipulate JSON as it
moves through your workflow. AWS Step Functions applies the `InputPath` field first,
and then the `Parameters` field. You can first filter your raw input to a selection
you want using InputPath, and then apply Parameters to manipulate that input
further, or add new values. If you don't specify an `InputPath`, a default value
of `$` will be used.

The following example provides the field named `input` as the input to the `Task`
state that runs a Lambda function.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
submit_job = sfn.Task(stack, "Invoke Handler",
    task=tasks.RunLambdaTask(submit_job_lambda),
    input_path="$.input"
)
```

### OutputPath

Tasks also allow you to select a portion of the state output to pass to the next
state. This enables you to filter out unwanted information, and pass only the
portion of the JSON that you care about. If you don't specify an `OutputPath`,
a default value of `$` will be used. This passes the entire JSON node to the next
state.

The [response](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_ResponseSyntax) from a Lambda function includes the response from the function
as well as other metadata.

The following example assigns the output from the Task to a field named `result`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
submit_job = sfn.Task(stack, "Invoke Handler",
    task=tasks.RunLambdaTask(submit_job_lambda),
    output_path="$.Payload.result"
)
```

### ResultPath

The output of a state can be a copy of its input, the result it produces (for
example, output from a Task state’s Lambda function), or a combination of its
input and result. Use [`ResultPath`](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-resultpath.html) to control which combination of these is
passed to the state output. If you don't specify an `ResultPath`, a default
value of `$` will be used.

The following example adds the item from calling DynamoDB's `getItem` API to the state
input and passes it to the next state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(self, "PutItem",
    task=tasks.CallDynamoDB.get_item(
        item={
            "MessageId": tasks.DynamoAttributeValue().with_s("12345")
        },
        table_name="my-table"
    ),
    result_path="$.Item"
)
```

⚠️ The `OutputPath` is computed after applying `ResultPath`. All service integrations
return metadata as part of their response. When using `ResultPath`, it's not possible to
merge a subset of the task output to the input.

## Task parameters from the state JSON

Most tasks take parameters. Parameter values can either be static, supplied directly
in the workflow definition (by specifying their values), or a value available at runtime
in the state machine's execution (either as its input or an output of a prior state).
Parameter values available at runtime can be specified via the `Data` class,
using methods such as `Data.stringAt()`.

The following example provides the field named `input` as the input to the Lambda function
and invokes it asynchronously.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
submit_job = sfn.Task(stack, "Invoke Handler",
    task=tasks.RunLambdaTask(submit_job_lambda,
        payload=sfn.Data.StringAt("$.input"),
        invocation_type=tasks.InvocationType.EVENT
    )
)
```

Each service integration has its own set of parameters that can be supplied.

## Evaluate Expression

Use the `EvaluateExpression` to perform simple operations referencing state paths. The
`expression` referenced in the task will be evaluated in a Lambda function
(`eval()`). This allows you to not have to write Lambda code for simple operations.

Example: convert a wait time from milliseconds to seconds, concat this in a message and wait:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
convert_to_seconds = sfn.Task(self, "Convert to seconds",
    task=tasks.EvaluateExpression(expression="$.waitMilliseconds / 1000"),
    result_path="$.waitSeconds"
)

create_message = sfn.Task(self, "Create message",
    # Note: this is a string inside a string.
    task=tasks.EvaluateExpression(
        expression="`Now waiting ${$.waitSeconds} seconds...`",
        runtime=lambda.Runtime.NODEJS_10_X
    ),
    result_path="$.message"
)

publish_message = sfn.Task(self, "Publish message",
    task=tasks.PublishToTopic(topic,
        message=sfn.TaskInput.from_data_at("$.message")
    ),
    result_path="$.sns"
)

wait = sfn.Wait(self, "Wait",
    time=sfn.WaitTime.seconds_path("$.waitSeconds")
)

sfn.StateMachine(self, "StateMachine",
    definition=convert_to_seconds.next(create_message).next(publish_message).next(wait)
)
```

The `EvaluateExpression` supports a `runtime` prop to specify the Lambda
runtime to use to evaluate the expression. Currently, the only runtime
supported is `lambda.Runtime.NODEJS_10_X`.

## Batch

Step Functions supports [Batch](https://docs.aws.amazon.com/step-functions/latest/dg/connect-batch.html) through the service integration pattern.

### SubmitJob

The [SubmitJob](https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html) API submits an AWS Batch job from a job definition.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_batch as batch

batch_queue = batch.JobQueue(self, "JobQueue",
    compute_environments=[JobQueueComputeEnvironment(
        order=1,
        compute_environment=batch.ComputeEnvironment(self, "ComputeEnv",
            compute_resources=ComputeResources(vpc=vpc)
        )
    )
    ]
)

batch_job_definition = batch.JobDefinition(self, "JobDefinition",
    container=JobDefinitionContainer(
        image=ecs.ContainerImage.from_asset(path.resolve(__dirname, "batchjob-image"))
    )
)

task = sfn.Task(self, "Submit Job",
    task=tasks.RunBatchJob(
        job_definition=batch_job_definition,
        job_name="MyJob",
        job_queue=batch_queue
    )
)
```

## DynamoDB

You can call DynamoDB APIs from a `Task` state.
Read more about calling DynamoDB APIs [here](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ddb.html)

### GetItem

The [GetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html) operation returns a set of attributes for the item with the given primary key.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(self, "Get Item",
    task=tasks.CallDynamoDB.get_item(
        partition_key={
            "name": "messageId",
            "value": tasks.DynamoAttributeValue().with_s("message-007")
        },
        table_name="my-table"
    )
)
```

### PutItem

The [PutItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html) operation creates a new item, or replaces an old item with a new item.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(self, "PutItem",
    task=tasks.CallDynamoDB.put_item(
        item={
            "MessageId": tasks.DynamoAttributeValue().with_s("message-007"),
            "Text": tasks.DynamoAttributeValue().with_s(sfn.Data.string_at("$.bar")),
            "TotalCount": tasks.DynamoAttributeValue().with_n("10")
        },
        table_name="my-table"
    )
)
```

### DeleteItem

The [DeleteItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html) operation deletes a single item in a table by primary key.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(self, "DeleteItem",
    task=tasks.CallDynamoDB.delete_item(
        partition_key={
            "name": "MessageId",
            "value": tasks.DynamoAttributeValue().with_s("message-007")
        },
        table_name="my-table"
    ),
    result_path="DISCARD"
)
```

### UpdateItem

The [UpdateItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html) operation edits an existing item's attributes, or adds a new item
to the table if it does not already exist.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
update_item_task = sfn.Task(self, "UpdateItem",
    task=tasks.CallDynamoDB.update_item(
        partition_key={
            "name": "MessageId",
            "value": tasks.DynamoAttributeValue().with_s("message-007")
        },
        table_name="my-table",
        expression_attribute_values={
            ":val": tasks.DynamoAttributeValue().with_n(sfn.Data.string_at("$.Item.TotalCount.N")),
            ":rand": tasks.DynamoAttributeValue().with_n("20")
        },
        update_expression="SET TotalCount = :val + :rand"
    )
)
```

## ECS

Step Functions supports [ECS/Fargate](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html) through the service integration pattern.

### RunTask

[RunTask](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html) starts a new task using the specified task definition.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ecs as ecs

# See examples in ECS library for initialization of 'cluster' and 'taskDefinition'

ecs.RunEcsFargateTask(
    cluster=cluster,
    task_definition=task_definition,
    container_overrides=[{
        "container_name": "TheContainer",
        "environment": [{
            "name": "CONTAINER_INPUT",
            "value": Data.string_at("$.valueFromStateData")
        }
        ]
    }
    ]
)

fargate_task.connections.allow_to_default_port(rds_cluster, "Read the database")

sfn.Task(self, "CallFargate",
    task=fargate_task
)
```

## EMR

Step Functions supports Amazon EMR through the service integration pattern.
The service integration APIs correspond to Amazon EMR APIs but differ in the
parameters that are used.

[Read more](https://docs.aws.amazon.com/step-functions/latest/dg/connect-emr.html) about the differences when using these service integrations.

### Create Cluster

Creates and starts running a cluster (job flow).
Corresponds to the [`runJobFlow`](https://docs.aws.amazon.com/emr/latest/APIReference/API_RunJobFlow.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster_role = iam.Role(stack, "ClusterRole",
    assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
)

service_role = iam.Role(stack, "ServiceRole",
    assumed_by=iam.ServicePrincipal("elasticmapreduce.amazonaws.com")
)

auto_scaling_role = iam.Role(stack, "AutoScalingRole",
    assumed_by=iam.ServicePrincipal("elasticmapreduce.amazonaws.com")
)

auto_scaling_role.assume_role_policy.add_statements(
    iam.PolicyStatement(
        effect=iam.Effect.ALLOW,
        principals=[
            iam.ServicePrincipal("application-autoscaling.amazonaws.com")
        ],
        actions=["sts:AssumeRole"
        ]
    ))

sfn.Task(stack, "Create Cluster",
    task=tasks.EmrCreateCluster(
        instances={},
        cluster_role=cluster_role,
        name=sfn.TaskInput.from_data_at("$.ClusterName").value,
        service_role=service_role,
        auto_scaling_role=auto_scaling_role,
        integration_pattern=sfn.ServiceIntegrationPattern.FIRE_AND_FORGET
    )
)
```

### Termination Protection

Locks a cluster (job flow) so the EC2 instances in the cluster cannot be
terminated by user intervention, an API call, or a job-flow error.

Corresponds to the [`setTerminationProtection`](https://docs.aws.amazon.com/step-functions/latest/dg/connect-emr.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(stack, "Task",
    task=tasks.EmrSetClusterTerminationProtection(
        cluster_id="ClusterId",
        termination_protected=False
    )
)
```

### Terminate Cluster

Shuts down a cluster (job flow).
Corresponds to the [`terminateJobFlows`](https://docs.aws.amazon.com/emr/latest/APIReference/API_TerminateJobFlows.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(stack, "Task",
    task=tasks.EmrTerminateCluster(
        cluster_id="ClusterId"
    )
)
```

### Add Step

Adds a new step to a running cluster.
Corresponds to the [`addJobFlowSteps`](https://docs.aws.amazon.com/emr/latest/APIReference/API_AddJobFlowSteps.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(stack, "Task",
    task=tasks.EmrAddStep(
        cluster_id="ClusterId",
        name="StepName",
        jar="Jar",
        action_on_failure=tasks.ActionOnFailure.CONTINUE
    )
)
```

### Cancel Step

Cancels a pending step in a running cluster.
Corresponds to the [`cancelSteps`](https://docs.aws.amazon.com/emr/latest/APIReference/API_CancelSteps.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(stack, "Task",
    task=tasks.EmrCancelStep(
        cluster_id="ClusterId",
        step_id="StepId"
    )
)
```

### Modify Instance Fleet

Modifies the target On-Demand and target Spot capacities for the instance
fleet with the specified InstanceFleetName.

Corresponds to the [`modifyInstanceFleet`](https://docs.aws.amazon.com/emr/latest/APIReference/API_ModifyInstanceFleet.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(stack, "Task",
    task=tasks.EmrModifyInstanceFleetByName(
        cluster_id="ClusterId",
        instance_fleet_name="InstanceFleetName",
        target_on_demand_capacity=2,
        target_spot_capacity=0
    )
)
```

### Modify Instance Group

Modifies the number of nodes and configuration settings of an instance group.

Corresponds to the [`modifyInstanceGroups`](https://docs.aws.amazon.com/emr/latest/APIReference/API_ModifyInstanceGroups.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(stack, "Task",
    task=tasks.EmrModifyInstanceGroupByName(
        cluster_id="ClusterId",
        instance_group_name=sfn.Data.string_at("$.InstanceGroupName"),
        instance_group={
            "instance_count": 1
        }
    )
)
```

## Glue

Step Functions supports [AWS Glue](https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html) through the service integration pattern.

You can call the [`StartJobRun`](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-runs.html#aws-glue-api-jobs-runs-StartJobRun) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
GlueStartJobRun(stack, "Task",
    job_name="my-glue-job",
    arguments={
        "key": "value"
    },
    timeout=cdk.Duration.minutes(30),
    notify_delay_after=cdk.Duration.minutes(5)
)
```

## Lambda

[Invoke](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html) a Lambda function.

You can specify the input to your Lambda function through the `payload` attribute.
By default, Step Functions invokes Lambda function with the state input (JSON path '$')
as the input.

The following snippet invokes a Lambda Function with the state input as the payload
by referencing the `$` path.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks

my_lambda = lambda.Function(self, "my sample lambda",
    code=Code.from_inline("exports.handler = async () => {\n    return {\n      statusCode: '200',\n      body: 'hello, world!'\n    };\n  };"),
    runtime=Runtime.NODEJS_12_X,
    handler="index.handler"
)

tasks.LambdaInvoke(self, "Invoke with state input",
    lambda_function=my_lambda
)
```

When a function is invoked, the Lambda service sends  [these response
elements](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_ResponseElements)
back.

⚠️ The response from the Lambda function is in an attribute called `Payload`

The following snippet invokes a Lambda Function by referencing the `$.Payload` path
to reference the output of a Lambda executed before it.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.LambdaInvoke(self, "Invoke with empty object as payload",
    lambda_function=my_lambda,
    payload=sfn.TaskInput.from_object()
)

# use the output of myLambda as input
tasks.LambdaInvoke(self, "Invoke with payload field in the state input",
    lambda_function=my_other_lambda,
    payload=sfn.TaskInput.from_data_at("$.Payload")
)
```

The following snippet invokes a Lambda and sets the task output to only include
the Lambda function response.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.LambdaInvoke(self, "Invoke and set function response as task output",
    lambda_function=my_lambda,
    payload=sfn.TaskInput.from_data_at("$"),
    output_path="$.Payload"
)
```

You can have Step Functions pause a task, and wait for an external process to
return a task token. Read more about the [callback pattern](https://docs.aws.amazon.com/step-functions/latest/dg/callback-task-sample-sqs.html#call-back-lambda-example)

To use the callback pattern, set the `token` property on the task. Call the Step
Functions `SendTaskSuccess` or `SendTaskFailure` APIs with the token to
indicate that the task has completed and the state machine should resume execution.

The following snippet invokes a Lambda with the task token as part of the input
to the Lambda.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.LambdaInvoke(stack, "Invoke with callback",
    lambda_function=my_lambda,
    integration_pattern=sfn.IntegrationPattern.WAIT_FOR_TASK_TOKEN,
    payload=sfn.TaskInput.from_object(
        token=sfn.Context.task_token,
        input=sfn.Data.string_at("$.someField")
    )
)
```

⚠️ The task will pause until it receives that task token back with a `SendTaskSuccess` or `SendTaskFailure`
call. Learn more about [Callback with the Task
Token](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token).

## SageMaker

Step Functions supports [AWS SageMaker](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html) through the service integration pattern.

### Create Training Job

You can call the [`CreateTrainingJob`](https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTrainingJob.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.Task(stack, "TrainSagemaker",
    task=tasks.SagemakerTrainTask(
        training_job_name=sfn.Data.string_at("$.JobName"),
        role=role,
        algorithm_specification={
            "algorithm_name": "BlazingText",
            "training_input_mode": tasks.InputMode.FILE
        },
        input_data_config=[{
            "channel_name": "train",
            "data_source": {
                "s3_data_source": {
                    "s3_data_type": tasks.S3DataType.S3_PREFIX,
                    "s3_location": tasks.S3Location.from_json_expression("$.S3Bucket")
                }
            }
        }
        ],
        output_data_config={
            "s3_output_location": tasks.S3Location.from_bucket(s3.Bucket.from_bucket_name(stack, "Bucket", "mybucket"), "myoutputpath")
        },
        resource_config={
            "instance_count": 1,
            "instance_type": ec2.InstanceType.of(ec2.InstanceClass.P3, ec2.InstanceSize.XLARGE2),
            "volume_size_in_gB": 50
        },
        stopping_condition={
            "max_runtime": cdk.Duration.hours(1)
        }
    )
)
```

### Create Transform Job

You can call the [`CreateTransformJob`](https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTransformJob.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
transform_job = tasks.SagemakerTransformTask(transform_job_name, "MyTransformJob", model_name, "MyModelName", role, transform_input, {
    "transform_data_source": {
        "s3_data_source": {
            "s3_uri": "s3://inputbucket/train",
            "s3_data_type": S3DataType.S3Prefix
        }
    }
}, transform_output, {
    "s3_output_path": "s3://outputbucket/TransformJobOutputPath"
}, transform_resources,
    instance_count=1,
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.M4, ec2.InstanceSize.XLarge)
)

task = sfn.Task(self, "Batch Inference",
    task=transform_job
)
```

## SNS

Step Functions supports [Amazon SNS](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sns.html) through the service integration pattern.

You can call the [`Publish`](https://docs.aws.amazon.com/sns/latest/api/API_Publish.html) API from a `Task` state to publish to an SNS topic.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns as sns
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks

# ...

topic = sns.Topic(self, "Topic")

# Use a field from the execution data as message.
task1 = tasks.SnsPublish(self, "Publish1",
    topic=topic,
    integration_pattern=sfn.IntegrationPattern.REQUEST_RESPONSE,
    message=sfn.TaskInput.from_data_at("$.state.message")
)

# Combine a field from the execution data with
# a literal object.
task2 = tasks.SnsPublish(self, "Publish2",
    topic=topic,
    message=sfn.TaskInput.from_object({
        "field1": "somedata",
        "field2": sfn.Data.string_at("$.field2")
    })
)
```

## Step Functions

You can manage [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/connect-stepfunctions.html) executions.

AWS Step Functions supports it's own [`StartExecution`](https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html) API as a service integration.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Define a state machine with one Pass state
child = sfn.StateMachine(stack, "ChildStateMachine",
    definition=sfn.Chain.start(sfn.Pass(stack, "PassState"))
)

# Include the state machine in a Task state with callback pattern
task = sfn.Task(stack, "ChildTask",
    task=tasks.ExecuteStateMachine(child,
        integration_pattern=sfn.ServiceIntegrationPattern.WAIT_FOR_TASK_TOKEN,
        input={
            "token": sfn.Context.task_token,
            "foo": "bar"
        },
        name="MyExecutionName"
    )
)

# Define a second state machine with the Task state above
sfn.StateMachine(stack, "ParentStateMachine",
    definition=task
)
```

## SQS

Step Functions supports [Amazon SQS](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sqs.html)

You can call the [`SendMessage`](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html) API from a `Task` state
to send a message to an SQS queue.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_sqs as sqs

# ...

queue = sqs.Queue(self, "Queue")

# Use a field from the execution data as message.
task1 = tasks.SqsSendMessage(self, "Send1",
    queue=queue,
    message_body=sfn.TaskInput.from_data_at("$.message")
)

# Combine a field from the execution data with
# a literal object.
task2 = tasks.SqsSendMessage(self, "Send2",
    queue=queue,
    message_body=sfn.TaskInput.from_object({
        "field1": "somedata",
        "field2": sfn.Data.string_at("$.field2")
    })
)
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.assets
import aws_cdk.aws_batch
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecr_assets
import aws_cdk.aws_ecs
import aws_cdk.aws_glue
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.aws_stepfunctions
import aws_cdk.core
import constructs

from ._jsii import *


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.ActionOnFailure")
class ActionOnFailure(enum.Enum):
    """The action to take when the cluster step fails.

    default
    :default: CONTINUE

    see
    :see:

    https://docs.aws.amazon.com/emr/latest/APIReference/API_StepConfig.html

    Here, they are named as TERMINATE_JOB_FLOW, TERMINATE_CLUSTER, CANCEL_AND_WAIT, and CONTINUE respectively.
    stability
    :stability: experimental
    """
    TERMINATE_CLUSTER = "TERMINATE_CLUSTER"
    """Terminate the Cluster on Step Failure.

    stability
    :stability: experimental
    """
    CANCEL_AND_WAIT = "CANCEL_AND_WAIT"
    """Cancel Step execution and enter WAITING state.

    stability
    :stability: experimental
    """
    CONTINUE = "CONTINUE"
    """Continue to the next Step.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.AlgorithmSpecification", jsii_struct_bases=[], name_mapping={'algorithm_name': 'algorithmName', 'metric_definitions': 'metricDefinitions', 'training_image': 'trainingImage', 'training_input_mode': 'trainingInputMode'})
class AlgorithmSpecification():
    def __init__(self, *, algorithm_name: typing.Optional[str]=None, metric_definitions: typing.Optional[typing.List["MetricDefinition"]]=None, training_image: typing.Optional["DockerImage"]=None, training_input_mode: typing.Optional["InputMode"]=None) -> None:
        """Specify the training algorithm and algorithm-specific metadata.

        :param algorithm_name: Name of the algorithm resource to use for the training job. This must be an algorithm resource that you created or subscribe to on AWS Marketplace. If you specify a value for this parameter, you can't specify a value for TrainingImage. Default: - No algorithm is specified
        :param metric_definitions: List of metric definition objects. Each object specifies the metric name and regular expressions used to parse algorithm logs. Default: - No metrics
        :param training_image: Registry path of the Docker image that contains the training algorithm. Default: - No Docker image is specified
        :param training_input_mode: Input mode that the algorithm supports. Default: 'File' mode

        stability
        :stability: experimental
        """
        self._values = {
        }
        if algorithm_name is not None: self._values["algorithm_name"] = algorithm_name
        if metric_definitions is not None: self._values["metric_definitions"] = metric_definitions
        if training_image is not None: self._values["training_image"] = training_image
        if training_input_mode is not None: self._values["training_input_mode"] = training_input_mode

    @builtins.property
    def algorithm_name(self) -> typing.Optional[str]:
        """Name of the algorithm resource to use for the training job.

        This must be an algorithm resource that you created or subscribe to on AWS Marketplace.
        If you specify a value for this parameter, you can't specify a value for TrainingImage.

        default
        :default: - No algorithm is specified

        stability
        :stability: experimental
        """
        return self._values.get('algorithm_name')

    @builtins.property
    def metric_definitions(self) -> typing.Optional[typing.List["MetricDefinition"]]:
        """List of metric definition objects.

        Each object specifies the metric name and regular expressions used to parse algorithm logs.

        default
        :default: - No metrics

        stability
        :stability: experimental
        """
        return self._values.get('metric_definitions')

    @builtins.property
    def training_image(self) -> typing.Optional["DockerImage"]:
        """Registry path of the Docker image that contains the training algorithm.

        default
        :default: - No Docker image is specified

        stability
        :stability: experimental
        """
        return self._values.get('training_image')

    @builtins.property
    def training_input_mode(self) -> typing.Optional["InputMode"]:
        """Input mode that the algorithm supports.

        default
        :default: 'File' mode

        stability
        :stability: experimental
        """
        return self._values.get('training_input_mode')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AlgorithmSpecification(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.AssembleWith")
class AssembleWith(enum.Enum):
    """How to assemble the results of the transform job as a single S3 object.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """Concatenate the results in binary format.

    stability
    :stability: experimental
    """
    LINE = "LINE"
    """Add a newline character at the end of every transformed record.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.BatchStrategy")
class BatchStrategy(enum.Enum):
    """Specifies the number of records to include in a mini-batch for an HTTP inference request.

    stability
    :stability: experimental
    """
    MULTI_RECORD = "MULTI_RECORD"
    """Fits multiple records in a mini-batch.

    stability
    :stability: experimental
    """
    SINGLE_RECORD = "SINGLE_RECORD"
    """Use a single record when making an invocation request.

    stability
    :stability: experimental
    """

class CallDynamoDB(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.CallDynamoDB"):
    """A helper wrapper class to call all DynamoDB APIs.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(CallDynamoDB, self, [])

    @jsii.member(jsii_name="deleteItem")
    @builtins.classmethod
    def delete_item(cls, *, partition_key: "DynamoAttribute", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None, sort_key: typing.Optional["DynamoAttribute"]=None) -> "DynamoDeleteItem":
        """Method to get DynamoDeleteItem task.

        :param partition_key: An attribute representing the partition key of the item to delete.
        :param table_name: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param sort_key: An attribute representing the sort key of the item to delete. Default: - No sort key

        stability
        :stability: experimental
        """
        props = DynamoDeleteItemProps(partition_key=partition_key, table_name=table_name, condition_expression=condition_expression, expression_attribute_names=expression_attribute_names, expression_attribute_values=expression_attribute_values, return_consumed_capacity=return_consumed_capacity, return_item_collection_metrics=return_item_collection_metrics, return_values=return_values, sort_key=sort_key)

        return jsii.sinvoke(cls, "deleteItem", [props])

    @jsii.member(jsii_name="getItem")
    @builtins.classmethod
    def get_item(cls, *, partition_key: "DynamoAttribute", table_name: str, consistent_read: typing.Optional[bool]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, projection_expression: typing.Optional[typing.List["DynamoProjectionExpression"]]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, sort_key: typing.Optional["DynamoAttribute"]=None) -> "DynamoGetItem":
        """Method to get DynamoGetItem task.

        :param partition_key: A attribute representing the partition key of the item to retrieve.
        :param table_name: The name of the table containing the requested item.
        :param consistent_read: Determines the read consistency model: If set to true, then the operation uses strongly consistent reads; otherwise, the operation uses eventually consistent reads. Default: false
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attributes
        :param projection_expression: An array of DynamoProjectionExpression that identifies one or more attributes to retrieve from the table. These attributes can include scalars, sets, or elements of a JSON document. Default: - No projection expression
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param sort_key: A attribute representing the sort key of the item to retrieve. Default: - No sort key

        stability
        :stability: experimental
        """
        props = DynamoGetItemProps(partition_key=partition_key, table_name=table_name, consistent_read=consistent_read, expression_attribute_names=expression_attribute_names, projection_expression=projection_expression, return_consumed_capacity=return_consumed_capacity, sort_key=sort_key)

        return jsii.sinvoke(cls, "getItem", [props])

    @jsii.member(jsii_name="putItem")
    @builtins.classmethod
    def put_item(cls, *, item: "DynamoAttributeValueMap", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None) -> "DynamoPutItem":
        """Method to get DynamoPutItem task.

        :param item: A map of attribute name/value pairs, one for each attribute. Only the primary key attributes are required; you can optionally provide other attribute name-value pairs for the item.
        :param table_name: The name of the table where the item should be writen .
        :param condition_expression: A condition that must be satisfied in order for a conditional PutItem operation to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: The item collection metrics to returned in the response. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were updated with the PutItem request. Default: DynamoReturnValues.NONE

        stability
        :stability: experimental
        """
        props = DynamoPutItemProps(item=item, table_name=table_name, condition_expression=condition_expression, expression_attribute_names=expression_attribute_names, expression_attribute_values=expression_attribute_values, return_consumed_capacity=return_consumed_capacity, return_item_collection_metrics=return_item_collection_metrics, return_values=return_values)

        return jsii.sinvoke(cls, "putItem", [props])

    @jsii.member(jsii_name="updateItem")
    @builtins.classmethod
    def update_item(cls, *, partition_key: "DynamoAttribute", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None, sort_key: typing.Optional["DynamoAttribute"]=None, update_expression: typing.Optional[str]=None) -> "DynamoUpdateItem":
        """Method to get DynamoUpdateItem task.

        :param partition_key: The partition key of the item to be updated.
        :param table_name: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param sort_key: The sort key of the item to be updated. Default: - No sort key
        :param update_expression: An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them. Default: - No update expression

        stability
        :stability: experimental
        """
        props = DynamoUpdateItemProps(partition_key=partition_key, table_name=table_name, condition_expression=condition_expression, expression_attribute_names=expression_attribute_names, expression_attribute_values=expression_attribute_values, return_consumed_capacity=return_consumed_capacity, return_item_collection_metrics=return_item_collection_metrics, return_values=return_values, sort_key=sort_key, update_expression=update_expression)

        return jsii.sinvoke(cls, "updateItem", [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.Channel", jsii_struct_bases=[], name_mapping={'channel_name': 'channelName', 'data_source': 'dataSource', 'compression_type': 'compressionType', 'content_type': 'contentType', 'input_mode': 'inputMode', 'record_wrapper_type': 'recordWrapperType', 'shuffle_config': 'shuffleConfig'})
class Channel():
    def __init__(self, *, channel_name: str, data_source: "DataSource", compression_type: typing.Optional["CompressionType"]=None, content_type: typing.Optional[str]=None, input_mode: typing.Optional["InputMode"]=None, record_wrapper_type: typing.Optional["RecordWrapperType"]=None, shuffle_config: typing.Optional["ShuffleConfig"]=None) -> None:
        """Describes the training, validation or test dataset and the Amazon S3 location where it is stored.

        :param channel_name: Name of the channel.
        :param data_source: Location of the channel data.
        :param compression_type: Compression type if training data is compressed. Default: - None
        :param content_type: The MIME type of the data. Default: - None
        :param input_mode: Input mode to use for the data channel in a training job. Default: - None
        :param record_wrapper_type: Specify RecordIO as the value when input data is in raw format but the training algorithm requires the RecordIO format. In this case, Amazon SageMaker wraps each individual S3 object in a RecordIO record. If the input data is already in RecordIO format, you don't need to set this attribute. Default: - None
        :param shuffle_config: Shuffle config option for input data in a channel. Default: - None

        stability
        :stability: experimental
        """
        if isinstance(data_source, dict): data_source = DataSource(**data_source)
        if isinstance(shuffle_config, dict): shuffle_config = ShuffleConfig(**shuffle_config)
        self._values = {
            'channel_name': channel_name,
            'data_source': data_source,
        }
        if compression_type is not None: self._values["compression_type"] = compression_type
        if content_type is not None: self._values["content_type"] = content_type
        if input_mode is not None: self._values["input_mode"] = input_mode
        if record_wrapper_type is not None: self._values["record_wrapper_type"] = record_wrapper_type
        if shuffle_config is not None: self._values["shuffle_config"] = shuffle_config

    @builtins.property
    def channel_name(self) -> str:
        """Name of the channel.

        stability
        :stability: experimental
        """
        return self._values.get('channel_name')

    @builtins.property
    def data_source(self) -> "DataSource":
        """Location of the channel data.

        stability
        :stability: experimental
        """
        return self._values.get('data_source')

    @builtins.property
    def compression_type(self) -> typing.Optional["CompressionType"]:
        """Compression type if training data is compressed.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('compression_type')

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        """The MIME type of the data.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('content_type')

    @builtins.property
    def input_mode(self) -> typing.Optional["InputMode"]:
        """Input mode to use for the data channel in a training job.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('input_mode')

    @builtins.property
    def record_wrapper_type(self) -> typing.Optional["RecordWrapperType"]:
        """Specify RecordIO as the value when input data is in raw format but the training algorithm requires the RecordIO format.

        In this case, Amazon SageMaker wraps each individual S3 object in a RecordIO record.
        If the input data is already in RecordIO format, you don't need to set this attribute.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('record_wrapper_type')

    @builtins.property
    def shuffle_config(self) -> typing.Optional["ShuffleConfig"]:
        """Shuffle config option for input data in a channel.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('shuffle_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Channel(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.CommonEcsRunTaskProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'task_definition': 'taskDefinition', 'container_overrides': 'containerOverrides', 'integration_pattern': 'integrationPattern'})
class CommonEcsRunTaskProps():
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None) -> None:
        """Basic properties for ECS Tasks.

        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if container_overrides is not None: self._values["container_overrides"] = container_overrides
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The topic to run the task on.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List["ContainerOverride"]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        default
        :default: - No overrides

        stability
        :stability: experimental
        """
        return self._values.get('container_overrides')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call RunTask in ECS.

        The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonEcsRunTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.CompressionType")
class CompressionType(enum.Enum):
    """Compression type of the data.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """None compression type.

    stability
    :stability: experimental
    """
    GZIP = "GZIP"
    """Gzip compression type.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.ContainerOverride", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'command': 'command', 'cpu': 'cpu', 'environment': 'environment', 'memory_limit': 'memoryLimit', 'memory_reservation': 'memoryReservation'})
class ContainerOverride():
    def __init__(self, *, container_name: str, command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.List["TaskEnvironmentVariable"]]=None, memory_limit: typing.Optional[jsii.Number]=None, memory_reservation: typing.Optional[jsii.Number]=None) -> None:
        """A list of container overrides that specify the name of a container and the overrides it should receive.

        :param container_name: Name of the container inside the task definition.
        :param command: Command to run inside the container. Default: - Default command from the Docker image or the task definition
        :param cpu: The number of cpu units reserved for the container. Default: - The default value from the task definition.
        :param environment: The environment variables to send to the container. You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the task definition. Default: - The existing environment variables from the Docker image or the task definition
        :param memory_limit: The hard limit (in MiB) of memory to present to the container. Default: - The default value from the task definition.
        :param memory_reservation: The soft limit (in MiB) of memory to reserve for the container. Default: - The default value from the task definition.

        stability
        :stability: experimental
        """
        self._values = {
            'container_name': container_name,
        }
        if command is not None: self._values["command"] = command
        if cpu is not None: self._values["cpu"] = cpu
        if environment is not None: self._values["environment"] = environment
        if memory_limit is not None: self._values["memory_limit"] = memory_limit
        if memory_reservation is not None: self._values["memory_reservation"] = memory_reservation

    @builtins.property
    def container_name(self) -> str:
        """Name of the container inside the task definition.

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """Command to run inside the container.

        default
        :default: - Default command from the Docker image or the task definition

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units reserved for the container.

        default
        :default: - The default value from the task definition.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def environment(self) -> typing.Optional[typing.List["TaskEnvironmentVariable"]]:
        """The environment variables to send to the container.

        You can add new environment variables, which are added to the container at launch,
        or you can override the existing environment variables from the Docker image or the task definition.

        default
        :default: - The existing environment variables from the Docker image or the task definition

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        default
        :default: - The default value from the task definition.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit')

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        default
        :default: - The default value from the task definition.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerOverride(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.ContainerOverrides", jsii_struct_bases=[], name_mapping={'command': 'command', 'environment': 'environment', 'gpu_count': 'gpuCount', 'instance_type': 'instanceType', 'memory': 'memory', 'vcpus': 'vcpus'})
class ContainerOverrides():
    def __init__(self, *, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, memory: typing.Optional[jsii.Number]=None, vcpus: typing.Optional[jsii.Number]=None) -> None:
        """The overrides that should be sent to a container.

        :param command: The command to send to the container that overrides the default command from the Docker image or the job definition. Default: - No command overrides
        :param environment: The environment variables to send to the container. You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the job definition. Default: - No environment overrides
        :param gpu_count: The number of physical GPUs to reserve for the container. The number of GPUs reserved for all containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on. Default: - No GPU reservation
        :param instance_type: The instance type to use for a multi-node parallel job. This parameter is not valid for single-node container jobs. Default: - No instance type overrides
        :param memory: The number of MiB of memory reserved for the job. This value overrides the value set in the job definition. Default: - No memory overrides
        :param vcpus: The number of vCPUs to reserve for the container. This value overrides the value set in the job definition. Default: - No vCPUs overrides

        stability
        :stability: experimental
        """
        self._values = {
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if gpu_count is not None: self._values["gpu_count"] = gpu_count
        if instance_type is not None: self._values["instance_type"] = instance_type
        if memory is not None: self._values["memory"] = memory
        if vcpus is not None: self._values["vcpus"] = vcpus

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command to send to the container that overrides the default command from the Docker image or the job definition.

        default
        :default: - No command overrides

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to send to the container.

        You can add new environment variables, which are added to the container
        at launch, or you can override the existing environment variables from
        the Docker image or the job definition.

        default
        :default: - No environment overrides

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of physical GPUs to reserve for the container.

        The number of GPUs reserved for all containers in a job
        should not exceed the number of available GPUs on the compute
        resource that the job is launched on.

        default
        :default: - No GPU reservation

        stability
        :stability: experimental
        """
        return self._values.get('gpu_count')

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The instance type to use for a multi-node parallel job.

        This parameter is not valid for single-node container jobs.

        default
        :default: - No instance type overrides

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        """The number of MiB of memory reserved for the job.

        This value overrides the value set in the job definition.

        default
        :default: - No memory overrides

        stability
        :stability: experimental
        """
        return self._values.get('memory')

    @builtins.property
    def vcpus(self) -> typing.Optional[jsii.Number]:
        """The number of vCPUs to reserve for the container.

        This value overrides the value set in the job definition.

        default
        :default: - No vCPUs overrides

        stability
        :stability: experimental
        """
        return self._values.get('vcpus')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerOverrides(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DataSource", jsii_struct_bases=[], name_mapping={'s3_data_source': 's3DataSource'})
class DataSource():
    def __init__(self, *, s3_data_source: "S3DataSource") -> None:
        """Location of the channel data.

        :param s3_data_source: S3 location of the data source that is associated with a channel.

        stability
        :stability: experimental
        """
        if isinstance(s3_data_source, dict): s3_data_source = S3DataSource(**s3_data_source)
        self._values = {
            's3_data_source': s3_data_source,
        }

    @builtins.property
    def s3_data_source(self) -> "S3DataSource":
        """S3 location of the data source that is associated with a channel.

        stability
        :stability: experimental
        """
        return self._values.get('s3_data_source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DataSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class DockerImage(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-stepfunctions-tasks.DockerImage"):
    """Creates ``IDockerImage`` instances.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _DockerImageProxy

    def __init__(self) -> None:
        jsii.create(DockerImage, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, scope: aws_cdk.core.Construct, id: str, *, directory: str, build_args: typing.Optional[typing.Mapping[str, str]]=None, file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None, extra_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[aws_cdk.assets.FollowMode]=None) -> "DockerImage":
        """Reference a Docker image that is provided as an Asset in the current app.

        :param scope: the scope in which to create the Asset.
        :param id: the ID for the asset in the construct tree.
        :param directory: The directory where the Dockerfile is stored.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_ecr_assets.DockerImageAssetProps(directory=directory, build_args=build_args, file=file, repository_name=repository_name, target=target, extra_hash=extra_hash, exclude=exclude, follow=follow)

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str]=None) -> "DockerImage":
        """Reference a Docker image stored in an ECR repository.

        :param repository: the ECR repository where the image is hosted.
        :param tag: an optional ``tag``.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="fromJsonExpression")
    @builtins.classmethod
    def from_json_expression(cls, expression: str, allow_any_ecr_image_pull: typing.Optional[bool]=None) -> "DockerImage":
        """Reference a Docker image which URI is obtained from the task's input.

        :param expression: the JSON path expression with the task input.
        :param allow_any_ecr_image_pull: whether ECR access should be permitted (set to ``false`` if the image will never be in ECR).

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJsonExpression", [expression, allow_any_ecr_image_pull])

    @jsii.member(jsii_name="fromRegistry")
    @builtins.classmethod
    def from_registry(cls, image_uri: str) -> "DockerImage":
        """Reference a Docker image by it's URI.

        When referencing ECR images, prefer using ``inEcr``.

        :param image_uri: the URI to the docker image.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRegistry", [image_uri])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, task: "ISageMakerTask") -> "DockerImageConfig":
        """Called when the image is used by a SageMaker task.

        :param task: -

        stability
        :stability: experimental
        """
        ...


class _DockerImageProxy(DockerImage):
    @jsii.member(jsii_name="bind")
    def bind(self, task: "ISageMakerTask") -> "DockerImageConfig":
        """Called when the image is used by a SageMaker task.

        :param task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DockerImageConfig", jsii_struct_bases=[], name_mapping={'image_uri': 'imageUri'})
class DockerImageConfig():
    def __init__(self, *, image_uri: str) -> None:
        """Configuration for a using Docker image.

        :param image_uri: The fully qualified URI of the Docker image.

        stability
        :stability: experimental
        """
        self._values = {
            'image_uri': image_uri,
        }

    @builtins.property
    def image_uri(self) -> str:
        """The fully qualified URI of the Docker image.

        stability
        :stability: experimental
        """
        return self._values.get('image_uri')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoAttribute", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
class DynamoAttribute():
    def __init__(self, *, name: str, value: "DynamoAttributeValue") -> None:
        """Property for any key.

        :param name: The name of the attribute.
        :param value: The value of the attribute.

        stability
        :stability: experimental
        """
        self._values = {
            'name': name,
            'value': value,
        }

    @builtins.property
    def name(self) -> str:
        """The name of the attribute.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def value(self) -> "DynamoAttributeValue":
        """The value of the attribute.

        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoAttribute(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class DynamoAttributeValue(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoAttributeValue"):
    """Class to generate AttributeValue.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(DynamoAttributeValue, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Any:
        """Return the attributeValue object.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toObject", [])

    @jsii.member(jsii_name="withB")
    def with_b(self, value: str) -> "DynamoAttributeValue":
        """Sets an attribute of type Binary.

        For example:  "B": "dGhpcyB0ZXh0IGlzIGJhc2U2NC1lbmNvZGVk"

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withB", [value])

    @jsii.member(jsii_name="withBOOL")
    def with_bool(self, value: bool) -> "DynamoAttributeValue":
        """Sets an attribute of type Boolean.

        For example:  "BOOL": true

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withBOOL", [value])

    @jsii.member(jsii_name="withBS")
    def with_bs(self, value: typing.List[str]) -> "DynamoAttributeValue":
        """Sets an attribute of type Binary Set.

        For example:  "BS": ["U3Vubnk=", "UmFpbnk=", "U25vd3k="]

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withBS", [value])

    @jsii.member(jsii_name="withL")
    def with_l(self, value: typing.List["DynamoAttributeValue"]) -> "DynamoAttributeValue":
        """Sets an attribute of type List.

        For example:  "L": [ {"S": "Cookies"} , {"S": "Coffee"}, {"N", "3.14159"}]

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withL", [value])

    @jsii.member(jsii_name="withM")
    def with_m(self) -> "DynamoAttributeValue":
        """Sets an attribute of type Map.

        For example:  "M": {"Name": {"S": "Joe"}, "Age": {"N": "35"}}

        stability
        :stability: experimental
        """
        value = DynamoAttributeValueMap()

        return jsii.invoke(self, "withM", [value])

    @jsii.member(jsii_name="withN")
    def with_n(self, value: str) -> "DynamoAttributeValue":
        """Sets an attribute of type Number.

        For example:  "N": "123.45"
        Numbers are sent across the network to DynamoDB as strings,
        to maximize compatibility across languages and libraries.
        However, DynamoDB treats them as number type attributes for mathematical operations.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withN", [value])

    @jsii.member(jsii_name="withNS")
    def with_ns(self, value: typing.List[str]) -> "DynamoAttributeValue":
        """Sets an attribute of type Number Set.

        For example:  "NS": ["42.2", "-19", "7.5", "3.14"]
        Numbers are sent across the network to DynamoDB as strings,
        to maximize compatibility across languages and libraries.
        However, DynamoDB treats them as number type attributes for mathematical operations.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withNS", [value])

    @jsii.member(jsii_name="withNULL")
    def with_null(self, value: bool) -> "DynamoAttributeValue":
        """Sets an attribute of type Null.

        For example:  "NULL": true

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withNULL", [value])

    @jsii.member(jsii_name="withS")
    def with_s(self, value: str) -> "DynamoAttributeValue":
        """Sets an attribute of type String.

        For example:  "S": "Hello"

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withS", [value])

    @jsii.member(jsii_name="withSS")
    def with_ss(self, value: typing.List[str]) -> "DynamoAttributeValue":
        """Sets an attribute of type String Set.

        For example:  "SS": ["Giraffe", "Hippo" ,"Zebra"]

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withSS", [value])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoAttributeValueMap", jsii_struct_bases=[], name_mapping={})
class DynamoAttributeValueMap():
    def __init__(self) -> None:
        """Map of string to AttributeValue.

        stability
        :stability: experimental
        """
        self._values = {
        }

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoAttributeValueMap(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoConsumedCapacity")
class DynamoConsumedCapacity(enum.Enum):
    """Determines the level of detail about provisioned throughput consumption that is returned.

    stability
    :stability: experimental
    """
    INDEXES = "INDEXES"
    """The response includes the aggregate ConsumedCapacity for the operation, together with ConsumedCapacity for each table and secondary index that was accessed.

    stability
    :stability: experimental
    """
    TOTAL = "TOTAL"
    """The response includes only the aggregate ConsumedCapacity for the operation.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """No ConsumedCapacity details are included in the response.

    stability
    :stability: experimental
    """

@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class DynamoDeleteItem(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoDeleteItem"):
    """A StepFunctions task to call DynamoDeleteItem.

    stability
    :stability: experimental
    """
    def __init__(self, *, partition_key: "DynamoAttribute", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None, sort_key: typing.Optional["DynamoAttribute"]=None) -> None:
        """
        :param partition_key: An attribute representing the partition key of the item to delete.
        :param table_name: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param sort_key: An attribute representing the sort key of the item to delete. Default: - No sort key

        stability
        :stability: experimental
        """
        props = DynamoDeleteItemProps(partition_key=partition_key, table_name=table_name, condition_expression=condition_expression, expression_attribute_names=expression_attribute_names, expression_attribute_values=expression_attribute_values, return_consumed_capacity=return_consumed_capacity, return_item_collection_metrics=return_item_collection_metrics, return_values=return_values, sort_key=sort_key)

        jsii.create(DynamoDeleteItem, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoDeleteItemProps", jsii_struct_bases=[], name_mapping={'partition_key': 'partitionKey', 'table_name': 'tableName', 'condition_expression': 'conditionExpression', 'expression_attribute_names': 'expressionAttributeNames', 'expression_attribute_values': 'expressionAttributeValues', 'return_consumed_capacity': 'returnConsumedCapacity', 'return_item_collection_metrics': 'returnItemCollectionMetrics', 'return_values': 'returnValues', 'sort_key': 'sortKey'})
class DynamoDeleteItemProps():
    def __init__(self, *, partition_key: "DynamoAttribute", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None, sort_key: typing.Optional["DynamoAttribute"]=None) -> None:
        """Properties for DynamoDeleteItem Task.

        :param partition_key: An attribute representing the partition key of the item to delete.
        :param table_name: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param sort_key: An attribute representing the sort key of the item to delete. Default: - No sort key

        stability
        :stability: experimental
        """
        if isinstance(partition_key, dict): partition_key = DynamoAttribute(**partition_key)
        if isinstance(expression_attribute_values, dict): expression_attribute_values = DynamoAttributeValueMap(**expression_attribute_values)
        if isinstance(sort_key, dict): sort_key = DynamoAttribute(**sort_key)
        self._values = {
            'partition_key': partition_key,
            'table_name': table_name,
        }
        if condition_expression is not None: self._values["condition_expression"] = condition_expression
        if expression_attribute_names is not None: self._values["expression_attribute_names"] = expression_attribute_names
        if expression_attribute_values is not None: self._values["expression_attribute_values"] = expression_attribute_values
        if return_consumed_capacity is not None: self._values["return_consumed_capacity"] = return_consumed_capacity
        if return_item_collection_metrics is not None: self._values["return_item_collection_metrics"] = return_item_collection_metrics
        if return_values is not None: self._values["return_values"] = return_values
        if sort_key is not None: self._values["sort_key"] = sort_key

    @builtins.property
    def partition_key(self) -> "DynamoAttribute":
        """An attribute representing the partition key of the item to delete.

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-Key
        stability
        :stability: experimental
        """
        return self._values.get('partition_key')

    @builtins.property
    def table_name(self) -> str:
        """The name of the table containing the requested item.

        stability
        :stability: experimental
        """
        return self._values.get('table_name')

    @builtins.property
    def condition_expression(self) -> typing.Optional[str]:
        """A condition that must be satisfied in order for a conditional DeleteItem to succeed.

        default
        :default: - No condition expression

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ConditionExpression
        stability
        :stability: experimental
        """
        return self._values.get('condition_expression')

    @builtins.property
    def expression_attribute_names(self) -> typing.Optional[typing.Mapping[str, str]]:
        """One or more substitution tokens for attribute names in an expression.

        default
        :default: - No expression attribute names

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ExpressionAttributeNames
        stability
        :stability: experimental
        """
        return self._values.get('expression_attribute_names')

    @builtins.property
    def expression_attribute_values(self) -> typing.Optional["DynamoAttributeValueMap"]:
        """One or more values that can be substituted in an expression.

        default
        :default: - No expression attribute values

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ExpressionAttributeValues
        stability
        :stability: experimental
        """
        return self._values.get('expression_attribute_values')

    @builtins.property
    def return_consumed_capacity(self) -> typing.Optional["DynamoConsumedCapacity"]:
        """Determines the level of detail about provisioned throughput consumption that is returned in the response.

        default
        :default: DynamoConsumedCapacity.NONE

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ReturnConsumedCapacity
        stability
        :stability: experimental
        """
        return self._values.get('return_consumed_capacity')

    @builtins.property
    def return_item_collection_metrics(self) -> typing.Optional["DynamoItemCollectionMetrics"]:
        """Determines whether item collection metrics are returned.

        If set to SIZE, the response includes statistics about item collections, if any,
        that were modified during the operation are returned in the response.
        If set to NONE (the default), no statistics are returned.

        default
        :default: DynamoItemCollectionMetrics.NONE

        stability
        :stability: experimental
        """
        return self._values.get('return_item_collection_metrics')

    @builtins.property
    def return_values(self) -> typing.Optional["DynamoReturnValues"]:
        """Use ReturnValues if you want to get the item attributes as they appeared before they were deleted.

        default
        :default: DynamoReturnValues.NONE

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ReturnValues
        stability
        :stability: experimental
        """
        return self._values.get('return_values')

    @builtins.property
    def sort_key(self) -> typing.Optional["DynamoAttribute"]:
        """An attribute representing the sort key of the item to delete.

        default
        :default: - No sort key

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-Key
        stability
        :stability: experimental
        """
        return self._values.get('sort_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoDeleteItemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class DynamoGetItem(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoGetItem"):
    """A StepFunctions task to call DynamoGetItem.

    stability
    :stability: experimental
    """
    def __init__(self, *, partition_key: "DynamoAttribute", table_name: str, consistent_read: typing.Optional[bool]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, projection_expression: typing.Optional[typing.List["DynamoProjectionExpression"]]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, sort_key: typing.Optional["DynamoAttribute"]=None) -> None:
        """
        :param partition_key: A attribute representing the partition key of the item to retrieve.
        :param table_name: The name of the table containing the requested item.
        :param consistent_read: Determines the read consistency model: If set to true, then the operation uses strongly consistent reads; otherwise, the operation uses eventually consistent reads. Default: false
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attributes
        :param projection_expression: An array of DynamoProjectionExpression that identifies one or more attributes to retrieve from the table. These attributes can include scalars, sets, or elements of a JSON document. Default: - No projection expression
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param sort_key: A attribute representing the sort key of the item to retrieve. Default: - No sort key

        stability
        :stability: experimental
        """
        props = DynamoGetItemProps(partition_key=partition_key, table_name=table_name, consistent_read=consistent_read, expression_attribute_names=expression_attribute_names, projection_expression=projection_expression, return_consumed_capacity=return_consumed_capacity, sort_key=sort_key)

        jsii.create(DynamoGetItem, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoGetItemProps", jsii_struct_bases=[], name_mapping={'partition_key': 'partitionKey', 'table_name': 'tableName', 'consistent_read': 'consistentRead', 'expression_attribute_names': 'expressionAttributeNames', 'projection_expression': 'projectionExpression', 'return_consumed_capacity': 'returnConsumedCapacity', 'sort_key': 'sortKey'})
class DynamoGetItemProps():
    def __init__(self, *, partition_key: "DynamoAttribute", table_name: str, consistent_read: typing.Optional[bool]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, projection_expression: typing.Optional[typing.List["DynamoProjectionExpression"]]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, sort_key: typing.Optional["DynamoAttribute"]=None) -> None:
        """Properties for DynamoGetItem Task.

        :param partition_key: A attribute representing the partition key of the item to retrieve.
        :param table_name: The name of the table containing the requested item.
        :param consistent_read: Determines the read consistency model: If set to true, then the operation uses strongly consistent reads; otherwise, the operation uses eventually consistent reads. Default: false
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attributes
        :param projection_expression: An array of DynamoProjectionExpression that identifies one or more attributes to retrieve from the table. These attributes can include scalars, sets, or elements of a JSON document. Default: - No projection expression
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param sort_key: A attribute representing the sort key of the item to retrieve. Default: - No sort key

        stability
        :stability: experimental
        """
        if isinstance(partition_key, dict): partition_key = DynamoAttribute(**partition_key)
        if isinstance(sort_key, dict): sort_key = DynamoAttribute(**sort_key)
        self._values = {
            'partition_key': partition_key,
            'table_name': table_name,
        }
        if consistent_read is not None: self._values["consistent_read"] = consistent_read
        if expression_attribute_names is not None: self._values["expression_attribute_names"] = expression_attribute_names
        if projection_expression is not None: self._values["projection_expression"] = projection_expression
        if return_consumed_capacity is not None: self._values["return_consumed_capacity"] = return_consumed_capacity
        if sort_key is not None: self._values["sort_key"] = sort_key

    @builtins.property
    def partition_key(self) -> "DynamoAttribute":
        """A attribute representing the partition key of the item to retrieve.

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-Key
        stability
        :stability: experimental
        """
        return self._values.get('partition_key')

    @builtins.property
    def table_name(self) -> str:
        """The name of the table containing the requested item.

        stability
        :stability: experimental
        """
        return self._values.get('table_name')

    @builtins.property
    def consistent_read(self) -> typing.Optional[bool]:
        """Determines the read consistency model: If set to true, then the operation uses strongly consistent reads;

        otherwise, the operation uses eventually consistent reads.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('consistent_read')

    @builtins.property
    def expression_attribute_names(self) -> typing.Optional[typing.Mapping[str, str]]:
        """One or more substitution tokens for attribute names in an expression.

        default
        :default: - No expression attributes

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-ExpressionAttributeNames
        stability
        :stability: experimental
        """
        return self._values.get('expression_attribute_names')

    @builtins.property
    def projection_expression(self) -> typing.Optional[typing.List["DynamoProjectionExpression"]]:
        """An array of DynamoProjectionExpression that identifies one or more attributes to retrieve from the table.

        These attributes can include scalars, sets, or elements of a JSON document.

        default
        :default: - No projection expression

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-ProjectionExpression
        stability
        :stability: experimental
        """
        return self._values.get('projection_expression')

    @builtins.property
    def return_consumed_capacity(self) -> typing.Optional["DynamoConsumedCapacity"]:
        """Determines the level of detail about provisioned throughput consumption that is returned in the response.

        default
        :default: DynamoConsumedCapacity.NONE

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-ReturnConsumedCapacity
        stability
        :stability: experimental
        """
        return self._values.get('return_consumed_capacity')

    @builtins.property
    def sort_key(self) -> typing.Optional["DynamoAttribute"]:
        """A attribute representing the sort key of the item to retrieve.

        default
        :default: - No sort key

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-Key
        stability
        :stability: experimental
        """
        return self._values.get('sort_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoGetItemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoItemCollectionMetrics")
class DynamoItemCollectionMetrics(enum.Enum):
    """Determines whether item collection metrics are returned.

    stability
    :stability: experimental
    """
    SIZE = "SIZE"
    """If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """If set to NONE, no statistics are returned.

    stability
    :stability: experimental
    """

class DynamoProjectionExpression(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoProjectionExpression"):
    """Class to generate projection expression.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(DynamoProjectionExpression, self, [])

    @jsii.member(jsii_name="atIndex")
    def at_index(self, index: jsii.Number) -> "DynamoProjectionExpression":
        """Adds the array literal access for passed index.

        :param index: array index.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "atIndex", [index])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """converts and return the string expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="withAttribute")
    def with_attribute(self, attr: str) -> "DynamoProjectionExpression":
        """Adds the passed attribute to the chain.

        :param attr: Attribute name.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "withAttribute", [attr])


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class DynamoPutItem(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoPutItem"):
    """A StepFunctions task to call DynamoPutItem.

    stability
    :stability: experimental
    """
    def __init__(self, *, item: "DynamoAttributeValueMap", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None) -> None:
        """
        :param item: A map of attribute name/value pairs, one for each attribute. Only the primary key attributes are required; you can optionally provide other attribute name-value pairs for the item.
        :param table_name: The name of the table where the item should be writen .
        :param condition_expression: A condition that must be satisfied in order for a conditional PutItem operation to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: The item collection metrics to returned in the response. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were updated with the PutItem request. Default: DynamoReturnValues.NONE

        stability
        :stability: experimental
        """
        props = DynamoPutItemProps(item=item, table_name=table_name, condition_expression=condition_expression, expression_attribute_names=expression_attribute_names, expression_attribute_values=expression_attribute_values, return_consumed_capacity=return_consumed_capacity, return_item_collection_metrics=return_item_collection_metrics, return_values=return_values)

        jsii.create(DynamoPutItem, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoPutItemProps", jsii_struct_bases=[], name_mapping={'item': 'item', 'table_name': 'tableName', 'condition_expression': 'conditionExpression', 'expression_attribute_names': 'expressionAttributeNames', 'expression_attribute_values': 'expressionAttributeValues', 'return_consumed_capacity': 'returnConsumedCapacity', 'return_item_collection_metrics': 'returnItemCollectionMetrics', 'return_values': 'returnValues'})
class DynamoPutItemProps():
    def __init__(self, *, item: "DynamoAttributeValueMap", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None) -> None:
        """Properties for DynamoPutItem Task.

        :param item: A map of attribute name/value pairs, one for each attribute. Only the primary key attributes are required; you can optionally provide other attribute name-value pairs for the item.
        :param table_name: The name of the table where the item should be writen .
        :param condition_expression: A condition that must be satisfied in order for a conditional PutItem operation to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: The item collection metrics to returned in the response. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were updated with the PutItem request. Default: DynamoReturnValues.NONE

        stability
        :stability: experimental
        """
        if isinstance(item, dict): item = DynamoAttributeValueMap(**item)
        if isinstance(expression_attribute_values, dict): expression_attribute_values = DynamoAttributeValueMap(**expression_attribute_values)
        self._values = {
            'item': item,
            'table_name': table_name,
        }
        if condition_expression is not None: self._values["condition_expression"] = condition_expression
        if expression_attribute_names is not None: self._values["expression_attribute_names"] = expression_attribute_names
        if expression_attribute_values is not None: self._values["expression_attribute_values"] = expression_attribute_values
        if return_consumed_capacity is not None: self._values["return_consumed_capacity"] = return_consumed_capacity
        if return_item_collection_metrics is not None: self._values["return_item_collection_metrics"] = return_item_collection_metrics
        if return_values is not None: self._values["return_values"] = return_values

    @builtins.property
    def item(self) -> "DynamoAttributeValueMap":
        """A map of attribute name/value pairs, one for each attribute.

        Only the primary key attributes are required;
        you can optionally provide other attribute name-value pairs for the item.

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-Item
        stability
        :stability: experimental
        """
        return self._values.get('item')

    @builtins.property
    def table_name(self) -> str:
        """The name of the table where the item should be writen .

        stability
        :stability: experimental
        """
        return self._values.get('table_name')

    @builtins.property
    def condition_expression(self) -> typing.Optional[str]:
        """A condition that must be satisfied in order for a conditional PutItem operation to succeed.

        default
        :default: - No condition expression

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ConditionExpression
        stability
        :stability: experimental
        """
        return self._values.get('condition_expression')

    @builtins.property
    def expression_attribute_names(self) -> typing.Optional[typing.Mapping[str, str]]:
        """One or more substitution tokens for attribute names in an expression.

        default
        :default: - No expression attribute names

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ExpressionAttributeNames
        stability
        :stability: experimental
        """
        return self._values.get('expression_attribute_names')

    @builtins.property
    def expression_attribute_values(self) -> typing.Optional["DynamoAttributeValueMap"]:
        """One or more values that can be substituted in an expression.

        default
        :default: - No expression attribute values

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ExpressionAttributeValues
        stability
        :stability: experimental
        """
        return self._values.get('expression_attribute_values')

    @builtins.property
    def return_consumed_capacity(self) -> typing.Optional["DynamoConsumedCapacity"]:
        """Determines the level of detail about provisioned throughput consumption that is returned in the response.

        default
        :default: DynamoConsumedCapacity.NONE

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ReturnConsumedCapacity
        stability
        :stability: experimental
        """
        return self._values.get('return_consumed_capacity')

    @builtins.property
    def return_item_collection_metrics(self) -> typing.Optional["DynamoItemCollectionMetrics"]:
        """The item collection metrics to returned in the response.

        default
        :default: DynamoItemCollectionMetrics.NONE

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html#LSI.ItemCollections
        stability
        :stability: experimental
        """
        return self._values.get('return_item_collection_metrics')

    @builtins.property
    def return_values(self) -> typing.Optional["DynamoReturnValues"]:
        """Use ReturnValues if you want to get the item attributes as they appeared before they were updated with the PutItem request.

        default
        :default: DynamoReturnValues.NONE

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ReturnValues
        stability
        :stability: experimental
        """
        return self._values.get('return_values')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoPutItemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoReturnValues")
class DynamoReturnValues(enum.Enum):
    """Use ReturnValues if you want to get the item attributes as they appear before or after they are changed.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """Nothing is returned.

    stability
    :stability: experimental
    """
    ALL_OLD = "ALL_OLD"
    """Returns all of the attributes of the item.

    stability
    :stability: experimental
    """
    UPDATED_OLD = "UPDATED_OLD"
    """Returns only the updated attributes.

    stability
    :stability: experimental
    """
    ALL_NEW = "ALL_NEW"
    """Returns all of the attributes of the item.

    stability
    :stability: experimental
    """
    UPDATED_NEW = "UPDATED_NEW"
    """Returns only the updated attributes.

    stability
    :stability: experimental
    """

@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class DynamoUpdateItem(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoUpdateItem"):
    """A StepFunctions task to call DynamoUpdateItem.

    stability
    :stability: experimental
    """
    def __init__(self, *, partition_key: "DynamoAttribute", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None, sort_key: typing.Optional["DynamoAttribute"]=None, update_expression: typing.Optional[str]=None) -> None:
        """
        :param partition_key: The partition key of the item to be updated.
        :param table_name: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param sort_key: The sort key of the item to be updated. Default: - No sort key
        :param update_expression: An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them. Default: - No update expression

        stability
        :stability: experimental
        """
        props = DynamoUpdateItemProps(partition_key=partition_key, table_name=table_name, condition_expression=condition_expression, expression_attribute_names=expression_attribute_names, expression_attribute_values=expression_attribute_values, return_consumed_capacity=return_consumed_capacity, return_item_collection_metrics=return_item_collection_metrics, return_values=return_values, sort_key=sort_key, update_expression=update_expression)

        jsii.create(DynamoUpdateItem, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoUpdateItemProps", jsii_struct_bases=[], name_mapping={'partition_key': 'partitionKey', 'table_name': 'tableName', 'condition_expression': 'conditionExpression', 'expression_attribute_names': 'expressionAttributeNames', 'expression_attribute_values': 'expressionAttributeValues', 'return_consumed_capacity': 'returnConsumedCapacity', 'return_item_collection_metrics': 'returnItemCollectionMetrics', 'return_values': 'returnValues', 'sort_key': 'sortKey', 'update_expression': 'updateExpression'})
class DynamoUpdateItemProps():
    def __init__(self, *, partition_key: "DynamoAttribute", table_name: str, condition_expression: typing.Optional[str]=None, expression_attribute_names: typing.Optional[typing.Mapping[str, str]]=None, expression_attribute_values: typing.Optional["DynamoAttributeValueMap"]=None, return_consumed_capacity: typing.Optional["DynamoConsumedCapacity"]=None, return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"]=None, return_values: typing.Optional["DynamoReturnValues"]=None, sort_key: typing.Optional["DynamoAttribute"]=None, update_expression: typing.Optional[str]=None) -> None:
        """Properties for DynamoUpdateItem Task.

        :param partition_key: The partition key of the item to be updated.
        :param table_name: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param sort_key: The sort key of the item to be updated. Default: - No sort key
        :param update_expression: An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them. Default: - No update expression

        stability
        :stability: experimental
        """
        if isinstance(partition_key, dict): partition_key = DynamoAttribute(**partition_key)
        if isinstance(expression_attribute_values, dict): expression_attribute_values = DynamoAttributeValueMap(**expression_attribute_values)
        if isinstance(sort_key, dict): sort_key = DynamoAttribute(**sort_key)
        self._values = {
            'partition_key': partition_key,
            'table_name': table_name,
        }
        if condition_expression is not None: self._values["condition_expression"] = condition_expression
        if expression_attribute_names is not None: self._values["expression_attribute_names"] = expression_attribute_names
        if expression_attribute_values is not None: self._values["expression_attribute_values"] = expression_attribute_values
        if return_consumed_capacity is not None: self._values["return_consumed_capacity"] = return_consumed_capacity
        if return_item_collection_metrics is not None: self._values["return_item_collection_metrics"] = return_item_collection_metrics
        if return_values is not None: self._values["return_values"] = return_values
        if sort_key is not None: self._values["sort_key"] = sort_key
        if update_expression is not None: self._values["update_expression"] = update_expression

    @builtins.property
    def partition_key(self) -> "DynamoAttribute":
        """The partition key of the item to be updated.

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-Key
        stability
        :stability: experimental
        """
        return self._values.get('partition_key')

    @builtins.property
    def table_name(self) -> str:
        """The name of the table containing the requested item.

        stability
        :stability: experimental
        """
        return self._values.get('table_name')

    @builtins.property
    def condition_expression(self) -> typing.Optional[str]:
        """A condition that must be satisfied in order for a conditional DeleteItem to succeed.

        default
        :default: - No condition expression

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ConditionExpression
        stability
        :stability: experimental
        """
        return self._values.get('condition_expression')

    @builtins.property
    def expression_attribute_names(self) -> typing.Optional[typing.Mapping[str, str]]:
        """One or more substitution tokens for attribute names in an expression.

        default
        :default: - No expression attribute names

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ExpressionAttributeNames
        stability
        :stability: experimental
        """
        return self._values.get('expression_attribute_names')

    @builtins.property
    def expression_attribute_values(self) -> typing.Optional["DynamoAttributeValueMap"]:
        """One or more values that can be substituted in an expression.

        default
        :default: - No expression attribute values

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ExpressionAttributeValues
        stability
        :stability: experimental
        """
        return self._values.get('expression_attribute_values')

    @builtins.property
    def return_consumed_capacity(self) -> typing.Optional["DynamoConsumedCapacity"]:
        """Determines the level of detail about provisioned throughput consumption that is returned in the response.

        default
        :default: DynamoConsumedCapacity.NONE

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ReturnConsumedCapacity
        stability
        :stability: experimental
        """
        return self._values.get('return_consumed_capacity')

    @builtins.property
    def return_item_collection_metrics(self) -> typing.Optional["DynamoItemCollectionMetrics"]:
        """Determines whether item collection metrics are returned.

        If set to SIZE, the response includes statistics about item collections, if any,
        that were modified during the operation are returned in the response.
        If set to NONE (the default), no statistics are returned.

        default
        :default: DynamoItemCollectionMetrics.NONE

        stability
        :stability: experimental
        """
        return self._values.get('return_item_collection_metrics')

    @builtins.property
    def return_values(self) -> typing.Optional["DynamoReturnValues"]:
        """Use ReturnValues if you want to get the item attributes as they appeared before they were deleted.

        default
        :default: DynamoReturnValues.NONE

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ReturnValues
        stability
        :stability: experimental
        """
        return self._values.get('return_values')

    @builtins.property
    def sort_key(self) -> typing.Optional["DynamoAttribute"]:
        """The sort key of the item to be updated.

        default
        :default: - No sort key

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-Key
        stability
        :stability: experimental
        """
        return self._values.get('sort_key')

    @builtins.property
    def update_expression(self) -> typing.Optional[str]:
        """An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them.

        default
        :default: - No update expression

        see
        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-UpdateExpression
        stability
        :stability: experimental
        """
        return self._values.get('update_expression')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoUpdateItemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EcsRunTaskBase(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsRunTaskBase"):
    """A StepFunctions Task to run a Task on ECS or Fargate.

    stability
    :stability: experimental
    """
    def __init__(self, *, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None) -> None:
        """
        :param parameters: Additional parameters to pass to the base task. Default: - No additional parameters passed
        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        props = EcsRunTaskBaseProps(parameters=parameters, cluster=cluster, task_definition=task_definition, container_overrides=container_overrides, integration_pattern=integration_pattern)

        jsii.create(EcsRunTaskBase, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])

    @jsii.member(jsii_name="configureAwsVpcNetworking")
    def _configure_aws_vpc_networking(self, vpc: aws_cdk.aws_ec2.IVpc, assign_public_ip: typing.Optional[bool]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None) -> None:
        """
        :param vpc: -
        :param assign_public_ip: -
        :param subnet_selection: -
        :param security_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "configureAwsVpcNetworking", [vpc, assign_public_ip, subnet_selection, security_group])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage allowed network traffic for this service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsRunTaskBaseProps", jsii_struct_bases=[CommonEcsRunTaskProps], name_mapping={'cluster': 'cluster', 'task_definition': 'taskDefinition', 'container_overrides': 'containerOverrides', 'integration_pattern': 'integrationPattern', 'parameters': 'parameters'})
class EcsRunTaskBaseProps(CommonEcsRunTaskProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> None:
        """Construction properties for the BaseRunTaskProps.

        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param parameters: Additional parameters to pass to the base task. Default: - No additional parameters passed

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if container_overrides is not None: self._values["container_overrides"] = container_overrides
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if parameters is not None: self._values["parameters"] = parameters

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The topic to run the task on.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List["ContainerOverride"]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        default
        :default: - No overrides

        stability
        :stability: experimental
        """
        return self._values.get('container_overrides')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call RunTask in ECS.

        The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Additional parameters to pass to the base task.

        default
        :default: - No additional parameters passed

        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsRunTaskBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EmrAddStep(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrAddStep"):
    """A Step Functions Task to add a Step to an EMR Cluster.

    The StepConfiguration is defined as Parameters in the state machine definition.

    OUTPUT: the StepId

    stability
    :stability: experimental
    """
    def __init__(self, *, cluster_id: str, jar: str, name: str, action_on_failure: typing.Optional["ActionOnFailure"]=None, args: typing.Optional[typing.List[str]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, main_class: typing.Optional[str]=None, properties: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """
        :param cluster_id: The ClusterId to add the Step to.
        :param jar: A path to a JAR file run during the step.
        :param name: The name of the Step.
        :param action_on_failure: The action to take when the cluster step fails. Default: CONTINUE
        :param args: A list of command line arguments passed to the JAR file's main function when executed. Default: No args
        :param integration_pattern: The service integration pattern indicates different ways to call AddStep. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC
        :param main_class: The name of the main class in the specified Java file. If not specified, the JAR file should specify a Main-Class in its manifest file. Default: No mainClass
        :param properties: A list of Java properties that are set when the step runs. You can use these properties to pass key value pairs to your main function. Default: No properties

        stability
        :stability: experimental
        """
        props = EmrAddStepProps(cluster_id=cluster_id, jar=jar, name=name, action_on_failure=action_on_failure, args=args, integration_pattern=integration_pattern, main_class=main_class, properties=properties)

        jsii.create(EmrAddStep, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrAddStepProps", jsii_struct_bases=[], name_mapping={'cluster_id': 'clusterId', 'jar': 'jar', 'name': 'name', 'action_on_failure': 'actionOnFailure', 'args': 'args', 'integration_pattern': 'integrationPattern', 'main_class': 'mainClass', 'properties': 'properties'})
class EmrAddStepProps():
    def __init__(self, *, cluster_id: str, jar: str, name: str, action_on_failure: typing.Optional["ActionOnFailure"]=None, args: typing.Optional[typing.List[str]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, main_class: typing.Optional[str]=None, properties: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Properties for EmrAddStep.

        :param cluster_id: The ClusterId to add the Step to.
        :param jar: A path to a JAR file run during the step.
        :param name: The name of the Step.
        :param action_on_failure: The action to take when the cluster step fails. Default: CONTINUE
        :param args: A list of command line arguments passed to the JAR file's main function when executed. Default: No args
        :param integration_pattern: The service integration pattern indicates different ways to call AddStep. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC
        :param main_class: The name of the main class in the specified Java file. If not specified, the JAR file should specify a Main-Class in its manifest file. Default: No mainClass
        :param properties: A list of Java properties that are set when the step runs. You can use these properties to pass key value pairs to your main function. Default: No properties

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_id': cluster_id,
            'jar': jar,
            'name': name,
        }
        if action_on_failure is not None: self._values["action_on_failure"] = action_on_failure
        if args is not None: self._values["args"] = args
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if main_class is not None: self._values["main_class"] = main_class
        if properties is not None: self._values["properties"] = properties

    @builtins.property
    def cluster_id(self) -> str:
        """The ClusterId to add the Step to.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_id')

    @builtins.property
    def jar(self) -> str:
        """A path to a JAR file run during the step.

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_HadoopJarStepConfig.html
        stability
        :stability: experimental
        """
        return self._values.get('jar')

    @builtins.property
    def name(self) -> str:
        """The name of the Step.

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_StepConfig.html
        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def action_on_failure(self) -> typing.Optional["ActionOnFailure"]:
        """The action to take when the cluster step fails.

        default
        :default: CONTINUE

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_StepConfig.html
        stability
        :stability: experimental
        """
        return self._values.get('action_on_failure')

    @builtins.property
    def args(self) -> typing.Optional[typing.List[str]]:
        """A list of command line arguments passed to the JAR file's main function when executed.

        default
        :default: No args

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_HadoopJarStepConfig.html
        stability
        :stability: experimental
        """
        return self._values.get('args')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call AddStep.

        The valid value is either FIRE_AND_FORGET or SYNC.

        default
        :default: SYNC

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def main_class(self) -> typing.Optional[str]:
        """The name of the main class in the specified Java file.

        If not specified, the JAR file should specify a Main-Class in its manifest file.

        default
        :default: No mainClass

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_HadoopJarStepConfig.html
        stability
        :stability: experimental
        """
        return self._values.get('main_class')

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of Java properties that are set when the step runs.

        You can use these properties to pass key value pairs to your main function.

        default
        :default: No properties

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_HadoopJarStepConfig.html
        stability
        :stability: experimental
        """
        return self._values.get('properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmrAddStepProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EmrCancelStep(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCancelStep"):
    """A Step Functions Task to to cancel a Step on an EMR Cluster.

    stability
    :stability: experimental
    """
    def __init__(self, *, cluster_id: str, step_id: str) -> None:
        """
        :param cluster_id: The ClusterId to update.
        :param step_id: The StepId to cancel.

        stability
        :stability: experimental
        """
        props = EmrCancelStepProps(cluster_id=cluster_id, step_id=step_id)

        jsii.create(EmrCancelStep, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCancelStepProps", jsii_struct_bases=[], name_mapping={'cluster_id': 'clusterId', 'step_id': 'stepId'})
class EmrCancelStepProps():
    def __init__(self, *, cluster_id: str, step_id: str) -> None:
        """Properties for EmrCancelStep.

        :param cluster_id: The ClusterId to update.
        :param step_id: The StepId to cancel.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_id': cluster_id,
            'step_id': step_id,
        }

    @builtins.property
    def cluster_id(self) -> str:
        """The ClusterId to update.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_id')

    @builtins.property
    def step_id(self) -> str:
        """The StepId to cancel.

        stability
        :stability: experimental
        """
        return self._values.get('step_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmrCancelStepProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EmrCreateCluster(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster"):
    """A Step Functions Task to create an EMR Cluster.

    The ClusterConfiguration is defined as Parameters in the state machine definition.

    OUTPUT: the ClusterId.

    stability
    :stability: experimental
    """
    def __init__(self, *, instances: "InstancesConfigProperty", name: str, additional_info: typing.Optional[str]=None, applications: typing.Optional[typing.List["ApplicationConfigProperty"]]=None, auto_scaling_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, bootstrap_actions: typing.Optional[typing.List["BootstrapActionConfigProperty"]]=None, cluster_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, configurations: typing.Optional[typing.List["ConfigurationProperty"]]=None, custom_ami_id: typing.Optional[str]=None, ebs_root_volume_size: typing.Optional[jsii.Number]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, kerberos_attributes: typing.Optional["KerberosAttributesProperty"]=None, log_uri: typing.Optional[str]=None, release_label: typing.Optional[str]=None, scale_down_behavior: typing.Optional["EmrClusterScaleDownBehavior"]=None, security_configuration: typing.Optional[str]=None, service_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, visible_to_all_users: typing.Optional[bool]=None) -> None:
        """
        :param instances: A specification of the number and type of Amazon EC2 instances.
        :param name: The Name of the Cluster.
        :param additional_info: A JSON string for selecting additional features. Default: No additionalInfo
        :param applications: A case-insensitive list of applications for Amazon EMR to install and configure when launching the cluster. Default: EMR selected default
        :param auto_scaling_role: An IAM role for automatic scaling policies. A Role will be created if one is not provided. Default: No autoScalingRole
        :param bootstrap_actions: A list of bootstrap actions to run before Hadoop starts on the cluster nodes. Default: No bootstrapActions
        :param cluster_role: Also called instance profile and EC2 role. An IAM role for an EMR cluster. The EC2 instances of the cluster assume this role. This attribute has been renamed from jobFlowRole to clusterRole to align with other ERM/StepFunction integration parameters. A Role will be created if one is not provided. Default: No clusterRole
        :param configurations: The list of configurations supplied for the EMR cluster you are creating. Default: No configurations
        :param custom_ami_id: The ID of a custom Amazon EBS-backed Linux AMI. Default: No customAmiId
        :param ebs_root_volume_size: The size, in GiB, of the EBS root device volume of the Linux AMI that is used for each EC2 instance. Default: EMR selected default
        :param integration_pattern: The service integration pattern indicates different ways to call CreateCluster. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC
        :param kerberos_attributes: Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration. Default: No kerberosAttributes
        :param log_uri: The location in Amazon S3 to write the log files of the job flow. Default: No logUri
        :param release_label: The Amazon EMR release label, which determines the version of open-source application packages installed on the cluster. Default: EMR selected default
        :param scale_down_behavior: Specifies the way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized. Default: EMR selected default
        :param security_configuration: The name of a security configuration to apply to the cluster. Default: No securityConfiguration
        :param service_role: The IAM role that will be assumed by the Amazon EMR service to access AWS resources on your behalf. A Role will be created if one is not provided. Default: No serviceRole
        :param tags: A list of tags to associate with a cluster and propagate to Amazon EC2 instances. Default: No Tags
        :param visible_to_all_users: A value of true indicates that all IAM users in the AWS account can perform cluster actions if they have the proper IAM policy permissions. Default: true

        stability
        :stability: experimental
        """
        props = EmrCreateClusterProps(instances=instances, name=name, additional_info=additional_info, applications=applications, auto_scaling_role=auto_scaling_role, bootstrap_actions=bootstrap_actions, cluster_role=cluster_role, configurations=configurations, custom_ami_id=custom_ami_id, ebs_root_volume_size=ebs_root_volume_size, integration_pattern=integration_pattern, kerberos_attributes=kerberos_attributes, log_uri=log_uri, release_label=release_label, scale_down_behavior=scale_down_behavior, security_configuration=security_configuration, service_role=service_role, tags=tags, visible_to_all_users=visible_to_all_users)

        jsii.create(EmrCreateCluster, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])

    @builtins.property
    @jsii.member(jsii_name="autoScalingRole")
    def auto_scaling_role(self) -> aws_cdk.aws_iam.IRole:
        """The autoscaling role for the EMR Cluster.

        Only available after task has been added to a state machine.

        stability
        :stability: experimental
        """
        return jsii.get(self, "autoScalingRole")

    @builtins.property
    @jsii.member(jsii_name="clusterRole")
    def cluster_role(self) -> aws_cdk.aws_iam.IRole:
        """The instance role for the EMR Cluster.

        Only available after task has been added to a state machine.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterRole")

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> aws_cdk.aws_iam.IRole:
        """The service role for the EMR Cluster.

        Only available after task has been added to a state machine.

        stability
        :stability: experimental
        """
        return jsii.get(self, "serviceRole")

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ApplicationConfigProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'additional_info': 'additionalInfo', 'args': 'args', 'version': 'version'})
    class ApplicationConfigProperty():
        def __init__(self, *, name: str, additional_info: typing.Optional[typing.Mapping[str, str]]=None, args: typing.Optional[typing.List[str]]=None, version: typing.Optional[str]=None) -> None:
            """Properties for the EMR Cluster Applications.

            Applies to Amazon EMR releases 4.0 and later. A case-insensitive list of applications for Amazon EMR to install and configure when launching
            the cluster.

            See the RunJobFlow API for complete documentation on input parameters

            :param name: The name of the application.
            :param additional_info: This option is for advanced users only. This is meta information about third-party applications that third-party vendors use for testing purposes. Default: No additionalInfo
            :param args: Arguments for Amazon EMR to pass to the application. Default: No args
            :param version: The version of the application. Default: No version

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_Application.html
            stability
            :stability: experimental
            """
            self._values = {
                'name': name,
            }
            if additional_info is not None: self._values["additional_info"] = additional_info
            if args is not None: self._values["args"] = args
            if version is not None: self._values["version"] = version

        @builtins.property
        def name(self) -> str:
            """The name of the application.

            stability
            :stability: experimental
            """
            return self._values.get('name')

        @builtins.property
        def additional_info(self) -> typing.Optional[typing.Mapping[str, str]]:
            """This option is for advanced users only.

            This is meta information about third-party applications that third-party vendors use
            for testing purposes.

            default
            :default: No additionalInfo

            stability
            :stability: experimental
            """
            return self._values.get('additional_info')

        @builtins.property
        def args(self) -> typing.Optional[typing.List[str]]:
            """Arguments for Amazon EMR to pass to the application.

            default
            :default: No args

            stability
            :stability: experimental
            """
            return self._values.get('args')

        @builtins.property
        def version(self) -> typing.Optional[str]:
            """The version of the application.

            default
            :default: No version

            stability
            :stability: experimental
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ApplicationConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.AutoScalingPolicyProperty", jsii_struct_bases=[], name_mapping={'constraints': 'constraints', 'rules': 'rules'})
    class AutoScalingPolicyProperty():
        def __init__(self, *, constraints: "EmrCreateCluster.ScalingConstraintsProperty", rules: typing.List["EmrCreateCluster.ScalingRuleProperty"]) -> None:
            """An automatic scaling policy for a core instance group or task instance group in an Amazon EMR cluster.

            :param constraints: The upper and lower EC2 instance limits for an automatic scaling policy. Automatic scaling activity will not cause an instance group to grow above or below these limits.
            :param rules: The scale-in and scale-out rules that comprise the automatic scaling policy.

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_AutoScalingPolicy.html
            stability
            :stability: experimental
            """
            if isinstance(constraints, dict): constraints = EmrCreateCluster.ScalingConstraintsProperty(**constraints)
            self._values = {
                'constraints': constraints,
                'rules': rules,
            }

        @builtins.property
        def constraints(self) -> "EmrCreateCluster.ScalingConstraintsProperty":
            """The upper and lower EC2 instance limits for an automatic scaling policy.

            Automatic scaling activity will not cause an instance
            group to grow above or below these limits.

            stability
            :stability: experimental
            """
            return self._values.get('constraints')

        @builtins.property
        def rules(self) -> typing.List["EmrCreateCluster.ScalingRuleProperty"]:
            """The scale-in and scale-out rules that comprise the automatic scaling policy.

            stability
            :stability: experimental
            """
            return self._values.get('rules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AutoScalingPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.BootstrapActionConfigProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'script_bootstrap_action': 'scriptBootstrapAction'})
    class BootstrapActionConfigProperty():
        def __init__(self, *, name: str, script_bootstrap_action: "EmrCreateCluster.ScriptBootstrapActionConfigProperty") -> None:
            """Configuration of a bootstrap action.

            See the RunJobFlow API for complete documentation on input parameters

            :param name: The name of the bootstrap action.
            :param script_bootstrap_action: The script run by the bootstrap action.

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_BootstrapActionConfig.html
            stability
            :stability: experimental
            """
            if isinstance(script_bootstrap_action, dict): script_bootstrap_action = EmrCreateCluster.ScriptBootstrapActionConfigProperty(**script_bootstrap_action)
            self._values = {
                'name': name,
                'script_bootstrap_action': script_bootstrap_action,
            }

        @builtins.property
        def name(self) -> str:
            """The name of the bootstrap action.

            stability
            :stability: experimental
            """
            return self._values.get('name')

        @builtins.property
        def script_bootstrap_action(self) -> "EmrCreateCluster.ScriptBootstrapActionConfigProperty":
            """The script run by the bootstrap action.

            stability
            :stability: experimental
            """
            return self._values.get('script_bootstrap_action')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BootstrapActionConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.CloudWatchAlarmComparisonOperator")
    class CloudWatchAlarmComparisonOperator(enum.Enum):
        """CloudWatch Alarm Comparison Operators.

        stability
        :stability: experimental
        """
        GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
        """GREATER_THAN_OR_EQUAL.

        stability
        :stability: experimental
        """
        GREATER_THAN = "GREATER_THAN"
        """GREATER_THAN.

        stability
        :stability: experimental
        """
        LESS_THAN = "LESS_THAN"
        """LESS_THAN.

        stability
        :stability: experimental
        """
        LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
        """LESS_THAN_OR_EQUAL.

        stability
        :stability: experimental
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.CloudWatchAlarmDefinitionProperty", jsii_struct_bases=[], name_mapping={'comparison_operator': 'comparisonOperator', 'metric_name': 'metricName', 'period': 'period', 'dimensions': 'dimensions', 'evalution_periods': 'evalutionPeriods', 'namespace': 'namespace', 'statistic': 'statistic', 'threshold': 'threshold', 'unit': 'unit'})
    class CloudWatchAlarmDefinitionProperty():
        def __init__(self, *, comparison_operator: "EmrCreateCluster.CloudWatchAlarmComparisonOperator", metric_name: str, period: aws_cdk.core.Duration, dimensions: typing.Optional[typing.List["EmrCreateCluster.MetricDimensionProperty"]]=None, evalution_periods: typing.Optional[jsii.Number]=None, namespace: typing.Optional[str]=None, statistic: typing.Optional["EmrCreateCluster.CloudWatchAlarmStatistic"]=None, threshold: typing.Optional[jsii.Number]=None, unit: typing.Optional["EmrCreateCluster.CloudWatchAlarmUnit"]=None) -> None:
            """The definition of a CloudWatch metric alarm, which determines when an automatic scaling activity is triggered.

            When the defined alarm conditions
            are satisfied, scaling activity begins.

            :param comparison_operator: Determines how the metric specified by MetricName is compared to the value specified by Threshold.
            :param metric_name: The name of the CloudWatch metric that is watched to determine an alarm condition.
            :param period: The period, in seconds, over which the statistic is applied. EMR CloudWatch metrics are emitted every five minutes (300 seconds), so if an EMR CloudWatch metric is specified, specify 300.
            :param dimensions: A CloudWatch metric dimension. Default: No dimensions
            :param evalution_periods: The number of periods, in five-minute increments, during which the alarm condition must exist before the alarm triggers automatic scaling activity. The default value is 1. Default: No evaluationPeriods
            :param namespace: The namespace for the CloudWatch metric. The default is AWS/ElasticMapReduce. Default: No nampespace
            :param statistic: The statistic to apply to the metric associated with the alarm. The default is AVERAGE. Default: No statistic
            :param threshold: The value against which the specified statistic is compared. Default: No threshold
            :param unit: The unit of measure associated with the CloudWatch metric being watched. The value specified for Unit must correspond to the units specified in the CloudWatch metric. Default: No unit

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_CloudWatchAlarmDefinition.html
            stability
            :stability: experimental
            """
            self._values = {
                'comparison_operator': comparison_operator,
                'metric_name': metric_name,
                'period': period,
            }
            if dimensions is not None: self._values["dimensions"] = dimensions
            if evalution_periods is not None: self._values["evalution_periods"] = evalution_periods
            if namespace is not None: self._values["namespace"] = namespace
            if statistic is not None: self._values["statistic"] = statistic
            if threshold is not None: self._values["threshold"] = threshold
            if unit is not None: self._values["unit"] = unit

        @builtins.property
        def comparison_operator(self) -> "EmrCreateCluster.CloudWatchAlarmComparisonOperator":
            """Determines how the metric specified by MetricName is compared to the value specified by Threshold.

            stability
            :stability: experimental
            """
            return self._values.get('comparison_operator')

        @builtins.property
        def metric_name(self) -> str:
            """The name of the CloudWatch metric that is watched to determine an alarm condition.

            stability
            :stability: experimental
            """
            return self._values.get('metric_name')

        @builtins.property
        def period(self) -> aws_cdk.core.Duration:
            """The period, in seconds, over which the statistic is applied.

            EMR CloudWatch metrics are emitted every five minutes (300 seconds), so if
            an EMR CloudWatch metric is specified, specify 300.

            stability
            :stability: experimental
            """
            return self._values.get('period')

        @builtins.property
        def dimensions(self) -> typing.Optional[typing.List["EmrCreateCluster.MetricDimensionProperty"]]:
            """A CloudWatch metric dimension.

            default
            :default: No dimensions

            stability
            :stability: experimental
            """
            return self._values.get('dimensions')

        @builtins.property
        def evalution_periods(self) -> typing.Optional[jsii.Number]:
            """The number of periods, in five-minute increments, during which the alarm condition must exist before the alarm triggers automatic scaling activity.

            The default value is 1.

            default
            :default: No evaluationPeriods

            stability
            :stability: experimental
            """
            return self._values.get('evalution_periods')

        @builtins.property
        def namespace(self) -> typing.Optional[str]:
            """The namespace for the CloudWatch metric.

            The default is AWS/ElasticMapReduce.

            default
            :default: No nampespace

            stability
            :stability: experimental
            """
            return self._values.get('namespace')

        @builtins.property
        def statistic(self) -> typing.Optional["EmrCreateCluster.CloudWatchAlarmStatistic"]:
            """The statistic to apply to the metric associated with the alarm.

            The default is AVERAGE.

            default
            :default: No statistic

            stability
            :stability: experimental
            """
            return self._values.get('statistic')

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            """The value against which the specified statistic is compared.

            default
            :default: No threshold

            stability
            :stability: experimental
            """
            return self._values.get('threshold')

        @builtins.property
        def unit(self) -> typing.Optional["EmrCreateCluster.CloudWatchAlarmUnit"]:
            """The unit of measure associated with the CloudWatch metric being watched.

            The value specified for Unit must correspond to the units
            specified in the CloudWatch metric.

            default
            :default: No unit

            stability
            :stability: experimental
            """
            return self._values.get('unit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CloudWatchAlarmDefinitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.CloudWatchAlarmStatistic")
    class CloudWatchAlarmStatistic(enum.Enum):
        """CloudWatch Alarm Statistics.

        stability
        :stability: experimental
        """
        SAMPLE_COUNT = "SAMPLE_COUNT"
        """SAMPLE_COUNT.

        stability
        :stability: experimental
        """
        AVERAGE = "AVERAGE"
        """AVERAGE.

        stability
        :stability: experimental
        """
        SUM = "SUM"
        """SUM.

        stability
        :stability: experimental
        """
        MINIMUM = "MINIMUM"
        """MINIMUM.

        stability
        :stability: experimental
        """
        MAXIMUM = "MAXIMUM"
        """MAXIMUM.

        stability
        :stability: experimental
        """

    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.CloudWatchAlarmUnit")
    class CloudWatchAlarmUnit(enum.Enum):
        """CloudWatch Alarm Units.

        stability
        :stability: experimental
        """
        NONE = "NONE"
        """NONE.

        stability
        :stability: experimental
        """
        SECONDS = "SECONDS"
        """SECONDS.

        stability
        :stability: experimental
        """
        MICRO_SECONDS = "MICRO_SECONDS"
        """MICRO_SECONDS.

        stability
        :stability: experimental
        """
        MILLI_SECONDS = "MILLI_SECONDS"
        """MILLI_SECONDS.

        stability
        :stability: experimental
        """
        BYTES = "BYTES"
        """BYTES.

        stability
        :stability: experimental
        """
        KILO_BYTES = "KILO_BYTES"
        """KILO_BYTES.

        stability
        :stability: experimental
        """
        MEGA_BYTES = "MEGA_BYTES"
        """MEGA_BYTES.

        stability
        :stability: experimental
        """
        GIGA_BYTES = "GIGA_BYTES"
        """GIGA_BYTES.

        stability
        :stability: experimental
        """
        TERA_BYTES = "TERA_BYTES"
        """TERA_BYTES.

        stability
        :stability: experimental
        """
        BITS = "BITS"
        """BITS.

        stability
        :stability: experimental
        """
        KILO_BITS = "KILO_BITS"
        """KILO_BITS.

        stability
        :stability: experimental
        """
        MEGA_BITS = "MEGA_BITS"
        """MEGA_BITS.

        stability
        :stability: experimental
        """
        GIGA_BITS = "GIGA_BITS"
        """GIGA_BITS.

        stability
        :stability: experimental
        """
        TERA_BITS = "TERA_BITS"
        """TERA_BITS.

        stability
        :stability: experimental
        """
        PERCENT = "PERCENT"
        """PERCENT.

        stability
        :stability: experimental
        """
        COUNT = "COUNT"
        """COUNT.

        stability
        :stability: experimental
        """
        BYTES_PER_SECOND = "BYTES_PER_SECOND"
        """BYTES_PER_SECOND.

        stability
        :stability: experimental
        """
        KILO_BYTES_PER_SECOND = "KILO_BYTES_PER_SECOND"
        """KILO_BYTES_PER_SECOND.

        stability
        :stability: experimental
        """
        MEGA_BYTES_PER_SECOND = "MEGA_BYTES_PER_SECOND"
        """MEGA_BYTES_PER_SECOND.

        stability
        :stability: experimental
        """
        GIGA_BYTES_PER_SECOND = "GIGA_BYTES_PER_SECOND"
        """GIGA_BYTES_PER_SECOND.

        stability
        :stability: experimental
        """
        TERA_BYTES_PER_SECOND = "TERA_BYTES_PER_SECOND"
        """TERA_BYTES_PER_SECOND.

        stability
        :stability: experimental
        """
        BITS_PER_SECOND = "BITS_PER_SECOND"
        """BITS_PER_SECOND.

        stability
        :stability: experimental
        """
        KILO_BITS_PER_SECOND = "KILO_BITS_PER_SECOND"
        """KILO_BITS_PER_SECOND.

        stability
        :stability: experimental
        """
        MEGA_BITS_PER_SECOND = "MEGA_BITS_PER_SECOND"
        """MEGA_BITS_PER_SECOND.

        stability
        :stability: experimental
        """
        GIGA_BITS_PER_SECOND = "GIGA_BITS_PER_SECOND"
        """GIGA_BITS_PER_SECOND.

        stability
        :stability: experimental
        """
        TERA_BITS_PER_SECOND = "TERA_BITS_PER_SECOND"
        """TERA_BITS_PER_SECOND.

        stability
        :stability: experimental
        """
        COUNT_PER_SECOND = "COUNT_PER_SECOND"
        """COUNT_PER_SECOND.

        stability
        :stability: experimental
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ConfigurationProperty", jsii_struct_bases=[], name_mapping={'classification': 'classification', 'configurations': 'configurations', 'properties': 'properties'})
    class ConfigurationProperty():
        def __init__(self, *, classification: typing.Optional[str]=None, configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]=None, properties: typing.Optional[typing.Mapping[str, str]]=None) -> None:
            """An optional configuration specification to be used when provisioning cluster instances, which can include configurations for applications and software bundled with Amazon EMR.

            See the RunJobFlow API for complete documentation on input parameters

            :param classification: The classification within a configuration. Default: No classification
            :param configurations: A list of additional configurations to apply within a configuration object. Default: No configurations
            :param properties: A set of properties specified within a configuration classification. Default: No properties

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_Configuration.html
            stability
            :stability: experimental
            """
            self._values = {
            }
            if classification is not None: self._values["classification"] = classification
            if configurations is not None: self._values["configurations"] = configurations
            if properties is not None: self._values["properties"] = properties

        @builtins.property
        def classification(self) -> typing.Optional[str]:
            """The classification within a configuration.

            default
            :default: No classification

            stability
            :stability: experimental
            """
            return self._values.get('classification')

        @builtins.property
        def configurations(self) -> typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]:
            """A list of additional configurations to apply within a configuration object.

            default
            :default: No configurations

            stability
            :stability: experimental
            """
            return self._values.get('configurations')

        @builtins.property
        def properties(self) -> typing.Optional[typing.Mapping[str, str]]:
            """A set of properties specified within a configuration classification.

            default
            :default: No properties

            stability
            :stability: experimental
            """
            return self._values.get('properties')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.EbsBlockDeviceConfigProperty", jsii_struct_bases=[], name_mapping={'volume_specification': 'volumeSpecification', 'volumes_per_instance': 'volumesPerInstance'})
    class EbsBlockDeviceConfigProperty():
        def __init__(self, *, volume_specification: "EmrCreateCluster.VolumeSpecificationProperty", volumes_per_instance: typing.Optional[jsii.Number]=None) -> None:
            """Configuration of requested EBS block device associated with the instance group with count of volumes that will be associated to every instance.

            :param volume_specification: EBS volume specifications such as volume type, IOPS, and size (GiB) that will be requested for the EBS volume attached to an EC2 instance in the cluster.
            :param volumes_per_instance: Number of EBS volumes with a specific volume configuration that will be associated with every instance in the instance group. Default: EMR selected default

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_EbsBlockDeviceConfig.html
            stability
            :stability: experimental
            """
            if isinstance(volume_specification, dict): volume_specification = EmrCreateCluster.VolumeSpecificationProperty(**volume_specification)
            self._values = {
                'volume_specification': volume_specification,
            }
            if volumes_per_instance is not None: self._values["volumes_per_instance"] = volumes_per_instance

        @builtins.property
        def volume_specification(self) -> "EmrCreateCluster.VolumeSpecificationProperty":
            """EBS volume specifications such as volume type, IOPS, and size (GiB) that will be requested for the EBS volume attached to an EC2 instance in the cluster.

            stability
            :stability: experimental
            """
            return self._values.get('volume_specification')

        @builtins.property
        def volumes_per_instance(self) -> typing.Optional[jsii.Number]:
            """Number of EBS volumes with a specific volume configuration that will be associated with every instance in the instance group.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('volumes_per_instance')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EbsBlockDeviceConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.EbsBlockDeviceVolumeType")
    class EbsBlockDeviceVolumeType(enum.Enum):
        """EBS Volume Types.

        stability
        :stability: experimental
        """
        GP2 = "GP2"
        """gp2 Volume Type.

        stability
        :stability: experimental
        """
        IO1 = "IO1"
        """io1 Volume Type.

        stability
        :stability: experimental
        """
        STANDARD = "STANDARD"
        """Standard Volume Type.

        stability
        :stability: experimental
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.EbsConfigurationProperty", jsii_struct_bases=[], name_mapping={'ebs_block_device_configs': 'ebsBlockDeviceConfigs', 'ebs_optimized': 'ebsOptimized'})
    class EbsConfigurationProperty():
        def __init__(self, *, ebs_block_device_configs: typing.Optional[typing.List["EmrCreateCluster.EbsBlockDeviceConfigProperty"]]=None, ebs_optimized: typing.Optional[bool]=None) -> None:
            """The Amazon EBS configuration of a cluster instance.

            :param ebs_block_device_configs: An array of Amazon EBS volume specifications attached to a cluster instance. Default: No ebsBlockDeviceConfigs
            :param ebs_optimized: Indicates whether an Amazon EBS volume is EBS-optimized. Default: EMR selected default

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_EbsConfiguration.html
            stability
            :stability: experimental
            """
            self._values = {
            }
            if ebs_block_device_configs is not None: self._values["ebs_block_device_configs"] = ebs_block_device_configs
            if ebs_optimized is not None: self._values["ebs_optimized"] = ebs_optimized

        @builtins.property
        def ebs_block_device_configs(self) -> typing.Optional[typing.List["EmrCreateCluster.EbsBlockDeviceConfigProperty"]]:
            """An array of Amazon EBS volume specifications attached to a cluster instance.

            default
            :default: No ebsBlockDeviceConfigs

            stability
            :stability: experimental
            """
            return self._values.get('ebs_block_device_configs')

        @builtins.property
        def ebs_optimized(self) -> typing.Optional[bool]:
            """Indicates whether an Amazon EBS volume is EBS-optimized.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('ebs_optimized')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EbsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.EmrClusterScaleDownBehavior")
    class EmrClusterScaleDownBehavior(enum.Enum):
        """Valid valus for the Cluster ScaleDownBehavior.

        stability
        :stability: experimental
        """
        TERMINATE_AT_INSTANCE_HOUR = "TERMINATE_AT_INSTANCE_HOUR"
        """Indicates that Amazon EMR terminates nodes at the instance-hour boundary, regardless of when the request to terminate the instance was submitted.

        This option is only available with Amazon EMR 5.1.0 and later and is the default for clusters created using that version

        stability
        :stability: experimental
        """
        TERMINATE_AT_TASK_COMPLETION = "TERMINATE_AT_TASK_COMPLETION"
        """Indicates that Amazon EMR blacklists and drains tasks from nodes before terminating the Amazon EC2 instances, regardless of the instance-hour boundary.

        stability
        :stability: experimental
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceFleetConfigProperty", jsii_struct_bases=[], name_mapping={'instance_fleet_type': 'instanceFleetType', 'instance_type_configs': 'instanceTypeConfigs', 'launch_specifications': 'launchSpecifications', 'name': 'name', 'target_on_demand_capacity': 'targetOnDemandCapacity', 'target_spot_capacity': 'targetSpotCapacity'})
    class InstanceFleetConfigProperty():
        def __init__(self, *, instance_fleet_type: "EmrCreateCluster.InstanceRoleType", instance_type_configs: typing.Optional[typing.List["EmrCreateCluster.InstanceTypeConfigProperty"]]=None, launch_specifications: typing.Optional["EmrCreateCluster.InstanceFleetProvisioningSpecificationsProperty"]=None, name: typing.Optional[str]=None, target_on_demand_capacity: typing.Optional[jsii.Number]=None, target_spot_capacity: typing.Optional[jsii.Number]=None) -> None:
            """The configuration that defines an instance fleet.

            :param instance_fleet_type: The node type that the instance fleet hosts. Valid values are MASTER,CORE,and TASK.
            :param instance_type_configs: The instance type configurations that define the EC2 instances in the instance fleet. Default: No instanceTpeConfigs
            :param launch_specifications: The launch specification for the instance fleet. Default: No launchSpecifications
            :param name: The friendly name of the instance fleet. Default: No name
            :param target_on_demand_capacity: The target capacity of On-Demand units for the instance fleet, which determines how many On-Demand instances to provision. Default: No targetOnDemandCapacity
            :param target_spot_capacity: The target capacity of Spot units for the instance fleet, which determines how many Spot instances to provision. Default: No targetSpotCapacity

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceFleetConfig.html
            stability
            :stability: experimental
            """
            if isinstance(launch_specifications, dict): launch_specifications = EmrCreateCluster.InstanceFleetProvisioningSpecificationsProperty(**launch_specifications)
            self._values = {
                'instance_fleet_type': instance_fleet_type,
            }
            if instance_type_configs is not None: self._values["instance_type_configs"] = instance_type_configs
            if launch_specifications is not None: self._values["launch_specifications"] = launch_specifications
            if name is not None: self._values["name"] = name
            if target_on_demand_capacity is not None: self._values["target_on_demand_capacity"] = target_on_demand_capacity
            if target_spot_capacity is not None: self._values["target_spot_capacity"] = target_spot_capacity

        @builtins.property
        def instance_fleet_type(self) -> "EmrCreateCluster.InstanceRoleType":
            """The node type that the instance fleet hosts.

            Valid values are MASTER,CORE,and TASK.

            stability
            :stability: experimental
            """
            return self._values.get('instance_fleet_type')

        @builtins.property
        def instance_type_configs(self) -> typing.Optional[typing.List["EmrCreateCluster.InstanceTypeConfigProperty"]]:
            """The instance type configurations that define the EC2 instances in the instance fleet.

            default
            :default: No instanceTpeConfigs

            stability
            :stability: experimental
            """
            return self._values.get('instance_type_configs')

        @builtins.property
        def launch_specifications(self) -> typing.Optional["EmrCreateCluster.InstanceFleetProvisioningSpecificationsProperty"]:
            """The launch specification for the instance fleet.

            default
            :default: No launchSpecifications

            stability
            :stability: experimental
            """
            return self._values.get('launch_specifications')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """The friendly name of the instance fleet.

            default
            :default: No name

            stability
            :stability: experimental
            """
            return self._values.get('name')

        @builtins.property
        def target_on_demand_capacity(self) -> typing.Optional[jsii.Number]:
            """The target capacity of On-Demand units for the instance fleet, which determines how many On-Demand instances to provision.

            default
            :default: No targetOnDemandCapacity

            stability
            :stability: experimental
            """
            return self._values.get('target_on_demand_capacity')

        @builtins.property
        def target_spot_capacity(self) -> typing.Optional[jsii.Number]:
            """The target capacity of Spot units for the instance fleet, which determines how many Spot instances to provision.

            default
            :default: No targetSpotCapacity

            stability
            :stability: experimental
            """
            return self._values.get('target_spot_capacity')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstanceFleetConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceFleetProvisioningSpecificationsProperty", jsii_struct_bases=[], name_mapping={'spot_specification': 'spotSpecification'})
    class InstanceFleetProvisioningSpecificationsProperty():
        def __init__(self, *, spot_specification: "EmrCreateCluster.SpotProvisioningSpecificationProperty") -> None:
            """The launch specification for Spot instances in the fleet, which determines the defined duration and provisioning timeout behavior.

            :param spot_specification: The launch specification for Spot instances in the fleet, which determines the defined duration and provisioning timeout behavior.

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceFleetProvisioningSpecifications.html
            stability
            :stability: experimental
            """
            if isinstance(spot_specification, dict): spot_specification = EmrCreateCluster.SpotProvisioningSpecificationProperty(**spot_specification)
            self._values = {
                'spot_specification': spot_specification,
            }

        @builtins.property
        def spot_specification(self) -> "EmrCreateCluster.SpotProvisioningSpecificationProperty":
            """The launch specification for Spot instances in the fleet, which determines the defined duration and provisioning timeout behavior.

            stability
            :stability: experimental
            """
            return self._values.get('spot_specification')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstanceFleetProvisioningSpecificationsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceGroupConfigProperty", jsii_struct_bases=[], name_mapping={'instance_count': 'instanceCount', 'instance_role': 'instanceRole', 'instance_type': 'instanceType', 'auto_scaling_policy': 'autoScalingPolicy', 'bid_price': 'bidPrice', 'configurations': 'configurations', 'ebs_configuration': 'ebsConfiguration', 'market': 'market', 'name': 'name'})
    class InstanceGroupConfigProperty():
        def __init__(self, *, instance_count: jsii.Number, instance_role: "EmrCreateCluster.InstanceRoleType", instance_type: str, auto_scaling_policy: typing.Optional["EmrCreateCluster.AutoScalingPolicyProperty"]=None, bid_price: typing.Optional[str]=None, configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]=None, ebs_configuration: typing.Optional["EmrCreateCluster.EbsConfigurationProperty"]=None, market: typing.Optional["EmrCreateCluster.InstanceMarket"]=None, name: typing.Optional[str]=None) -> None:
            """Configuration defining a new instance group.

            :param instance_count: Target number of instances for the instance group.
            :param instance_role: The role of the instance group in the cluster.
            :param instance_type: The EC2 instance type for all instances in the instance group.
            :param auto_scaling_policy: An automatic scaling policy for a core instance group or task instance group in an Amazon EMR cluster. Default: No autoScalingPolicy
            :param bid_price: The bid price for each EC2 Spot instance type as defined by InstanceType. Expressed in USD. Default: No bidPrice
            :param configurations: The list of configurations supplied for an EMR cluster instance group. Default: No configurations
            :param ebs_configuration: EBS configurations that will be attached to each EC2 instance in the instance group. Default: No ebsConfiguration
            :param market: Market type of the EC2 instances used to create a cluster node. Default: EMR selected default
            :param name: Friendly name given to the instance group. Default: No name

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceGroupConfig.html
            stability
            :stability: experimental
            """
            if isinstance(auto_scaling_policy, dict): auto_scaling_policy = EmrCreateCluster.AutoScalingPolicyProperty(**auto_scaling_policy)
            if isinstance(ebs_configuration, dict): ebs_configuration = EmrCreateCluster.EbsConfigurationProperty(**ebs_configuration)
            self._values = {
                'instance_count': instance_count,
                'instance_role': instance_role,
                'instance_type': instance_type,
            }
            if auto_scaling_policy is not None: self._values["auto_scaling_policy"] = auto_scaling_policy
            if bid_price is not None: self._values["bid_price"] = bid_price
            if configurations is not None: self._values["configurations"] = configurations
            if ebs_configuration is not None: self._values["ebs_configuration"] = ebs_configuration
            if market is not None: self._values["market"] = market
            if name is not None: self._values["name"] = name

        @builtins.property
        def instance_count(self) -> jsii.Number:
            """Target number of instances for the instance group.

            stability
            :stability: experimental
            """
            return self._values.get('instance_count')

        @builtins.property
        def instance_role(self) -> "EmrCreateCluster.InstanceRoleType":
            """The role of the instance group in the cluster.

            stability
            :stability: experimental
            """
            return self._values.get('instance_role')

        @builtins.property
        def instance_type(self) -> str:
            """The EC2 instance type for all instances in the instance group.

            stability
            :stability: experimental
            """
            return self._values.get('instance_type')

        @builtins.property
        def auto_scaling_policy(self) -> typing.Optional["EmrCreateCluster.AutoScalingPolicyProperty"]:
            """An automatic scaling policy for a core instance group or task instance group in an Amazon EMR cluster.

            default
            :default: No autoScalingPolicy

            stability
            :stability: experimental
            """
            return self._values.get('auto_scaling_policy')

        @builtins.property
        def bid_price(self) -> typing.Optional[str]:
            """The bid price for each EC2 Spot instance type as defined by InstanceType.

            Expressed in USD.

            default
            :default: No bidPrice

            stability
            :stability: experimental
            """
            return self._values.get('bid_price')

        @builtins.property
        def configurations(self) -> typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]:
            """The list of configurations supplied for an EMR cluster instance group.

            default
            :default: No configurations

            stability
            :stability: experimental
            """
            return self._values.get('configurations')

        @builtins.property
        def ebs_configuration(self) -> typing.Optional["EmrCreateCluster.EbsConfigurationProperty"]:
            """EBS configurations that will be attached to each EC2 instance in the instance group.

            default
            :default: No ebsConfiguration

            stability
            :stability: experimental
            """
            return self._values.get('ebs_configuration')

        @builtins.property
        def market(self) -> typing.Optional["EmrCreateCluster.InstanceMarket"]:
            """Market type of the EC2 instances used to create a cluster node.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('market')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """Friendly name given to the instance group.

            default
            :default: No name

            stability
            :stability: experimental
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstanceGroupConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceMarket")
    class InstanceMarket(enum.Enum):
        """EC2 Instance Market.

        stability
        :stability: experimental
        """
        ON_DEMAND = "ON_DEMAND"
        """On Demand Instance.

        stability
        :stability: experimental
        """
        SPOT = "SPOT"
        """Spot Instance.

        stability
        :stability: experimental
        """

    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceRoleType")
    class InstanceRoleType(enum.Enum):
        """Instance Role Types.

        stability
        :stability: experimental
        """
        MASTER = "MASTER"
        """Master Node.

        stability
        :stability: experimental
        """
        CORE = "CORE"
        """Core Node.

        stability
        :stability: experimental
        """
        TASK = "TASK"
        """Task Node.

        stability
        :stability: experimental
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceTypeConfigProperty", jsii_struct_bases=[], name_mapping={'instance_type': 'instanceType', 'bid_price': 'bidPrice', 'bid_price_as_percentage_of_on_demand_price': 'bidPriceAsPercentageOfOnDemandPrice', 'configurations': 'configurations', 'ebs_configuration': 'ebsConfiguration', 'weighted_capacity': 'weightedCapacity'})
    class InstanceTypeConfigProperty():
        def __init__(self, *, instance_type: str, bid_price: typing.Optional[str]=None, bid_price_as_percentage_of_on_demand_price: typing.Optional[jsii.Number]=None, configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]=None, ebs_configuration: typing.Optional["EmrCreateCluster.EbsConfigurationProperty"]=None, weighted_capacity: typing.Optional[jsii.Number]=None) -> None:
            """An instance type configuration for each instance type in an instance fleet, which determines the EC2 instances Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities.

            :param instance_type: An EC2 instance type.
            :param bid_price: The bid price for each EC2 Spot instance type as defined by InstanceType. Expressed in USD. Default: No bidPrice
            :param bid_price_as_percentage_of_on_demand_price: The bid price, as a percentage of On-Demand price. Default: No bidPriceAsPercentageOfOnDemandPrice
            :param configurations: A configuration classification that applies when provisioning cluster instances, which can include configurations for applications and software that run on the cluster. Default: No configurations
            :param ebs_configuration: The configuration of Amazon Elastic Block Storage (EBS) attached to each instance as defined by InstanceType. Default: No ebsConfiguration
            :param weighted_capacity: The number of units that a provisioned instance of this type provides toward fulfilling the target capacities defined in the InstanceFleetConfig. Default: No weightedCapacity

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceTypeConfig.html
            stability
            :stability: experimental
            """
            if isinstance(ebs_configuration, dict): ebs_configuration = EmrCreateCluster.EbsConfigurationProperty(**ebs_configuration)
            self._values = {
                'instance_type': instance_type,
            }
            if bid_price is not None: self._values["bid_price"] = bid_price
            if bid_price_as_percentage_of_on_demand_price is not None: self._values["bid_price_as_percentage_of_on_demand_price"] = bid_price_as_percentage_of_on_demand_price
            if configurations is not None: self._values["configurations"] = configurations
            if ebs_configuration is not None: self._values["ebs_configuration"] = ebs_configuration
            if weighted_capacity is not None: self._values["weighted_capacity"] = weighted_capacity

        @builtins.property
        def instance_type(self) -> str:
            """An EC2 instance type.

            stability
            :stability: experimental
            """
            return self._values.get('instance_type')

        @builtins.property
        def bid_price(self) -> typing.Optional[str]:
            """The bid price for each EC2 Spot instance type as defined by InstanceType.

            Expressed in USD.

            default
            :default: No bidPrice

            stability
            :stability: experimental
            """
            return self._values.get('bid_price')

        @builtins.property
        def bid_price_as_percentage_of_on_demand_price(self) -> typing.Optional[jsii.Number]:
            """The bid price, as a percentage of On-Demand price.

            default
            :default: No bidPriceAsPercentageOfOnDemandPrice

            stability
            :stability: experimental
            """
            return self._values.get('bid_price_as_percentage_of_on_demand_price')

        @builtins.property
        def configurations(self) -> typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]:
            """A configuration classification that applies when provisioning cluster instances, which can include configurations for applications and software that run on the cluster.

            default
            :default: No configurations

            stability
            :stability: experimental
            """
            return self._values.get('configurations')

        @builtins.property
        def ebs_configuration(self) -> typing.Optional["EmrCreateCluster.EbsConfigurationProperty"]:
            """The configuration of Amazon Elastic Block Storage (EBS) attached to each instance as defined by InstanceType.

            default
            :default: No ebsConfiguration

            stability
            :stability: experimental
            """
            return self._values.get('ebs_configuration')

        @builtins.property
        def weighted_capacity(self) -> typing.Optional[jsii.Number]:
            """The number of units that a provisioned instance of this type provides toward fulfilling the target capacities defined in the InstanceFleetConfig.

            default
            :default: No weightedCapacity

            stability
            :stability: experimental
            """
            return self._values.get('weighted_capacity')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstanceTypeConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstancesConfigProperty", jsii_struct_bases=[], name_mapping={'additional_master_security_groups': 'additionalMasterSecurityGroups', 'additional_slave_security_groups': 'additionalSlaveSecurityGroups', 'ec2_key_name': 'ec2KeyName', 'ec2_subnet_id': 'ec2SubnetId', 'ec2_subnet_ids': 'ec2SubnetIds', 'emr_managed_master_security_group': 'emrManagedMasterSecurityGroup', 'emr_managed_slave_security_group': 'emrManagedSlaveSecurityGroup', 'hadoop_version': 'hadoopVersion', 'instance_count': 'instanceCount', 'instance_fleets': 'instanceFleets', 'instance_groups': 'instanceGroups', 'master_instance_type': 'masterInstanceType', 'placement': 'placement', 'service_access_security_group': 'serviceAccessSecurityGroup', 'slave_instance_type': 'slaveInstanceType', 'termination_protected': 'terminationProtected'})
    class InstancesConfigProperty():
        def __init__(self, *, additional_master_security_groups: typing.Optional[typing.List[str]]=None, additional_slave_security_groups: typing.Optional[typing.List[str]]=None, ec2_key_name: typing.Optional[str]=None, ec2_subnet_id: typing.Optional[str]=None, ec2_subnet_ids: typing.Optional[typing.List[str]]=None, emr_managed_master_security_group: typing.Optional[str]=None, emr_managed_slave_security_group: typing.Optional[str]=None, hadoop_version: typing.Optional[str]=None, instance_count: typing.Optional[jsii.Number]=None, instance_fleets: typing.Optional[typing.List["EmrCreateCluster.InstanceFleetConfigProperty"]]=None, instance_groups: typing.Optional[typing.List["EmrCreateCluster.InstanceGroupConfigProperty"]]=None, master_instance_type: typing.Optional[str]=None, placement: typing.Optional["EmrCreateCluster.PlacementTypeProperty"]=None, service_access_security_group: typing.Optional[str]=None, slave_instance_type: typing.Optional[str]=None, termination_protected: typing.Optional[bool]=None) -> None:
            """A specification of the number and type of Amazon EC2 instances.

            See the RunJobFlow API for complete documentation on input parameters

            :param additional_master_security_groups: A list of additional Amazon EC2 security group IDs for the master node. Default: No additionalMasterSecurityGroups
            :param additional_slave_security_groups: A list of additional Amazon EC2 security group IDs for the core and task nodes. Default: No additionalSlaveSecurityGroups
            :param ec2_key_name: The name of the EC2 key pair that can be used to ssh to the master node as the user called "hadoop.". Default: No ec2KeyName
            :param ec2_subnet_id: Applies to clusters that use the uniform instance group configuration. To launch the cluster in Amazon Virtual Private Cloud (Amazon VPC), set this parameter to the identifier of the Amazon VPC subnet where you want the cluster to launch. Default: EMR selected default
            :param ec2_subnet_ids: Applies to clusters that use the instance fleet configuration. When multiple EC2 subnet IDs are specified, Amazon EMR evaluates them and launches instances in the optimal subnet. Default: EMR selected default
            :param emr_managed_master_security_group: The identifier of the Amazon EC2 security group for the master node. Default: No emrManagedMasterSecurityGroup
            :param emr_managed_slave_security_group: The identifier of the Amazon EC2 security group for the core and task nodes. Default: No emrManagedSlaveSecurityGroup
            :param hadoop_version: Applies only to Amazon EMR release versions earlier than 4.0. The Hadoop version for the cluster. Default: No hadoopVersion
            :param instance_count: The number of EC2 instances in the cluster. Default: No instanceCount
            :param instance_fleets: Describes the EC2 instances and instance configurations for clusters that use the instance fleet configuration. Default: No instanceFleets
            :param instance_groups: Configuration for the instance groups in a cluster. Default: No instanceGroups
            :param master_instance_type: The EC2 instance type of the master node. Default: No masterInstanceType
            :param placement: The Availability Zone in which the cluster runs. Default: EMR selected default
            :param service_access_security_group: The identifier of the Amazon EC2 security group for the Amazon EMR service to access clusters in VPC private subnets. Default: No serviceAccessSecurityGroup
            :param slave_instance_type: The EC2 instance type of the core and task nodes. Default: No slaveInstanceThpe
            :param termination_protected: Specifies whether to lock the cluster to prevent the Amazon EC2 instances from being terminated by API call, user intervention, or in the event of a job-flow error. Default: EMR selected default (false)

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_JobFlowInstancesConfig.html
            stability
            :stability: experimental
            """
            if isinstance(placement, dict): placement = EmrCreateCluster.PlacementTypeProperty(**placement)
            self._values = {
            }
            if additional_master_security_groups is not None: self._values["additional_master_security_groups"] = additional_master_security_groups
            if additional_slave_security_groups is not None: self._values["additional_slave_security_groups"] = additional_slave_security_groups
            if ec2_key_name is not None: self._values["ec2_key_name"] = ec2_key_name
            if ec2_subnet_id is not None: self._values["ec2_subnet_id"] = ec2_subnet_id
            if ec2_subnet_ids is not None: self._values["ec2_subnet_ids"] = ec2_subnet_ids
            if emr_managed_master_security_group is not None: self._values["emr_managed_master_security_group"] = emr_managed_master_security_group
            if emr_managed_slave_security_group is not None: self._values["emr_managed_slave_security_group"] = emr_managed_slave_security_group
            if hadoop_version is not None: self._values["hadoop_version"] = hadoop_version
            if instance_count is not None: self._values["instance_count"] = instance_count
            if instance_fleets is not None: self._values["instance_fleets"] = instance_fleets
            if instance_groups is not None: self._values["instance_groups"] = instance_groups
            if master_instance_type is not None: self._values["master_instance_type"] = master_instance_type
            if placement is not None: self._values["placement"] = placement
            if service_access_security_group is not None: self._values["service_access_security_group"] = service_access_security_group
            if slave_instance_type is not None: self._values["slave_instance_type"] = slave_instance_type
            if termination_protected is not None: self._values["termination_protected"] = termination_protected

        @builtins.property
        def additional_master_security_groups(self) -> typing.Optional[typing.List[str]]:
            """A list of additional Amazon EC2 security group IDs for the master node.

            default
            :default: No additionalMasterSecurityGroups

            stability
            :stability: experimental
            """
            return self._values.get('additional_master_security_groups')

        @builtins.property
        def additional_slave_security_groups(self) -> typing.Optional[typing.List[str]]:
            """A list of additional Amazon EC2 security group IDs for the core and task nodes.

            default
            :default: No additionalSlaveSecurityGroups

            stability
            :stability: experimental
            """
            return self._values.get('additional_slave_security_groups')

        @builtins.property
        def ec2_key_name(self) -> typing.Optional[str]:
            """The name of the EC2 key pair that can be used to ssh to the master node as the user called "hadoop.".

            default
            :default: No ec2KeyName

            stability
            :stability: experimental
            """
            return self._values.get('ec2_key_name')

        @builtins.property
        def ec2_subnet_id(self) -> typing.Optional[str]:
            """Applies to clusters that use the uniform instance group configuration.

            To launch the cluster in Amazon Virtual Private Cloud (Amazon VPC),
            set this parameter to the identifier of the Amazon VPC subnet where you want the cluster to launch.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('ec2_subnet_id')

        @builtins.property
        def ec2_subnet_ids(self) -> typing.Optional[typing.List[str]]:
            """Applies to clusters that use the instance fleet configuration.

            When multiple EC2 subnet IDs are specified, Amazon EMR evaluates them and
            launches instances in the optimal subnet.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('ec2_subnet_ids')

        @builtins.property
        def emr_managed_master_security_group(self) -> typing.Optional[str]:
            """The identifier of the Amazon EC2 security group for the master node.

            default
            :default: No emrManagedMasterSecurityGroup

            stability
            :stability: experimental
            """
            return self._values.get('emr_managed_master_security_group')

        @builtins.property
        def emr_managed_slave_security_group(self) -> typing.Optional[str]:
            """The identifier of the Amazon EC2 security group for the core and task nodes.

            default
            :default: No emrManagedSlaveSecurityGroup

            stability
            :stability: experimental
            """
            return self._values.get('emr_managed_slave_security_group')

        @builtins.property
        def hadoop_version(self) -> typing.Optional[str]:
            """Applies only to Amazon EMR release versions earlier than 4.0. The Hadoop version for the cluster.

            default
            :default: No hadoopVersion

            stability
            :stability: experimental
            """
            return self._values.get('hadoop_version')

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            """The number of EC2 instances in the cluster.

            default
            :default: No instanceCount

            stability
            :stability: experimental
            """
            return self._values.get('instance_count')

        @builtins.property
        def instance_fleets(self) -> typing.Optional[typing.List["EmrCreateCluster.InstanceFleetConfigProperty"]]:
            """Describes the EC2 instances and instance configurations for clusters that use the instance fleet configuration.

            default
            :default: No instanceFleets

            stability
            :stability: experimental
            """
            return self._values.get('instance_fleets')

        @builtins.property
        def instance_groups(self) -> typing.Optional[typing.List["EmrCreateCluster.InstanceGroupConfigProperty"]]:
            """Configuration for the instance groups in a cluster.

            default
            :default: No instanceGroups

            stability
            :stability: experimental
            """
            return self._values.get('instance_groups')

        @builtins.property
        def master_instance_type(self) -> typing.Optional[str]:
            """The EC2 instance type of the master node.

            default
            :default: No masterInstanceType

            stability
            :stability: experimental
            """
            return self._values.get('master_instance_type')

        @builtins.property
        def placement(self) -> typing.Optional["EmrCreateCluster.PlacementTypeProperty"]:
            """The Availability Zone in which the cluster runs.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('placement')

        @builtins.property
        def service_access_security_group(self) -> typing.Optional[str]:
            """The identifier of the Amazon EC2 security group for the Amazon EMR service to access clusters in VPC private subnets.

            default
            :default: No serviceAccessSecurityGroup

            stability
            :stability: experimental
            """
            return self._values.get('service_access_security_group')

        @builtins.property
        def slave_instance_type(self) -> typing.Optional[str]:
            """The EC2 instance type of the core and task nodes.

            default
            :default: No slaveInstanceThpe

            stability
            :stability: experimental
            """
            return self._values.get('slave_instance_type')

        @builtins.property
        def termination_protected(self) -> typing.Optional[bool]:
            """Specifies whether to lock the cluster to prevent the Amazon EC2 instances from being terminated by API call, user intervention, or in the event of a job-flow error.

            default
            :default: EMR selected default (false)

            stability
            :stability: experimental
            """
            return self._values.get('termination_protected')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstancesConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.KerberosAttributesProperty", jsii_struct_bases=[], name_mapping={'realm': 'realm', 'ad_domain_join_password': 'adDomainJoinPassword', 'ad_domain_join_user': 'adDomainJoinUser', 'cross_realm_trust_principal_password': 'crossRealmTrustPrincipalPassword', 'kdc_admin_password': 'kdcAdminPassword'})
    class KerberosAttributesProperty():
        def __init__(self, *, realm: str, ad_domain_join_password: typing.Optional[str]=None, ad_domain_join_user: typing.Optional[str]=None, cross_realm_trust_principal_password: typing.Optional[str]=None, kdc_admin_password: typing.Optional[str]=None) -> None:
            """Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration.

            See the RunJobFlow API for complete documentation on input parameters

            :param realm: The name of the Kerberos realm to which all nodes in a cluster belong. For example, EC2.INTERNAL.
            :param ad_domain_join_password: The Active Directory password for ADDomainJoinUser. Default: No adDomainJoinPassword
            :param ad_domain_join_user: Required only when establishing a cross-realm trust with an Active Directory domain. A user with sufficient privileges to join resources to the domain. Default: No adDomainJoinUser
            :param cross_realm_trust_principal_password: Required only when establishing a cross-realm trust with a KDC in a different realm. The cross-realm principal password, which must be identical across realms. Default: No crossRealmTrustPrincipalPassword
            :param kdc_admin_password: The password used within the cluster for the kadmin service on the cluster-dedicated KDC, which maintains Kerberos principals, password policies, and keytabs for the cluster. Default: No kdcAdminPassword

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_KerberosAttributes.html
            stability
            :stability: experimental
            """
            self._values = {
                'realm': realm,
            }
            if ad_domain_join_password is not None: self._values["ad_domain_join_password"] = ad_domain_join_password
            if ad_domain_join_user is not None: self._values["ad_domain_join_user"] = ad_domain_join_user
            if cross_realm_trust_principal_password is not None: self._values["cross_realm_trust_principal_password"] = cross_realm_trust_principal_password
            if kdc_admin_password is not None: self._values["kdc_admin_password"] = kdc_admin_password

        @builtins.property
        def realm(self) -> str:
            """The name of the Kerberos realm to which all nodes in a cluster belong.

            For example, EC2.INTERNAL.

            stability
            :stability: experimental
            """
            return self._values.get('realm')

        @builtins.property
        def ad_domain_join_password(self) -> typing.Optional[str]:
            """The Active Directory password for ADDomainJoinUser.

            default
            :default: No adDomainJoinPassword

            stability
            :stability: experimental
            """
            return self._values.get('ad_domain_join_password')

        @builtins.property
        def ad_domain_join_user(self) -> typing.Optional[str]:
            """Required only when establishing a cross-realm trust with an Active Directory domain.

            A user with sufficient privileges to join
            resources to the domain.

            default
            :default: No adDomainJoinUser

            stability
            :stability: experimental
            """
            return self._values.get('ad_domain_join_user')

        @builtins.property
        def cross_realm_trust_principal_password(self) -> typing.Optional[str]:
            """Required only when establishing a cross-realm trust with a KDC in a different realm.

            The cross-realm principal password, which
            must be identical across realms.

            default
            :default: No crossRealmTrustPrincipalPassword

            stability
            :stability: experimental
            """
            return self._values.get('cross_realm_trust_principal_password')

        @builtins.property
        def kdc_admin_password(self) -> typing.Optional[str]:
            """The password used within the cluster for the kadmin service on the cluster-dedicated KDC, which maintains Kerberos principals, password policies, and keytabs for the cluster.

            default
            :default: No kdcAdminPassword

            stability
            :stability: experimental
            """
            return self._values.get('kdc_admin_password')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'KerberosAttributesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.MetricDimensionProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class MetricDimensionProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """A CloudWatch dimension, which is specified using a Key (known as a Name in CloudWatch), Value pair.

            By default, Amazon EMR uses
            one dimension whose Key is JobFlowID and Value is a variable representing the cluster ID, which is ${emr.clusterId}. This enables
            the rule to bootstrap when the cluster ID becomes available

            :param key: The dimension name.
            :param value: The dimension value.

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_MetricDimension.html
            stability
            :stability: experimental
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """The dimension name.

            stability
            :stability: experimental
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """The dimension value.

            stability
            :stability: experimental
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricDimensionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.PlacementTypeProperty", jsii_struct_bases=[], name_mapping={'availability_zone': 'availabilityZone', 'availability_zones': 'availabilityZones'})
    class PlacementTypeProperty():
        def __init__(self, *, availability_zone: typing.Optional[str]=None, availability_zones: typing.Optional[typing.List[str]]=None) -> None:
            """The Amazon EC2 Availability Zone configuration of the cluster (job flow).

            :param availability_zone: The Amazon EC2 Availability Zone for the cluster. AvailabilityZone is used for uniform instance groups, while AvailabilityZones (plural) is used for instance fleets. Default: EMR selected default
            :param availability_zones: When multiple Availability Zones are specified, Amazon EMR evaluates them and launches instances in the optimal Availability Zone. AvailabilityZones is used for instance fleets, while AvailabilityZone (singular) is used for uniform instance groups. Default: EMR selected default

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_PlacementType.html
            stability
            :stability: experimental
            """
            self._values = {
            }
            if availability_zone is not None: self._values["availability_zone"] = availability_zone
            if availability_zones is not None: self._values["availability_zones"] = availability_zones

        @builtins.property
        def availability_zone(self) -> typing.Optional[str]:
            """The Amazon EC2 Availability Zone for the cluster.

            AvailabilityZone is used for uniform instance groups, while AvailabilityZones
            (plural) is used for instance fleets.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('availability_zone')

        @builtins.property
        def availability_zones(self) -> typing.Optional[typing.List[str]]:
            """When multiple Availability Zones are specified, Amazon EMR evaluates them and launches instances in the optimal Availability Zone.

            AvailabilityZones is used for instance fleets, while AvailabilityZone (singular) is used for uniform instance groups.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('availability_zones')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PlacementTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingActionProperty", jsii_struct_bases=[], name_mapping={'simple_scaling_policy_configuration': 'simpleScalingPolicyConfiguration', 'market': 'market'})
    class ScalingActionProperty():
        def __init__(self, *, simple_scaling_policy_configuration: "EmrCreateCluster.SimpleScalingPolicyConfigurationProperty", market: typing.Optional["EmrCreateCluster.InstanceMarket"]=None) -> None:
            """The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            And an automatic scaling configuration, which describes how the policy adds or removes instances, the cooldown period,
            and the number of EC2 instances that will be added each time the CloudWatch metric alarm condition is satisfied.

            :param simple_scaling_policy_configuration: The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.
            :param market: Not available for instance groups. Instance groups use the market type specified for the group. Default: EMR selected default

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScalingAction.html
            stability
            :stability: experimental
            """
            if isinstance(simple_scaling_policy_configuration, dict): simple_scaling_policy_configuration = EmrCreateCluster.SimpleScalingPolicyConfigurationProperty(**simple_scaling_policy_configuration)
            self._values = {
                'simple_scaling_policy_configuration': simple_scaling_policy_configuration,
            }
            if market is not None: self._values["market"] = market

        @builtins.property
        def simple_scaling_policy_configuration(self) -> "EmrCreateCluster.SimpleScalingPolicyConfigurationProperty":
            """The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            stability
            :stability: experimental
            """
            return self._values.get('simple_scaling_policy_configuration')

        @builtins.property
        def market(self) -> typing.Optional["EmrCreateCluster.InstanceMarket"]:
            """Not available for instance groups.

            Instance groups use the market type specified for the group.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('market')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScalingActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingAdjustmentType")
    class ScalingAdjustmentType(enum.Enum):
        """AutoScaling Adjustment Type.

        stability
        :stability: experimental
        """
        CHANGE_IN_CAPACITY = "CHANGE_IN_CAPACITY"
        """CHANGE_IN_CAPACITY.

        stability
        :stability: experimental
        """
        PERCENT_CHANGE_IN_CAPACITY = "PERCENT_CHANGE_IN_CAPACITY"
        """PERCENT_CHANGE_IN_CAPACITY.

        stability
        :stability: experimental
        """
        EXACT_CAPACITY = "EXACT_CAPACITY"
        """EXACT_CAPACITY.

        stability
        :stability: experimental
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingConstraintsProperty", jsii_struct_bases=[], name_mapping={'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity'})
    class ScalingConstraintsProperty():
        def __init__(self, *, max_capacity: jsii.Number, min_capacity: jsii.Number) -> None:
            """The upper and lower EC2 instance limits for an automatic scaling policy.

            Automatic scaling activities triggered by automatic scaling
            rules will not cause an instance group to grow above or below these limits.

            :param max_capacity: The upper boundary of EC2 instances in an instance group beyond which scaling activities are not allowed to grow. Scale-out activities will not add instances beyond this boundary.
            :param min_capacity: The lower boundary of EC2 instances in an instance group below which scaling activities are not allowed to shrink. Scale-in activities will not terminate instances below this boundary.

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScalingConstraints.html
            stability
            :stability: experimental
            """
            self._values = {
                'max_capacity': max_capacity,
                'min_capacity': min_capacity,
            }

        @builtins.property
        def max_capacity(self) -> jsii.Number:
            """The upper boundary of EC2 instances in an instance group beyond which scaling activities are not allowed to grow.

            Scale-out
            activities will not add instances beyond this boundary.

            stability
            :stability: experimental
            """
            return self._values.get('max_capacity')

        @builtins.property
        def min_capacity(self) -> jsii.Number:
            """The lower boundary of EC2 instances in an instance group below which scaling activities are not allowed to shrink.

            Scale-in
            activities will not terminate instances below this boundary.

            stability
            :stability: experimental
            """
            return self._values.get('min_capacity')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScalingConstraintsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingRuleProperty", jsii_struct_bases=[], name_mapping={'action': 'action', 'name': 'name', 'trigger': 'trigger', 'description': 'description'})
    class ScalingRuleProperty():
        def __init__(self, *, action: "EmrCreateCluster.ScalingActionProperty", name: str, trigger: "EmrCreateCluster.ScalingTriggerProperty", description: typing.Optional[str]=None) -> None:
            """A scale-in or scale-out rule that defines scaling activity, including the CloudWatch metric alarm that triggers activity, how EC2 instances are added or removed, and the periodicity of adjustments.

            :param action: The conditions that trigger an automatic scaling activity.
            :param name: The name used to identify an automatic scaling rule. Rule names must be unique within a scaling policy.
            :param trigger: The CloudWatch alarm definition that determines when automatic scaling activity is triggered.
            :param description: A friendly, more verbose description of the automatic scaling rule. Default: No description

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScalingRule.html
            stability
            :stability: experimental
            """
            if isinstance(action, dict): action = EmrCreateCluster.ScalingActionProperty(**action)
            if isinstance(trigger, dict): trigger = EmrCreateCluster.ScalingTriggerProperty(**trigger)
            self._values = {
                'action': action,
                'name': name,
                'trigger': trigger,
            }
            if description is not None: self._values["description"] = description

        @builtins.property
        def action(self) -> "EmrCreateCluster.ScalingActionProperty":
            """The conditions that trigger an automatic scaling activity.

            stability
            :stability: experimental
            """
            return self._values.get('action')

        @builtins.property
        def name(self) -> str:
            """The name used to identify an automatic scaling rule.

            Rule names must be unique within a scaling policy.

            stability
            :stability: experimental
            """
            return self._values.get('name')

        @builtins.property
        def trigger(self) -> "EmrCreateCluster.ScalingTriggerProperty":
            """The CloudWatch alarm definition that determines when automatic scaling activity is triggered.

            stability
            :stability: experimental
            """
            return self._values.get('trigger')

        @builtins.property
        def description(self) -> typing.Optional[str]:
            """A friendly, more verbose description of the automatic scaling rule.

            default
            :default: No description

            stability
            :stability: experimental
            """
            return self._values.get('description')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScalingRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingTriggerProperty", jsii_struct_bases=[], name_mapping={'cloud_watch_alarm_definition': 'cloudWatchAlarmDefinition'})
    class ScalingTriggerProperty():
        def __init__(self, *, cloud_watch_alarm_definition: "EmrCreateCluster.CloudWatchAlarmDefinitionProperty") -> None:
            """The conditions that trigger an automatic scaling activity and the definition of a CloudWatch metric alarm.

            When the defined alarm conditions are met along with other trigger parameters, scaling activity begins.

            :param cloud_watch_alarm_definition: The definition of a CloudWatch metric alarm. When the defined alarm conditions are met along with other trigger parameters, scaling activity begins.

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScalingTrigger.html
            stability
            :stability: experimental
            """
            if isinstance(cloud_watch_alarm_definition, dict): cloud_watch_alarm_definition = EmrCreateCluster.CloudWatchAlarmDefinitionProperty(**cloud_watch_alarm_definition)
            self._values = {
                'cloud_watch_alarm_definition': cloud_watch_alarm_definition,
            }

        @builtins.property
        def cloud_watch_alarm_definition(self) -> "EmrCreateCluster.CloudWatchAlarmDefinitionProperty":
            """The definition of a CloudWatch metric alarm.

            When the defined alarm conditions are met along with other trigger parameters,
            scaling activity begins.

            stability
            :stability: experimental
            """
            return self._values.get('cloud_watch_alarm_definition')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScalingTriggerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScriptBootstrapActionConfigProperty", jsii_struct_bases=[], name_mapping={'path': 'path', 'args': 'args'})
    class ScriptBootstrapActionConfigProperty():
        def __init__(self, *, path: str, args: typing.Optional[typing.List[str]]=None) -> None:
            """Configuration of the script to run during a bootstrap action.

            :param path: Location of the script to run during a bootstrap action. Can be either a location in Amazon S3 or on a local file system.
            :param args: A list of command line arguments to pass to the bootstrap action script. Default: No args

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScriptBootstrapActionConfig.html
            stability
            :stability: experimental
            """
            self._values = {
                'path': path,
            }
            if args is not None: self._values["args"] = args

        @builtins.property
        def path(self) -> str:
            """Location of the script to run during a bootstrap action.

            Can be either a location in Amazon S3 or on a local file system.

            stability
            :stability: experimental
            """
            return self._values.get('path')

        @builtins.property
        def args(self) -> typing.Optional[typing.List[str]]:
            """A list of command line arguments to pass to the bootstrap action script.

            default
            :default: No args

            stability
            :stability: experimental
            """
            return self._values.get('args')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScriptBootstrapActionConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.SimpleScalingPolicyConfigurationProperty", jsii_struct_bases=[], name_mapping={'scaling_adjustment': 'scalingAdjustment', 'adjustment_type': 'adjustmentType', 'cool_down': 'coolDown'})
    class SimpleScalingPolicyConfigurationProperty():
        def __init__(self, *, scaling_adjustment: jsii.Number, adjustment_type: typing.Optional["EmrCreateCluster.ScalingAdjustmentType"]=None, cool_down: typing.Optional[jsii.Number]=None) -> None:
            """An automatic scaling configuration, which describes how the policy adds or removes instances, the cooldown period, and the number of EC2 instances that will be added each time the CloudWatch metric alarm condition is satisfied.

            :param scaling_adjustment: The amount by which to scale in or scale out, based on the specified AdjustmentType. A positive value adds to the instance group's EC2 instance count while a negative number removes instances. If AdjustmentType is set to EXACT_CAPACITY, the number should only be a positive integer.
            :param adjustment_type: The way in which EC2 instances are added (if ScalingAdjustment is a positive number) or terminated (if ScalingAdjustment is a negative number) each time the scaling activity is triggered. Default: No adjustmentType
            :param cool_down: The amount of time, in seconds, after a scaling activity completes before any further trigger-related scaling activities can start. The default value is 0. Default: No coolDown

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_SimpleScalingPolicyConfiguration.html
            stability
            :stability: experimental
            """
            self._values = {
                'scaling_adjustment': scaling_adjustment,
            }
            if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
            if cool_down is not None: self._values["cool_down"] = cool_down

        @builtins.property
        def scaling_adjustment(self) -> jsii.Number:
            """The amount by which to scale in or scale out, based on the specified AdjustmentType.

            A positive value adds to the instance group's
            EC2 instance count while a negative number removes instances. If AdjustmentType is set to EXACT_CAPACITY, the number should only be
            a positive integer.

            stability
            :stability: experimental
            """
            return self._values.get('scaling_adjustment')

        @builtins.property
        def adjustment_type(self) -> typing.Optional["EmrCreateCluster.ScalingAdjustmentType"]:
            """The way in which EC2 instances are added (if ScalingAdjustment is a positive number) or terminated (if ScalingAdjustment is a negative number) each time the scaling activity is triggered.

            default
            :default: No adjustmentType

            stability
            :stability: experimental
            """
            return self._values.get('adjustment_type')

        @builtins.property
        def cool_down(self) -> typing.Optional[jsii.Number]:
            """The amount of time, in seconds, after a scaling activity completes before any further trigger-related scaling activities can start.

            The default value is 0.

            default
            :default: No coolDown

            stability
            :stability: experimental
            """
            return self._values.get('cool_down')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SimpleScalingPolicyConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.SpotProvisioningSpecificationProperty", jsii_struct_bases=[], name_mapping={'timeout_action': 'timeoutAction', 'timeout_duration_minutes': 'timeoutDurationMinutes', 'block_duration_minutes': 'blockDurationMinutes'})
    class SpotProvisioningSpecificationProperty():
        def __init__(self, *, timeout_action: "EmrCreateCluster.SpotTimeoutAction", timeout_duration_minutes: jsii.Number, block_duration_minutes: typing.Optional[jsii.Number]=None) -> None:
            """The launch specification for Spot instances in the instance fleet, which determines the defined duration and provisioning timeout behavior.

            :param timeout_action: The action to take when TargetSpotCapacity has not been fulfilled when the TimeoutDurationMinutes has expired.
            :param timeout_duration_minutes: The spot provisioning timeout period in minutes.
            :param block_duration_minutes: The defined duration for Spot instances (also known as Spot blocks) in minutes. Default: No blockDurationMinutes

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_SpotProvisioningSpecification.html
            stability
            :stability: experimental
            """
            self._values = {
                'timeout_action': timeout_action,
                'timeout_duration_minutes': timeout_duration_minutes,
            }
            if block_duration_minutes is not None: self._values["block_duration_minutes"] = block_duration_minutes

        @builtins.property
        def timeout_action(self) -> "EmrCreateCluster.SpotTimeoutAction":
            """The action to take when TargetSpotCapacity has not been fulfilled when the TimeoutDurationMinutes has expired.

            stability
            :stability: experimental
            """
            return self._values.get('timeout_action')

        @builtins.property
        def timeout_duration_minutes(self) -> jsii.Number:
            """The spot provisioning timeout period in minutes.

            stability
            :stability: experimental
            """
            return self._values.get('timeout_duration_minutes')

        @builtins.property
        def block_duration_minutes(self) -> typing.Optional[jsii.Number]:
            """The defined duration for Spot instances (also known as Spot blocks) in minutes.

            default
            :default: No blockDurationMinutes

            stability
            :stability: experimental
            """
            return self._values.get('block_duration_minutes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SpotProvisioningSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.SpotTimeoutAction")
    class SpotTimeoutAction(enum.Enum):
        """Spot Timeout Actions.

        stability
        :stability: experimental
        """
        SWITCH_TO_ON_DEMAND = "SWITCH_TO_ON_DEMAND"
        """\ SWITCH_TO_ON_DEMAND.

        stability
        :stability: experimental
        """
        TERMINATE_CLUSTER = "TERMINATE_CLUSTER"
        """TERMINATE_CLUSTER.

        stability
        :stability: experimental
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.VolumeSpecificationProperty", jsii_struct_bases=[], name_mapping={'size_in_gb': 'sizeInGB', 'volume_type': 'volumeType', 'iops': 'iops'})
    class VolumeSpecificationProperty():
        def __init__(self, *, size_in_gb: jsii.Number, volume_type: "EmrCreateCluster.EbsBlockDeviceVolumeType", iops: typing.Optional[jsii.Number]=None) -> None:
            """EBS volume specifications such as volume type, IOPS, and size (GiB) that will be requested for the EBS volume attached to an EC2 instance in the cluster.

            :param size_in_gb: The volume size, in gibibytes (GiB). This can be a number from 1 - 1024. If the volume type is EBS-optimized, the minimum value is 10.
            :param volume_type: The volume type. Volume types supported are gp2, io1, standard.
            :param iops: The number of I/O operations per second (IOPS) that the volume supports. Default: EMR selected default

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_VolumeSpecification.html
            stability
            :stability: experimental
            """
            self._values = {
                'size_in_gb': size_in_gb,
                'volume_type': volume_type,
            }
            if iops is not None: self._values["iops"] = iops

        @builtins.property
        def size_in_gb(self) -> jsii.Number:
            """The volume size, in gibibytes (GiB).

            This can be a number from 1 - 1024. If the volume type is EBS-optimized, the minimum value is 10.

            stability
            :stability: experimental
            """
            return self._values.get('size_in_gb')

        @builtins.property
        def volume_type(self) -> "EmrCreateCluster.EbsBlockDeviceVolumeType":
            """The volume type.

            Volume types supported are gp2, io1, standard.

            stability
            :stability: experimental
            """
            return self._values.get('volume_type')

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            """The number of I/O operations per second (IOPS) that the volume supports.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('iops')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VolumeSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateClusterProps", jsii_struct_bases=[], name_mapping={'instances': 'instances', 'name': 'name', 'additional_info': 'additionalInfo', 'applications': 'applications', 'auto_scaling_role': 'autoScalingRole', 'bootstrap_actions': 'bootstrapActions', 'cluster_role': 'clusterRole', 'configurations': 'configurations', 'custom_ami_id': 'customAmiId', 'ebs_root_volume_size': 'ebsRootVolumeSize', 'integration_pattern': 'integrationPattern', 'kerberos_attributes': 'kerberosAttributes', 'log_uri': 'logUri', 'release_label': 'releaseLabel', 'scale_down_behavior': 'scaleDownBehavior', 'security_configuration': 'securityConfiguration', 'service_role': 'serviceRole', 'tags': 'tags', 'visible_to_all_users': 'visibleToAllUsers'})
class EmrCreateClusterProps():
    def __init__(self, *, instances: "EmrCreateCluster.InstancesConfigProperty", name: str, additional_info: typing.Optional[str]=None, applications: typing.Optional[typing.List["EmrCreateCluster.ApplicationConfigProperty"]]=None, auto_scaling_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, bootstrap_actions: typing.Optional[typing.List["EmrCreateCluster.BootstrapActionConfigProperty"]]=None, cluster_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]=None, custom_ami_id: typing.Optional[str]=None, ebs_root_volume_size: typing.Optional[jsii.Number]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, kerberos_attributes: typing.Optional["EmrCreateCluster.KerberosAttributesProperty"]=None, log_uri: typing.Optional[str]=None, release_label: typing.Optional[str]=None, scale_down_behavior: typing.Optional["EmrCreateCluster.EmrClusterScaleDownBehavior"]=None, security_configuration: typing.Optional[str]=None, service_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, visible_to_all_users: typing.Optional[bool]=None) -> None:
        """Properties for EmrCreateCluster.

        See the RunJobFlow API for complete documentation on input parameters

        :param instances: A specification of the number and type of Amazon EC2 instances.
        :param name: The Name of the Cluster.
        :param additional_info: A JSON string for selecting additional features. Default: No additionalInfo
        :param applications: A case-insensitive list of applications for Amazon EMR to install and configure when launching the cluster. Default: EMR selected default
        :param auto_scaling_role: An IAM role for automatic scaling policies. A Role will be created if one is not provided. Default: No autoScalingRole
        :param bootstrap_actions: A list of bootstrap actions to run before Hadoop starts on the cluster nodes. Default: No bootstrapActions
        :param cluster_role: Also called instance profile and EC2 role. An IAM role for an EMR cluster. The EC2 instances of the cluster assume this role. This attribute has been renamed from jobFlowRole to clusterRole to align with other ERM/StepFunction integration parameters. A Role will be created if one is not provided. Default: No clusterRole
        :param configurations: The list of configurations supplied for the EMR cluster you are creating. Default: No configurations
        :param custom_ami_id: The ID of a custom Amazon EBS-backed Linux AMI. Default: No customAmiId
        :param ebs_root_volume_size: The size, in GiB, of the EBS root device volume of the Linux AMI that is used for each EC2 instance. Default: EMR selected default
        :param integration_pattern: The service integration pattern indicates different ways to call CreateCluster. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC
        :param kerberos_attributes: Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration. Default: No kerberosAttributes
        :param log_uri: The location in Amazon S3 to write the log files of the job flow. Default: No logUri
        :param release_label: The Amazon EMR release label, which determines the version of open-source application packages installed on the cluster. Default: EMR selected default
        :param scale_down_behavior: Specifies the way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized. Default: EMR selected default
        :param security_configuration: The name of a security configuration to apply to the cluster. Default: No securityConfiguration
        :param service_role: The IAM role that will be assumed by the Amazon EMR service to access AWS resources on your behalf. A Role will be created if one is not provided. Default: No serviceRole
        :param tags: A list of tags to associate with a cluster and propagate to Amazon EC2 instances. Default: No Tags
        :param visible_to_all_users: A value of true indicates that all IAM users in the AWS account can perform cluster actions if they have the proper IAM policy permissions. Default: true

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_RunJobFlow.html
        stability
        :stability: experimental
        """
        if isinstance(instances, dict): instances = EmrCreateCluster.InstancesConfigProperty(**instances)
        if isinstance(kerberos_attributes, dict): kerberos_attributes = EmrCreateCluster.KerberosAttributesProperty(**kerberos_attributes)
        self._values = {
            'instances': instances,
            'name': name,
        }
        if additional_info is not None: self._values["additional_info"] = additional_info
        if applications is not None: self._values["applications"] = applications
        if auto_scaling_role is not None: self._values["auto_scaling_role"] = auto_scaling_role
        if bootstrap_actions is not None: self._values["bootstrap_actions"] = bootstrap_actions
        if cluster_role is not None: self._values["cluster_role"] = cluster_role
        if configurations is not None: self._values["configurations"] = configurations
        if custom_ami_id is not None: self._values["custom_ami_id"] = custom_ami_id
        if ebs_root_volume_size is not None: self._values["ebs_root_volume_size"] = ebs_root_volume_size
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if kerberos_attributes is not None: self._values["kerberos_attributes"] = kerberos_attributes
        if log_uri is not None: self._values["log_uri"] = log_uri
        if release_label is not None: self._values["release_label"] = release_label
        if scale_down_behavior is not None: self._values["scale_down_behavior"] = scale_down_behavior
        if security_configuration is not None: self._values["security_configuration"] = security_configuration
        if service_role is not None: self._values["service_role"] = service_role
        if tags is not None: self._values["tags"] = tags
        if visible_to_all_users is not None: self._values["visible_to_all_users"] = visible_to_all_users

    @builtins.property
    def instances(self) -> "EmrCreateCluster.InstancesConfigProperty":
        """A specification of the number and type of Amazon EC2 instances.

        stability
        :stability: experimental
        """
        return self._values.get('instances')

    @builtins.property
    def name(self) -> str:
        """The Name of the Cluster.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def additional_info(self) -> typing.Optional[str]:
        """A JSON string for selecting additional features.

        default
        :default: No additionalInfo

        stability
        :stability: experimental
        """
        return self._values.get('additional_info')

    @builtins.property
    def applications(self) -> typing.Optional[typing.List["EmrCreateCluster.ApplicationConfigProperty"]]:
        """A case-insensitive list of applications for Amazon EMR to install and configure when launching the cluster.

        default
        :default: EMR selected default

        stability
        :stability: experimental
        """
        return self._values.get('applications')

    @builtins.property
    def auto_scaling_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role for automatic scaling policies.

        A Role will be created if one is not provided.

        default
        :default: No autoScalingRole

        stability
        :stability: experimental
        """
        return self._values.get('auto_scaling_role')

    @builtins.property
    def bootstrap_actions(self) -> typing.Optional[typing.List["EmrCreateCluster.BootstrapActionConfigProperty"]]:
        """A list of bootstrap actions to run before Hadoop starts on the cluster nodes.

        default
        :default: No bootstrapActions

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_actions')

    @builtins.property
    def cluster_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Also called instance profile and EC2 role.

        An IAM role for an EMR cluster. The EC2 instances of the cluster assume this role.

        This attribute has been renamed from jobFlowRole to clusterRole to align with other ERM/StepFunction integration parameters.
        A Role will be created if one is not provided.

        default
        :default: No clusterRole

        stability
        :stability: experimental
        """
        return self._values.get('cluster_role')

    @builtins.property
    def configurations(self) -> typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]:
        """The list of configurations supplied for the EMR cluster you are creating.

        default
        :default: No configurations

        stability
        :stability: experimental
        """
        return self._values.get('configurations')

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[str]:
        """The ID of a custom Amazon EBS-backed Linux AMI.

        default
        :default: No customAmiId

        stability
        :stability: experimental
        """
        return self._values.get('custom_ami_id')

    @builtins.property
    def ebs_root_volume_size(self) -> typing.Optional[jsii.Number]:
        """The size, in GiB, of the EBS root device volume of the Linux AMI that is used for each EC2 instance.

        default
        :default: EMR selected default

        stability
        :stability: experimental
        """
        return self._values.get('ebs_root_volume_size')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call CreateCluster.

        The valid value is either FIRE_AND_FORGET or SYNC.

        default
        :default: SYNC

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def kerberos_attributes(self) -> typing.Optional["EmrCreateCluster.KerberosAttributesProperty"]:
        """Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration.

        default
        :default: No kerberosAttributes

        stability
        :stability: experimental
        """
        return self._values.get('kerberos_attributes')

    @builtins.property
    def log_uri(self) -> typing.Optional[str]:
        """The location in Amazon S3 to write the log files of the job flow.

        default
        :default: No logUri

        stability
        :stability: experimental
        """
        return self._values.get('log_uri')

    @builtins.property
    def release_label(self) -> typing.Optional[str]:
        """The Amazon EMR release label, which determines the version of open-source application packages installed on the cluster.

        default
        :default: EMR selected default

        stability
        :stability: experimental
        """
        return self._values.get('release_label')

    @builtins.property
    def scale_down_behavior(self) -> typing.Optional["EmrCreateCluster.EmrClusterScaleDownBehavior"]:
        """Specifies the way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized.

        default
        :default: EMR selected default

        stability
        :stability: experimental
        """
        return self._values.get('scale_down_behavior')

    @builtins.property
    def security_configuration(self) -> typing.Optional[str]:
        """The name of a security configuration to apply to the cluster.

        default
        :default: No securityConfiguration

        stability
        :stability: experimental
        """
        return self._values.get('security_configuration')

    @builtins.property
    def service_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role that will be assumed by the Amazon EMR service to access AWS resources on your behalf.

        A Role will be created if
        one is not provided.

        default
        :default: No serviceRole

        stability
        :stability: experimental
        """
        return self._values.get('service_role')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """A list of tags to associate with a cluster and propagate to Amazon EC2 instances.

        default
        :default: No Tags

        stability
        :stability: experimental
        """
        return self._values.get('tags')

    @builtins.property
    def visible_to_all_users(self) -> typing.Optional[bool]:
        """A value of true indicates that all IAM users in the AWS account can perform cluster actions if they have the proper IAM policy permissions.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('visible_to_all_users')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmrCreateClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EmrModifyInstanceFleetByName(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceFleetByName"):
    """A Step Functions Task to to modify an InstanceFleet on an EMR Cluster.

    stability
    :stability: experimental
    """
    def __init__(self, *, cluster_id: str, instance_fleet_name: str, target_on_demand_capacity: jsii.Number, target_spot_capacity: jsii.Number) -> None:
        """
        :param cluster_id: The ClusterId to update.
        :param instance_fleet_name: The InstanceFleetName to update.
        :param target_on_demand_capacity: The target capacity of On-Demand units for the instance fleet. Default: None
        :param target_spot_capacity: The target capacity of Spot units for the instance fleet. Default: None

        stability
        :stability: experimental
        """
        props = EmrModifyInstanceFleetByNameProps(cluster_id=cluster_id, instance_fleet_name=instance_fleet_name, target_on_demand_capacity=target_on_demand_capacity, target_spot_capacity=target_spot_capacity)

        jsii.create(EmrModifyInstanceFleetByName, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceFleetByNameProps", jsii_struct_bases=[], name_mapping={'cluster_id': 'clusterId', 'instance_fleet_name': 'instanceFleetName', 'target_on_demand_capacity': 'targetOnDemandCapacity', 'target_spot_capacity': 'targetSpotCapacity'})
class EmrModifyInstanceFleetByNameProps():
    def __init__(self, *, cluster_id: str, instance_fleet_name: str, target_on_demand_capacity: jsii.Number, target_spot_capacity: jsii.Number) -> None:
        """Properties for EmrModifyInstanceFleetByName.

        :param cluster_id: The ClusterId to update.
        :param instance_fleet_name: The InstanceFleetName to update.
        :param target_on_demand_capacity: The target capacity of On-Demand units for the instance fleet. Default: None
        :param target_spot_capacity: The target capacity of Spot units for the instance fleet. Default: None

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_id': cluster_id,
            'instance_fleet_name': instance_fleet_name,
            'target_on_demand_capacity': target_on_demand_capacity,
            'target_spot_capacity': target_spot_capacity,
        }

    @builtins.property
    def cluster_id(self) -> str:
        """The ClusterId to update.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_id')

    @builtins.property
    def instance_fleet_name(self) -> str:
        """The InstanceFleetName to update.

        stability
        :stability: experimental
        """
        return self._values.get('instance_fleet_name')

    @builtins.property
    def target_on_demand_capacity(self) -> jsii.Number:
        """The target capacity of On-Demand units for the instance fleet.

        default
        :default: None

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceFleetModifyConfig.html
        stability
        :stability: experimental
        """
        return self._values.get('target_on_demand_capacity')

    @builtins.property
    def target_spot_capacity(self) -> jsii.Number:
        """The target capacity of Spot units for the instance fleet.

        default
        :default: None

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceFleetModifyConfig.html
        stability
        :stability: experimental
        """
        return self._values.get('target_spot_capacity')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmrModifyInstanceFleetByNameProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EmrModifyInstanceGroupByName(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByName"):
    """A Step Functions Task to to modify an InstanceGroup on an EMR Cluster.

    stability
    :stability: experimental
    """
    def __init__(self, *, cluster_id: str, instance_group: "InstanceGroupModifyConfigProperty", instance_group_name: str) -> None:
        """
        :param cluster_id: The ClusterId to update.
        :param instance_group: The JSON that you want to provide to your ModifyInstanceGroup call as input. This uses the same syntax as the ModifyInstanceGroups API.
        :param instance_group_name: The InstanceGroupName to update.

        stability
        :stability: experimental
        """
        props = EmrModifyInstanceGroupByNameProps(cluster_id=cluster_id, instance_group=instance_group, instance_group_name=instance_group_name)

        jsii.create(EmrModifyInstanceGroupByName, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty", jsii_struct_bases=[], name_mapping={'configurations': 'configurations', 'e_c2_instance_ids_to_terminate': 'eC2InstanceIdsToTerminate', 'instance_count': 'instanceCount', 'shrink_policy': 'shrinkPolicy'})
    class InstanceGroupModifyConfigProperty():
        def __init__(self, *, configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]=None, e_c2_instance_ids_to_terminate: typing.Optional[typing.List[str]]=None, instance_count: typing.Optional[jsii.Number]=None, shrink_policy: typing.Optional["EmrModifyInstanceGroupByName.ShrinkPolicyProperty"]=None) -> None:
            """Modify the size or configurations of an instance group.

            :param configurations: A list of new or modified configurations to apply for an instance group. Default: No configurations
            :param e_c2_instance_ids_to_terminate: The EC2 InstanceIds to terminate. After you terminate the instances, the instance group will not return to its original requested size. Default: No eC2InstanceIdsToTerminate
            :param instance_count: Target size for the instance group. Default: No instanceCount
            :param shrink_policy: Policy for customizing shrink operations. Default: No shrinkPolicy

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceGroupModifyConfig.html
            stability
            :stability: experimental
            """
            if isinstance(shrink_policy, dict): shrink_policy = EmrModifyInstanceGroupByName.ShrinkPolicyProperty(**shrink_policy)
            self._values = {
            }
            if configurations is not None: self._values["configurations"] = configurations
            if e_c2_instance_ids_to_terminate is not None: self._values["e_c2_instance_ids_to_terminate"] = e_c2_instance_ids_to_terminate
            if instance_count is not None: self._values["instance_count"] = instance_count
            if shrink_policy is not None: self._values["shrink_policy"] = shrink_policy

        @builtins.property
        def configurations(self) -> typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]:
            """A list of new or modified configurations to apply for an instance group.

            default
            :default: No configurations

            stability
            :stability: experimental
            """
            return self._values.get('configurations')

        @builtins.property
        def e_c2_instance_ids_to_terminate(self) -> typing.Optional[typing.List[str]]:
            """The EC2 InstanceIds to terminate.

            After you terminate the instances, the instance group will not return to its original requested size.

            default
            :default: No eC2InstanceIdsToTerminate

            stability
            :stability: experimental
            """
            return self._values.get('e_c2_instance_ids_to_terminate')

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            """Target size for the instance group.

            default
            :default: No instanceCount

            stability
            :stability: experimental
            """
            return self._values.get('instance_count')

        @builtins.property
        def shrink_policy(self) -> typing.Optional["EmrModifyInstanceGroupByName.ShrinkPolicyProperty"]:
            """Policy for customizing shrink operations.

            default
            :default: No shrinkPolicy

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ShrinkPolicy.html
            stability
            :stability: experimental
            """
            return self._values.get('shrink_policy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstanceGroupModifyConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByName.InstanceResizePolicyProperty", jsii_struct_bases=[], name_mapping={'instances_to_protect': 'instancesToProtect', 'instances_to_terminate': 'instancesToTerminate', 'instance_termination_timeout': 'instanceTerminationTimeout'})
    class InstanceResizePolicyProperty():
        def __init__(self, *, instances_to_protect: typing.Optional[typing.List[str]]=None, instances_to_terminate: typing.Optional[typing.List[str]]=None, instance_termination_timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
            """Custom policy for requesting termination protection or termination of specific instances when shrinking an instance group.

            :param instances_to_protect: Specific list of instances to be protected when shrinking an instance group. Default: No instancesToProtect
            :param instances_to_terminate: Specific list of instances to be terminated when shrinking an instance group. Default: No instancesToTerminate
            :param instance_termination_timeout: Decommissioning timeout override for the specific list of instances to be terminated. Default: EMR selected default

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceResizePolicy.html
            stability
            :stability: experimental
            """
            self._values = {
            }
            if instances_to_protect is not None: self._values["instances_to_protect"] = instances_to_protect
            if instances_to_terminate is not None: self._values["instances_to_terminate"] = instances_to_terminate
            if instance_termination_timeout is not None: self._values["instance_termination_timeout"] = instance_termination_timeout

        @builtins.property
        def instances_to_protect(self) -> typing.Optional[typing.List[str]]:
            """Specific list of instances to be protected when shrinking an instance group.

            default
            :default: No instancesToProtect

            stability
            :stability: experimental
            """
            return self._values.get('instances_to_protect')

        @builtins.property
        def instances_to_terminate(self) -> typing.Optional[typing.List[str]]:
            """Specific list of instances to be terminated when shrinking an instance group.

            default
            :default: No instancesToTerminate

            stability
            :stability: experimental
            """
            return self._values.get('instances_to_terminate')

        @builtins.property
        def instance_termination_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
            """Decommissioning timeout override for the specific list of instances to be terminated.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('instance_termination_timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstanceResizePolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByName.ShrinkPolicyProperty", jsii_struct_bases=[], name_mapping={'decommission_timeout': 'decommissionTimeout', 'instance_resize_policy': 'instanceResizePolicy'})
    class ShrinkPolicyProperty():
        def __init__(self, *, decommission_timeout: typing.Optional[aws_cdk.core.Duration]=None, instance_resize_policy: typing.Optional["EmrModifyInstanceGroupByName.InstanceResizePolicyProperty"]=None) -> None:
            """Policy for customizing shrink operations.

            Allows configuration of decommissioning timeout and targeted instance shrinking.

            :param decommission_timeout: The desired timeout for decommissioning an instance. Overrides the default YARN decommissioning timeout. Default: EMR selected default
            :param instance_resize_policy: Custom policy for requesting termination protection or termination of specific instances when shrinking an instance group. Default: No instanceResizePolicy

            see
            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ShrinkPolicy.html
            stability
            :stability: experimental
            """
            if isinstance(instance_resize_policy, dict): instance_resize_policy = EmrModifyInstanceGroupByName.InstanceResizePolicyProperty(**instance_resize_policy)
            self._values = {
            }
            if decommission_timeout is not None: self._values["decommission_timeout"] = decommission_timeout
            if instance_resize_policy is not None: self._values["instance_resize_policy"] = instance_resize_policy

        @builtins.property
        def decommission_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
            """The desired timeout for decommissioning an instance.

            Overrides the default YARN decommissioning timeout.

            default
            :default: EMR selected default

            stability
            :stability: experimental
            """
            return self._values.get('decommission_timeout')

        @builtins.property
        def instance_resize_policy(self) -> typing.Optional["EmrModifyInstanceGroupByName.InstanceResizePolicyProperty"]:
            """Custom policy for requesting termination protection or termination of specific instances when shrinking an instance group.

            default
            :default: No instanceResizePolicy

            stability
            :stability: experimental
            """
            return self._values.get('instance_resize_policy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ShrinkPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByNameProps", jsii_struct_bases=[], name_mapping={'cluster_id': 'clusterId', 'instance_group': 'instanceGroup', 'instance_group_name': 'instanceGroupName'})
class EmrModifyInstanceGroupByNameProps():
    def __init__(self, *, cluster_id: str, instance_group: "EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty", instance_group_name: str) -> None:
        """Properties for EmrModifyInstanceGroupByName.

        :param cluster_id: The ClusterId to update.
        :param instance_group: The JSON that you want to provide to your ModifyInstanceGroup call as input. This uses the same syntax as the ModifyInstanceGroups API.
        :param instance_group_name: The InstanceGroupName to update.

        stability
        :stability: experimental
        """
        if isinstance(instance_group, dict): instance_group = EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty(**instance_group)
        self._values = {
            'cluster_id': cluster_id,
            'instance_group': instance_group,
            'instance_group_name': instance_group_name,
        }

    @builtins.property
    def cluster_id(self) -> str:
        """The ClusterId to update.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_id')

    @builtins.property
    def instance_group(self) -> "EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty":
        """The JSON that you want to provide to your ModifyInstanceGroup call as input.

        This uses the same syntax as the ModifyInstanceGroups API.

        see
        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ModifyInstanceGroups.html
        stability
        :stability: experimental
        """
        return self._values.get('instance_group')

    @builtins.property
    def instance_group_name(self) -> str:
        """The InstanceGroupName to update.

        stability
        :stability: experimental
        """
        return self._values.get('instance_group_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmrModifyInstanceGroupByNameProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EmrSetClusterTerminationProtection(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrSetClusterTerminationProtection"):
    """A Step Functions Task to to set Termination Protection on an EMR Cluster.

    stability
    :stability: experimental
    """
    def __init__(self, *, cluster_id: str, termination_protected: bool) -> None:
        """
        :param cluster_id: The ClusterId to update.
        :param termination_protected: Termination protection indicator.

        stability
        :stability: experimental
        """
        props = EmrSetClusterTerminationProtectionProps(cluster_id=cluster_id, termination_protected=termination_protected)

        jsii.create(EmrSetClusterTerminationProtection, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrSetClusterTerminationProtectionProps", jsii_struct_bases=[], name_mapping={'cluster_id': 'clusterId', 'termination_protected': 'terminationProtected'})
class EmrSetClusterTerminationProtectionProps():
    def __init__(self, *, cluster_id: str, termination_protected: bool) -> None:
        """Properties for EmrSetClusterTerminationProtection.

        :param cluster_id: The ClusterId to update.
        :param termination_protected: Termination protection indicator.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_id': cluster_id,
            'termination_protected': termination_protected,
        }

    @builtins.property
    def cluster_id(self) -> str:
        """The ClusterId to update.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_id')

    @builtins.property
    def termination_protected(self) -> bool:
        """Termination protection indicator.

        stability
        :stability: experimental
        """
        return self._values.get('termination_protected')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmrSetClusterTerminationProtectionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EmrTerminateCluster(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrTerminateCluster"):
    """A Step Functions Task to terminate an EMR Cluster.

    stability
    :stability: experimental
    """
    def __init__(self, *, cluster_id: str, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None) -> None:
        """
        :param cluster_id: The ClusterId to terminate.
        :param integration_pattern: The service integration pattern indicates different ways to call TerminateCluster. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC

        stability
        :stability: experimental
        """
        props = EmrTerminateClusterProps(cluster_id=cluster_id, integration_pattern=integration_pattern)

        jsii.create(EmrTerminateCluster, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrTerminateClusterProps", jsii_struct_bases=[], name_mapping={'cluster_id': 'clusterId', 'integration_pattern': 'integrationPattern'})
class EmrTerminateClusterProps():
    def __init__(self, *, cluster_id: str, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None) -> None:
        """Properties for EmrTerminateCluster.

        :param cluster_id: The ClusterId to terminate.
        :param integration_pattern: The service integration pattern indicates different ways to call TerminateCluster. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_id': cluster_id,
        }
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern

    @builtins.property
    def cluster_id(self) -> str:
        """The ClusterId to terminate.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_id')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call TerminateCluster.

        The valid value is either FIRE_AND_FORGET or SYNC.

        default
        :default: SYNC

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmrTerminateClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EvaluateExpression(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.EvaluateExpression"):
    """A Step Functions Task to evaluate an expression.

    OUTPUT: the output of this task is the evaluated expression.

    stability
    :stability: experimental
    """
    def __init__(self, *, expression: str, runtime: typing.Optional[aws_cdk.aws_lambda.Runtime]=None) -> None:
        """
        :param expression: The expression to evaluate. The expression may contain state paths.
        :param runtime: The runtime language to use to evaluate the expression. Default: lambda.Runtime.NODEJS_10_X

        stability
        :stability: experimental
        """
        props = EvaluateExpressionProps(expression=expression, runtime=runtime)

        jsii.create(EvaluateExpression, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EvaluateExpressionProps", jsii_struct_bases=[], name_mapping={'expression': 'expression', 'runtime': 'runtime'})
class EvaluateExpressionProps():
    def __init__(self, *, expression: str, runtime: typing.Optional[aws_cdk.aws_lambda.Runtime]=None) -> None:
        """Properties for EvaluateExpression.

        :param expression: The expression to evaluate. The expression may contain state paths.
        :param runtime: The runtime language to use to evaluate the expression. Default: lambda.Runtime.NODEJS_10_X

        stability
        :stability: experimental
        """
        self._values = {
            'expression': expression,
        }
        if runtime is not None: self._values["runtime"] = runtime

    @builtins.property
    def expression(self) -> str:
        """The expression to evaluate.

        The expression may contain state paths.

        stability
        :stability: experimental

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            "$.a + $.b"
        """
        return self._values.get('expression')

    @builtins.property
    def runtime(self) -> typing.Optional[aws_cdk.aws_lambda.Runtime]:
        """The runtime language to use to evaluate the expression.

        default
        :default: lambda.Runtime.NODEJS_10_X

        stability
        :stability: experimental
        """
        return self._values.get('runtime')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EvaluateExpressionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class GlueStartJobRun(aws_cdk.aws_stepfunctions.TaskStateBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.GlueStartJobRun"):
    """Starts an AWS Glue job in a Task state.

    OUTPUT: the output of this task is a JobRun structure, for details consult
    https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-runs.html#aws-glue-api-jobs-runs-JobRun

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, glue_job_name: str, arguments: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]=None, notify_delay_after: typing.Optional[aws_cdk.core.Duration]=None, security_configuration: typing.Optional[str]=None, comment: typing.Optional[str]=None, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, input_path: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param glue_job_name: Glue job name.
        :param arguments: The job arguments specifically for this run. For this job run, they replace the default arguments set in the job definition itself. Default: - Default arguments set in the job definition
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification. Must be at least 1 minute. Default: - Default delay set in the job definition
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this job run. This must match the Glue API Default: - Default configuration set in the job definition
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        stability
        :stability: experimental
        """
        props = GlueStartJobRunProps(glue_job_name=glue_job_name, arguments=arguments, notify_delay_after=notify_delay_after, security_configuration=security_configuration, comment=comment, heartbeat=heartbeat, input_path=input_path, integration_pattern=integration_pattern, output_path=output_path, result_path=result_path, timeout=timeout)

        jsii.create(GlueStartJobRun, self, [scope, id, props])

    @jsii.member(jsii_name="renderTask")
    def _render_task(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderTask", [])

    @builtins.property
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.GlueStartJobRunProps", jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps], name_mapping={'comment': 'comment', 'heartbeat': 'heartbeat', 'input_path': 'inputPath', 'integration_pattern': 'integrationPattern', 'output_path': 'outputPath', 'result_path': 'resultPath', 'timeout': 'timeout', 'glue_job_name': 'glueJobName', 'arguments': 'arguments', 'notify_delay_after': 'notifyDelayAfter', 'security_configuration': 'securityConfiguration'})
class GlueStartJobRunProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(self, *, comment: typing.Optional[str]=None, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, input_path: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, glue_job_name: str, arguments: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]=None, notify_delay_after: typing.Optional[aws_cdk.core.Duration]=None, security_configuration: typing.Optional[str]=None) -> None:
        """Properties for starting an AWS Glue job as a task.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param glue_job_name: Glue job name.
        :param arguments: The job arguments specifically for this run. For this job run, they replace the default arguments set in the job definition itself. Default: - Default arguments set in the job definition
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification. Must be at least 1 minute. Default: - Default delay set in the job definition
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this job run. This must match the Glue API Default: - Default configuration set in the job definition

        stability
        :stability: experimental
        """
        self._values = {
            'glue_job_name': glue_job_name,
        }
        if comment is not None: self._values["comment"] = comment
        if heartbeat is not None: self._values["heartbeat"] = heartbeat
        if input_path is not None: self._values["input_path"] = input_path
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if output_path is not None: self._values["output_path"] = output_path
        if result_path is not None: self._values["result_path"] = result_path
        if timeout is not None: self._values["timeout"] = timeout
        if arguments is not None: self._values["arguments"] = arguments
        if notify_delay_after is not None: self._values["notify_delay_after"] = notify_delay_after
        if security_configuration is not None: self._values["security_configuration"] = security_configuration

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: - No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('heartbeat')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: - The entire task input (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        default
        :default: IntegrationPattern.REQUEST_RESPONSE

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default:

        - The entire JSON node determined by the state input, the task result,
          and resultPath is passed to the next state (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: - Replaces the entire input with the result (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def glue_job_name(self) -> str:
        """Glue job name.

        stability
        :stability: experimental
        """
        return self._values.get('glue_job_name')

    @builtins.property
    def arguments(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """The job arguments specifically for this run.

        For this job run, they replace the default arguments set in the job
        definition itself.

        default
        :default: - Default arguments set in the job definition

        stability
        :stability: experimental
        """
        return self._values.get('arguments')

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """After a job run starts, the number of minutes to wait before sending a job run delay notification.

        Must be at least 1 minute.

        default
        :default: - Default delay set in the job definition

        stability
        :stability: experimental
        """
        return self._values.get('notify_delay_after')

    @builtins.property
    def security_configuration(self) -> typing.Optional[str]:
        """The name of the SecurityConfiguration structure to be used with this job run.

        This must match the Glue API

        default
        :default: - Default configuration set in the job definition

        see
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html#aws-glue-api-regex-oneLine
        stability
        :stability: experimental
        """
        return self._values.get('security_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GlueStartJobRunProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions-tasks.ISageMakerTask")
class ISageMakerTask(aws_cdk.aws_stepfunctions.IStepFunctionsTask, aws_cdk.aws_iam.IGrantable, jsii.compat.Protocol):
    """Task to train a machine learning model using Amazon SageMaker.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISageMakerTaskProxy

    pass

class _ISageMakerTaskProxy(jsii.proxy_for(aws_cdk.aws_stepfunctions.IStepFunctionsTask), jsii.proxy_for(aws_cdk.aws_iam.IGrantable)):
    """Task to train a machine learning model using Amazon SageMaker.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-stepfunctions-tasks.ISageMakerTask"
    pass

@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.InputMode")
class InputMode(enum.Enum):
    """Input mode that the algorithm supports.

    stability
    :stability: experimental
    """
    PIPE = "PIPE"
    """Pipe mode.

    stability
    :stability: experimental
    """
    FILE = "FILE"
    """File mode.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvocationType")
class InvocationType(enum.Enum):
    """Invocation type of a Lambda.

    stability
    :stability: experimental
    """
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    """Invoke synchronously.

    The API response includes the function response and additional data.

    stability
    :stability: experimental
    """
    EVENT = "EVENT"
    """Invoke asynchronously.

    Send events that fail multiple times to the function's dead-letter queue (if it's configured).
    The API response only includes a status code.

    stability
    :stability: experimental
    """
    DRY_RUN = "DRY_RUN"
    """TValidate parameter values and verify that the user or role has permission to invoke the function.

    stability
    :stability: experimental
    """

@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class InvokeActivity(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvokeActivity"):
    """A Step Functions Task to invoke an Activity worker.

    An Activity can be used directly as a Resource.

    stability
    :stability: experimental
    """
    def __init__(self, activity: aws_cdk.aws_stepfunctions.IActivity, *, heartbeat: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param activity: -
        :param heartbeat: Maximum time between heart beats. If the time between heart beats takes longer than this, a 'Timeout' error is raised. Default: No heart beat timeout

        stability
        :stability: experimental
        """
        props = InvokeActivityProps(heartbeat=heartbeat)

        jsii.create(InvokeActivity, self, [activity, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvokeActivityProps", jsii_struct_bases=[], name_mapping={'heartbeat': 'heartbeat'})
class InvokeActivityProps():
    def __init__(self, *, heartbeat: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Properties for FunctionTask.

        :param heartbeat: Maximum time between heart beats. If the time between heart beats takes longer than this, a 'Timeout' error is raised. Default: No heart beat timeout

        stability
        :stability: experimental
        """
        self._values = {
        }
        if heartbeat is not None: self._values["heartbeat"] = heartbeat

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum time between heart beats.

        If the time between heart beats takes longer than this, a 'Timeout' error is raised.

        default
        :default: No heart beat timeout

        stability
        :stability: experimental
        """
        return self._values.get('heartbeat')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'InvokeActivityProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class InvokeFunction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvokeFunction"):
    """A Step Functions Task to invoke a Lambda function.

    The Lambda function Arn is defined as Resource in the state machine definition.

    OUTPUT: the output of this task is the return value of the Lambda Function.

    deprecated
    :deprecated: Use ``LambdaInvoke``

    stability
    :stability: deprecated
    """
    def __init__(self, lambda_function: aws_cdk.aws_lambda.IFunction, *, payload: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> None:
        """
        :param lambda_function: -
        :param payload: The JSON that you want to provide to your Lambda function as input. This parameter is named as payload to keep consistent with RunLambdaTask class. Default: - The JSON data indicated by the task's InputPath is used as payload

        stability
        :stability: deprecated
        """
        props = InvokeFunctionProps(payload=payload)

        jsii.create(InvokeFunction, self, [lambda_function, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvokeFunctionProps", jsii_struct_bases=[], name_mapping={'payload': 'payload'})
class InvokeFunctionProps():
    def __init__(self, *, payload: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> None:
        """Properties for InvokeFunction.

        :param payload: The JSON that you want to provide to your Lambda function as input. This parameter is named as payload to keep consistent with RunLambdaTask class. Default: - The JSON data indicated by the task's InputPath is used as payload

        deprecated
        :deprecated: use ``LambdaInvoke``

        stability
        :stability: deprecated
        """
        self._values = {
        }
        if payload is not None: self._values["payload"] = payload

    @builtins.property
    def payload(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The JSON that you want to provide to your Lambda function as input.

        This parameter is named as payload to keep consistent with RunLambdaTask class.

        default
        :default: - The JSON data indicated by the task's InputPath is used as payload

        stability
        :stability: deprecated
        """
        return self._values.get('payload')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'InvokeFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.JobDependency", jsii_struct_bases=[], name_mapping={'job_id': 'jobId', 'type': 'type'})
class JobDependency():
    def __init__(self, *, job_id: typing.Optional[str]=None, type: typing.Optional[str]=None) -> None:
        """An object representing an AWS Batch job dependency.

        :param job_id: The job ID of the AWS Batch job associated with this dependency. Default: - No jobId
        :param type: The type of the job dependency. Default: - No type

        stability
        :stability: experimental
        """
        self._values = {
        }
        if job_id is not None: self._values["job_id"] = job_id
        if type is not None: self._values["type"] = type

    @builtins.property
    def job_id(self) -> typing.Optional[str]:
        """The job ID of the AWS Batch job associated with this dependency.

        default
        :default: - No jobId

        stability
        :stability: experimental
        """
        return self._values.get('job_id')

    @builtins.property
    def type(self) -> typing.Optional[str]:
        """The type of the job dependency.

        default
        :default: - No type

        stability
        :stability: experimental
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JobDependency(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.LambdaInvocationType")
class LambdaInvocationType(enum.Enum):
    """Invocation type of a Lambda.

    stability
    :stability: experimental
    """
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    """Invoke the function synchronously.

    Keep the connection open until the function returns a response or times out.
    The API response includes the function response and additional data.

    stability
    :stability: experimental
    """
    EVENT = "EVENT"
    """Invoke the function asynchronously.

    Send events that fail multiple times to the function's dead-letter queue (if it's configured).
    The API response only includes a status code.

    stability
    :stability: experimental
    """
    DRY_RUN = "DRY_RUN"
    """Validate parameter values and verify that the user or role has permission to invoke the function.

    stability
    :stability: experimental
    """

class LambdaInvoke(aws_cdk.aws_stepfunctions.TaskStateBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.LambdaInvoke"):
    """Invoke a Lambda function as a Task.

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, lambda_function: aws_cdk.aws_lambda.IFunction, client_context: typing.Optional[str]=None, invocation_type: typing.Optional["LambdaInvocationType"]=None, payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]=None, qualifier: typing.Optional[str]=None, comment: typing.Optional[str]=None, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, input_path: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param lambda_function: Lambda function to invoke.
        :param client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function. Default: - No context
        :param invocation_type: Invocation type of the Lambda function. Default: InvocationType.REQUEST_RESPONSE
        :param payload: The JSON that will be supplied as input to the Lambda function. Default: - The state input (JSON path '$')
        :param qualifier: Version or alias to invoke a published version of the function. You only need to supply this if you want the version of the Lambda Function to depend on data in the state machine state. If not, you can pass the appropriate Alias or Version object directly as the ``lambdaFunction`` argument. Default: - Version or alias inherent to the ``lambdaFunction`` object.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        stability
        :stability: experimental
        """
        props = LambdaInvokeProps(lambda_function=lambda_function, client_context=client_context, invocation_type=invocation_type, payload=payload, qualifier=qualifier, comment=comment, heartbeat=heartbeat, input_path=input_path, integration_pattern=integration_pattern, output_path=output_path, result_path=result_path, timeout=timeout)

        jsii.create(LambdaInvoke, self, [scope, id, props])

    @jsii.member(jsii_name="renderTask")
    def _render_task(self) -> typing.Any:
        """Provides the Lambda Invoke service integration task configuration.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderTask", [])

    @builtins.property
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.LambdaInvokeProps", jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps], name_mapping={'comment': 'comment', 'heartbeat': 'heartbeat', 'input_path': 'inputPath', 'integration_pattern': 'integrationPattern', 'output_path': 'outputPath', 'result_path': 'resultPath', 'timeout': 'timeout', 'lambda_function': 'lambdaFunction', 'client_context': 'clientContext', 'invocation_type': 'invocationType', 'payload': 'payload', 'qualifier': 'qualifier'})
class LambdaInvokeProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(self, *, comment: typing.Optional[str]=None, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, input_path: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, lambda_function: aws_cdk.aws_lambda.IFunction, client_context: typing.Optional[str]=None, invocation_type: typing.Optional["LambdaInvocationType"]=None, payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]=None, qualifier: typing.Optional[str]=None) -> None:
        """Properties for invoking a Lambda function with LambdaInvoke.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param lambda_function: Lambda function to invoke.
        :param client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function. Default: - No context
        :param invocation_type: Invocation type of the Lambda function. Default: InvocationType.REQUEST_RESPONSE
        :param payload: The JSON that will be supplied as input to the Lambda function. Default: - The state input (JSON path '$')
        :param qualifier: Version or alias to invoke a published version of the function. You only need to supply this if you want the version of the Lambda Function to depend on data in the state machine state. If not, you can pass the appropriate Alias or Version object directly as the ``lambdaFunction`` argument. Default: - Version or alias inherent to the ``lambdaFunction`` object.

        stability
        :stability: experimental
        """
        self._values = {
            'lambda_function': lambda_function,
        }
        if comment is not None: self._values["comment"] = comment
        if heartbeat is not None: self._values["heartbeat"] = heartbeat
        if input_path is not None: self._values["input_path"] = input_path
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if output_path is not None: self._values["output_path"] = output_path
        if result_path is not None: self._values["result_path"] = result_path
        if timeout is not None: self._values["timeout"] = timeout
        if client_context is not None: self._values["client_context"] = client_context
        if invocation_type is not None: self._values["invocation_type"] = invocation_type
        if payload is not None: self._values["payload"] = payload
        if qualifier is not None: self._values["qualifier"] = qualifier

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: - No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('heartbeat')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: - The entire task input (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        default
        :default: IntegrationPattern.REQUEST_RESPONSE

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default:

        - The entire JSON node determined by the state input, the task result,
          and resultPath is passed to the next state (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: - Replaces the entire input with the result (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        """Lambda function to invoke.

        stability
        :stability: experimental
        """
        return self._values.get('lambda_function')

    @builtins.property
    def client_context(self) -> typing.Optional[str]:
        """Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function.

        default
        :default: - No context

        stability
        :stability: experimental
        """
        return self._values.get('client_context')

    @builtins.property
    def invocation_type(self) -> typing.Optional["LambdaInvocationType"]:
        """Invocation type of the Lambda function.

        default
        :default: InvocationType.REQUEST_RESPONSE

        stability
        :stability: experimental
        """
        return self._values.get('invocation_type')

    @builtins.property
    def payload(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """The JSON that will be supplied as input to the Lambda function.

        default
        :default: - The state input (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('payload')

    @builtins.property
    def qualifier(self) -> typing.Optional[str]:
        """Version or alias to invoke a published version of the function.

        You only need to supply this if you want the version of the Lambda Function to depend
        on data in the state machine state. If not, you can pass the appropriate Alias or Version object
        directly as the ``lambdaFunction`` argument.

        default
        :default: - Version or alias inherent to the ``lambdaFunction`` object.

        stability
        :stability: experimental
        """
        return self._values.get('qualifier')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaInvokeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.MetricDefinition", jsii_struct_bases=[], name_mapping={'name': 'name', 'regex': 'regex'})
class MetricDefinition():
    def __init__(self, *, name: str, regex: str) -> None:
        """Specifies the metric name and regular expressions used to parse algorithm logs.

        :param name: Name of the metric.
        :param regex: Regular expression that searches the output of a training job and gets the value of the metric.

        stability
        :stability: experimental
        """
        self._values = {
            'name': name,
            'regex': regex,
        }

    @builtins.property
    def name(self) -> str:
        """Name of the metric.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def regex(self) -> str:
        """Regular expression that searches the output of a training job and gets the value of the metric.

        stability
        :stability: experimental
        """
        return self._values.get('regex')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricDefinition(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.OutputDataConfig", jsii_struct_bases=[], name_mapping={'s3_output_location': 's3OutputLocation', 'encryption_key': 'encryptionKey'})
class OutputDataConfig():
    def __init__(self, *, s3_output_location: "S3Location", encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> None:
        """Configures the S3 bucket where SageMaker will save the result of model training.

        :param s3_output_location: Identifies the S3 path where you want Amazon SageMaker to store the model artifacts.
        :param encryption_key: Optional KMS encryption key that Amazon SageMaker uses to encrypt the model artifacts at rest using Amazon S3 server-side encryption. Default: - Amazon SageMaker uses the default KMS key for Amazon S3 for your role's account

        stability
        :stability: experimental
        """
        self._values = {
            's3_output_location': s3_output_location,
        }
        if encryption_key is not None: self._values["encryption_key"] = encryption_key

    @builtins.property
    def s3_output_location(self) -> "S3Location":
        """Identifies the S3 path where you want Amazon SageMaker to store the model artifacts.

        stability
        :stability: experimental
        """
        return self._values.get('s3_output_location')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key that Amazon SageMaker uses to encrypt the model artifacts at rest using Amazon S3 server-side encryption.

        default
        :default: - Amazon SageMaker uses the default KMS key for Amazon S3 for your role's account

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OutputDataConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class PublishToTopic(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.PublishToTopic"):
    """A Step Functions Task to publish messages to SNS topic.

    A Function can be used directly as a Resource, but this class mirrors
    integration with other AWS services via a specific class instance.

    deprecated
    :deprecated: Use ``SnsPublish``

    stability
    :stability: deprecated
    """
    def __init__(self, topic: aws_cdk.aws_sns.ITopic, *, message: aws_cdk.aws_stepfunctions.TaskInput, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, message_per_subscription_type: typing.Optional[bool]=None, subject: typing.Optional[str]=None) -> None:
        """
        :param topic: -
        :param message: The text message to send to the topic.
        :param integration_pattern: The service integration pattern indicates different ways to call Publish to SNS. The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param message_per_subscription_type: If true, send a different message to every subscription type. If this is set to true, message must be a JSON object with a "default" key and a key for every subscription type (such as "sqs", "email", etc.) The values are strings representing the messages being sent to every subscription type. Default: false
        :param subject: Used as the "Subject" line when the message is delivered to email endpoints. Also included, if present, in the standard JSON messages delivered to other endpoints. Default: - No subject

        stability
        :stability: deprecated
        """
        props = PublishToTopicProps(message=message, integration_pattern=integration_pattern, message_per_subscription_type=message_per_subscription_type, subject=subject)

        jsii.create(PublishToTopic, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.PublishToTopicProps", jsii_struct_bases=[], name_mapping={'message': 'message', 'integration_pattern': 'integrationPattern', 'message_per_subscription_type': 'messagePerSubscriptionType', 'subject': 'subject'})
class PublishToTopicProps():
    def __init__(self, *, message: aws_cdk.aws_stepfunctions.TaskInput, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, message_per_subscription_type: typing.Optional[bool]=None, subject: typing.Optional[str]=None) -> None:
        """Properties for PublishTask.

        :param message: The text message to send to the topic.
        :param integration_pattern: The service integration pattern indicates different ways to call Publish to SNS. The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param message_per_subscription_type: If true, send a different message to every subscription type. If this is set to true, message must be a JSON object with a "default" key and a key for every subscription type (such as "sqs", "email", etc.) The values are strings representing the messages being sent to every subscription type. Default: false
        :param subject: Used as the "Subject" line when the message is delivered to email endpoints. Also included, if present, in the standard JSON messages delivered to other endpoints. Default: - No subject

        deprecated
        :deprecated: Use ``SnsPublish``

        stability
        :stability: deprecated
        """
        self._values = {
            'message': message,
        }
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if message_per_subscription_type is not None: self._values["message_per_subscription_type"] = message_per_subscription_type
        if subject is not None: self._values["subject"] = subject

    @builtins.property
    def message(self) -> aws_cdk.aws_stepfunctions.TaskInput:
        """The text message to send to the topic.

        stability
        :stability: deprecated
        """
        return self._values.get('message')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call Publish to SNS.

        The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: deprecated
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def message_per_subscription_type(self) -> typing.Optional[bool]:
        """If true, send a different message to every subscription type.

        If this is set to true, message must be a JSON object with a
        "default" key and a key for every subscription type (such as "sqs",
        "email", etc.) The values are strings representing the messages
        being sent to every subscription type.

        default
        :default: false

        see
        :see: https://docs.aws.amazon.com/sns/latest/api/API_Publish.html#API_Publish_RequestParameters
        stability
        :stability: deprecated
        """
        return self._values.get('message_per_subscription_type')

    @builtins.property
    def subject(self) -> typing.Optional[str]:
        """Used as the "Subject" line when the message is delivered to email endpoints.

        Also included, if present, in the standard JSON messages delivered to other endpoints.

        default
        :default: - No subject

        stability
        :stability: deprecated
        """
        return self._values.get('subject')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PublishToTopicProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.RecordWrapperType")
class RecordWrapperType(enum.Enum):
    """Define the format of the input data.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """None record wrapper type.

    stability
    :stability: experimental
    """
    RECORD_IO = "RECORD_IO"
    """RecordIO record wrapper type.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.ResourceConfig", jsii_struct_bases=[], name_mapping={'instance_count': 'instanceCount', 'instance_type': 'instanceType', 'volume_size_in_gb': 'volumeSizeInGB', 'volume_encryption_key': 'volumeEncryptionKey'})
class ResourceConfig():
    def __init__(self, *, instance_count: jsii.Number, instance_type: aws_cdk.aws_ec2.InstanceType, volume_size_in_gb: jsii.Number, volume_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> None:
        """Specifies the resources, ML compute instances, and ML storage volumes to deploy for model training.

        :param instance_count: The number of ML compute instances to use. Default: 1 instance.
        :param instance_type: ML compute instance type. Default: is the 'm4.xlarge' instance type.
        :param volume_size_in_gb: Size of the ML storage volume that you want to provision. Default: 10 GB EBS volume.
        :param volume_encryption_key: KMS key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance(s) that run the training job. Default: - Amazon SageMaker uses the default KMS key for Amazon S3 for your role's account

        stability
        :stability: experimental
        """
        self._values = {
            'instance_count': instance_count,
            'instance_type': instance_type,
            'volume_size_in_gb': volume_size_in_gb,
        }
        if volume_encryption_key is not None: self._values["volume_encryption_key"] = volume_encryption_key

    @builtins.property
    def instance_count(self) -> jsii.Number:
        """The number of ML compute instances to use.

        default
        :default: 1 instance.

        stability
        :stability: experimental
        """
        return self._values.get('instance_count')

    @builtins.property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        """ML compute instance type.

        default
        :default: is the 'm4.xlarge' instance type.

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def volume_size_in_gb(self) -> jsii.Number:
        """Size of the ML storage volume that you want to provision.

        default
        :default: 10 GB EBS volume.

        stability
        :stability: experimental
        """
        return self._values.get('volume_size_in_gb')

    @builtins.property
    def volume_encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """KMS key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance(s) that run the training job.

        default
        :default: - Amazon SageMaker uses the default KMS key for Amazon S3 for your role's account

        stability
        :stability: experimental
        """
        return self._values.get('volume_encryption_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResourceConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class RunBatchJob(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunBatchJob"):
    """A Step Functions Task to run AWS Batch.

    stability
    :stability: experimental
    """
    def __init__(self, *, job_definition: aws_cdk.aws_batch.IJobDefinition, job_name: str, job_queue: aws_cdk.aws_batch.IJobQueue, array_size: typing.Optional[jsii.Number]=None, attempts: typing.Optional[jsii.Number]=None, container_overrides: typing.Optional["ContainerOverrides"]=None, depends_on: typing.Optional[typing.List["JobDependency"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, payload: typing.Optional[typing.Mapping[str, typing.Any]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param job_definition: The job definition used by this job.
        :param job_name: The name of the job. The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.
        :param job_queue: The job queue into which the job is submitted.
        :param array_size: The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. For more information, see Array Jobs in the AWS Batch User Guide. Default: - No array size
        :param attempts: The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: - 1
        :param container_overrides: A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive. Default: - No container overrides
        :param depends_on: A list of dependencies for the job. A job can depend upon a maximum of 20 jobs. Default: - No dependencies
        :param integration_pattern: The service integration pattern indicates different ways to call TerminateCluster. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC
        :param payload: The payload to be passed as parametrs to the batch job. Default: - No parameters are passed
        :param timeout: The timeout configuration for this SubmitJob operation. The minimum value for the timeout is 60 seconds. Default: - No timeout

        stability
        :stability: experimental
        """
        props = RunBatchJobProps(job_definition=job_definition, job_name=job_name, job_queue=job_queue, array_size=array_size, attempts=attempts, container_overrides=container_overrides, depends_on=depends_on, integration_pattern=integration_pattern, payload=payload, timeout=timeout)

        jsii.create(RunBatchJob, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunBatchJobProps", jsii_struct_bases=[], name_mapping={'job_definition': 'jobDefinition', 'job_name': 'jobName', 'job_queue': 'jobQueue', 'array_size': 'arraySize', 'attempts': 'attempts', 'container_overrides': 'containerOverrides', 'depends_on': 'dependsOn', 'integration_pattern': 'integrationPattern', 'payload': 'payload', 'timeout': 'timeout'})
class RunBatchJobProps():
    def __init__(self, *, job_definition: aws_cdk.aws_batch.IJobDefinition, job_name: str, job_queue: aws_cdk.aws_batch.IJobQueue, array_size: typing.Optional[jsii.Number]=None, attempts: typing.Optional[jsii.Number]=None, container_overrides: typing.Optional["ContainerOverrides"]=None, depends_on: typing.Optional[typing.List["JobDependency"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, payload: typing.Optional[typing.Mapping[str, typing.Any]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Properties for RunBatchJob.

        :param job_definition: The job definition used by this job.
        :param job_name: The name of the job. The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.
        :param job_queue: The job queue into which the job is submitted.
        :param array_size: The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. For more information, see Array Jobs in the AWS Batch User Guide. Default: - No array size
        :param attempts: The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: - 1
        :param container_overrides: A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive. Default: - No container overrides
        :param depends_on: A list of dependencies for the job. A job can depend upon a maximum of 20 jobs. Default: - No dependencies
        :param integration_pattern: The service integration pattern indicates different ways to call TerminateCluster. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC
        :param payload: The payload to be passed as parametrs to the batch job. Default: - No parameters are passed
        :param timeout: The timeout configuration for this SubmitJob operation. The minimum value for the timeout is 60 seconds. Default: - No timeout

        stability
        :stability: experimental
        """
        if isinstance(container_overrides, dict): container_overrides = ContainerOverrides(**container_overrides)
        self._values = {
            'job_definition': job_definition,
            'job_name': job_name,
            'job_queue': job_queue,
        }
        if array_size is not None: self._values["array_size"] = array_size
        if attempts is not None: self._values["attempts"] = attempts
        if container_overrides is not None: self._values["container_overrides"] = container_overrides
        if depends_on is not None: self._values["depends_on"] = depends_on
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if payload is not None: self._values["payload"] = payload
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def job_definition(self) -> aws_cdk.aws_batch.IJobDefinition:
        """The job definition used by this job.

        stability
        :stability: experimental
        """
        return self._values.get('job_definition')

    @builtins.property
    def job_name(self) -> str:
        """The name of the job.

        The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase),
        numbers, hyphens, and underscores are allowed.

        stability
        :stability: experimental
        """
        return self._values.get('job_name')

    @builtins.property
    def job_queue(self) -> aws_cdk.aws_batch.IJobQueue:
        """The job queue into which the job is submitted.

        stability
        :stability: experimental
        """
        return self._values.get('job_queue')

    @builtins.property
    def array_size(self) -> typing.Optional[jsii.Number]:
        """The array size can be between 2 and 10,000.

        If you specify array properties for a job, it becomes an array job.
        For more information, see Array Jobs in the AWS Batch User Guide.

        default
        :default: - No array size

        stability
        :stability: experimental
        """
        return self._values.get('array_size')

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        """The number of times to move a job to the RUNNABLE status.

        You may specify between 1 and 10 attempts.
        If the value of attempts is greater than one,
        the job is retried on failure the same number of attempts as the value.

        default
        :default: - 1

        stability
        :stability: experimental
        """
        return self._values.get('attempts')

    @builtins.property
    def container_overrides(self) -> typing.Optional["ContainerOverrides"]:
        """A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive.

        default
        :default: - No container overrides

        see
        :see: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-containerOverrides
        stability
        :stability: experimental
        """
        return self._values.get('container_overrides')

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["JobDependency"]]:
        """A list of dependencies for the job.

        A job can depend upon a maximum of 20 jobs.

        default
        :default: - No dependencies

        see
        :see: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-dependsOn
        stability
        :stability: experimental
        """
        return self._values.get('depends_on')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call TerminateCluster.

        The valid value is either FIRE_AND_FORGET or SYNC.

        default
        :default: SYNC

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def payload(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The payload to be passed as parametrs to the batch job.

        default
        :default: - No parameters are passed

        stability
        :stability: experimental
        """
        return self._values.get('payload')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The timeout configuration for this SubmitJob operation.

        The minimum value for the timeout is 60 seconds.

        default
        :default: - No timeout

        see
        :see: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-timeout
        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RunBatchJobProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class RunEcsEc2Task(EcsRunTaskBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunEcsEc2Task"):
    """Run an ECS/EC2 Task in a StepFunctions workflow.

    stability
    :stability: experimental
    """
    def __init__(self, *, placement_constraints: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]]=None, placement_strategies: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None) -> None:
        """
        :param placement_constraints: Placement constraints. Default: No constraints
        :param placement_strategies: Placement strategies. Default: No strategies
        :param security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnets: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        props = RunEcsEc2TaskProps(placement_constraints=placement_constraints, placement_strategies=placement_strategies, security_group=security_group, subnets=subnets, cluster=cluster, task_definition=task_definition, container_overrides=container_overrides, integration_pattern=integration_pattern)

        jsii.create(RunEcsEc2Task, self, [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunEcsEc2TaskProps", jsii_struct_bases=[CommonEcsRunTaskProps], name_mapping={'cluster': 'cluster', 'task_definition': 'taskDefinition', 'container_overrides': 'containerOverrides', 'integration_pattern': 'integrationPattern', 'placement_constraints': 'placementConstraints', 'placement_strategies': 'placementStrategies', 'security_group': 'securityGroup', 'subnets': 'subnets'})
class RunEcsEc2TaskProps(CommonEcsRunTaskProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, placement_constraints: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]]=None, placement_strategies: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """Properties to run an ECS task on EC2 in StepFunctionsan ECS.

        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param placement_constraints: Placement constraints. Default: No constraints
        :param placement_strategies: Placement strategies. Default: No strategies
        :param security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnets: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets

        stability
        :stability: experimental
        """
        if isinstance(subnets, dict): subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if container_overrides is not None: self._values["container_overrides"] = container_overrides
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None: self._values["placement_strategies"] = placement_strategies
        if security_group is not None: self._values["security_group"] = security_group
        if subnets is not None: self._values["subnets"] = subnets

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The topic to run the task on.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List["ContainerOverride"]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        default
        :default: - No overrides

        stability
        :stability: experimental
        """
        return self._values.get('container_overrides')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call RunTask in ECS.

        The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def placement_constraints(self) -> typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]]:
        """Placement constraints.

        default
        :default: No constraints

        stability
        :stability: experimental
        """
        return self._values.get('placement_constraints')

    @builtins.property
    def placement_strategies(self) -> typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]]:
        """Placement strategies.

        default
        :default: No strategies

        stability
        :stability: experimental
        """
        return self._values.get('placement_strategies')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Existing security group to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        default
        :default: A new security group is created

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        default
        :default: Private subnets

        stability
        :stability: experimental
        """
        return self._values.get('subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RunEcsEc2TaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class RunEcsFargateTask(EcsRunTaskBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunEcsFargateTask"):
    """Start a service on an ECS cluster.

    stability
    :stability: experimental
    """
    def __init__(self, *, assign_public_ip: typing.Optional[bool]=None, platform_version: typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None) -> None:
        """
        :param assign_public_ip: Assign public IP addresses to each task. Default: false
        :param platform_version: Fargate platform version to run this service on. Unless you have specific compatibility requirements, you don't need to specify this. Default: Latest
        :param security_group: Existing security group to use for the tasks. Default: A new security group is created
        :param subnets: In what subnets to place the task's ENIs. Default: Private subnet if assignPublicIp, public subnets otherwise
        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        props = RunEcsFargateTaskProps(assign_public_ip=assign_public_ip, platform_version=platform_version, security_group=security_group, subnets=subnets, cluster=cluster, task_definition=task_definition, container_overrides=container_overrides, integration_pattern=integration_pattern)

        jsii.create(RunEcsFargateTask, self, [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunEcsFargateTaskProps", jsii_struct_bases=[CommonEcsRunTaskProps], name_mapping={'cluster': 'cluster', 'task_definition': 'taskDefinition', 'container_overrides': 'containerOverrides', 'integration_pattern': 'integrationPattern', 'assign_public_ip': 'assignPublicIp', 'platform_version': 'platformVersion', 'security_group': 'securityGroup', 'subnets': 'subnets'})
class RunEcsFargateTaskProps(CommonEcsRunTaskProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, assign_public_ip: typing.Optional[bool]=None, platform_version: typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """Properties to define an ECS service.

        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param assign_public_ip: Assign public IP addresses to each task. Default: false
        :param platform_version: Fargate platform version to run this service on. Unless you have specific compatibility requirements, you don't need to specify this. Default: Latest
        :param security_group: Existing security group to use for the tasks. Default: A new security group is created
        :param subnets: In what subnets to place the task's ENIs. Default: Private subnet if assignPublicIp, public subnets otherwise

        stability
        :stability: experimental
        """
        if isinstance(subnets, dict): subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if container_overrides is not None: self._values["container_overrides"] = container_overrides
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if platform_version is not None: self._values["platform_version"] = platform_version
        if security_group is not None: self._values["security_group"] = security_group
        if subnets is not None: self._values["subnets"] = subnets

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The topic to run the task on.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List["ContainerOverride"]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        default
        :default: - No overrides

        stability
        :stability: experimental
        """
        return self._values.get('container_overrides')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call RunTask in ECS.

        The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Assign public IP addresses to each task.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def platform_version(self) -> typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion]:
        """Fargate platform version to run this service on.

        Unless you have specific compatibility requirements, you don't need to
        specify this.

        default
        :default: Latest

        stability
        :stability: experimental
        """
        return self._values.get('platform_version')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Existing security group to use for the tasks.

        default
        :default: A new security group is created

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """In what subnets to place the task's ENIs.

        default
        :default: Private subnet if assignPublicIp, public subnets otherwise

        stability
        :stability: experimental
        """
        return self._values.get('subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RunEcsFargateTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class RunGlueJobTask(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunGlueJobTask"):
    """Invoke a Glue job as a Task.

    OUTPUT: the output of this task is a JobRun structure, for details consult
    https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-runs.html#aws-glue-api-jobs-runs-JobRun

    deprecated
    :deprecated: use ``GlueStartJobRun``

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html
    stability
    :stability: deprecated
    """
    def __init__(self, glue_job_name: str, *, arguments: typing.Optional[typing.Mapping[str, str]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, notify_delay_after: typing.Optional[aws_cdk.core.Duration]=None, security_configuration: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param glue_job_name: -
        :param arguments: The job arguments specifically for this run. For this job run, they replace the default arguments set in the job definition itself. Default: - Default arguments set in the job definition
        :param integration_pattern: The service integration pattern indicates different ways to start the Glue job. The valid value for Glue is either FIRE_AND_FORGET or SYNC. Default: FIRE_AND_FORGET
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification. Must be at least 1 minute. Default: - Default delay set in the job definition
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this job run. This must match the Glue API `single-line string pattern <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html#aws-glue-api-regex-oneLine>`_. Default: - Default configuration set in the job definition
        :param timeout: The job run timeout. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. Must be at least 1 minute. Default: - Default timeout set in the job definition

        stability
        :stability: deprecated
        """
        props = RunGlueJobTaskProps(arguments=arguments, integration_pattern=integration_pattern, notify_delay_after=notify_delay_after, security_configuration=security_configuration, timeout=timeout)

        jsii.create(RunGlueJobTask, self, [glue_job_name, props])

    @jsii.member(jsii_name="bind")
    def bind(self, task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunGlueJobTaskProps", jsii_struct_bases=[], name_mapping={'arguments': 'arguments', 'integration_pattern': 'integrationPattern', 'notify_delay_after': 'notifyDelayAfter', 'security_configuration': 'securityConfiguration', 'timeout': 'timeout'})
class RunGlueJobTaskProps():
    def __init__(self, *, arguments: typing.Optional[typing.Mapping[str, str]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, notify_delay_after: typing.Optional[aws_cdk.core.Duration]=None, security_configuration: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Properties for RunGlueJobTask.

        :param arguments: The job arguments specifically for this run. For this job run, they replace the default arguments set in the job definition itself. Default: - Default arguments set in the job definition
        :param integration_pattern: The service integration pattern indicates different ways to start the Glue job. The valid value for Glue is either FIRE_AND_FORGET or SYNC. Default: FIRE_AND_FORGET
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification. Must be at least 1 minute. Default: - Default delay set in the job definition
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this job run. This must match the Glue API `single-line string pattern <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html#aws-glue-api-regex-oneLine>`_. Default: - Default configuration set in the job definition
        :param timeout: The job run timeout. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. Must be at least 1 minute. Default: - Default timeout set in the job definition

        deprecated
        :deprecated: use ``GlueStartJobRun``

        stability
        :stability: deprecated
        """
        self._values = {
        }
        if arguments is not None: self._values["arguments"] = arguments
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if notify_delay_after is not None: self._values["notify_delay_after"] = notify_delay_after
        if security_configuration is not None: self._values["security_configuration"] = security_configuration
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def arguments(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The job arguments specifically for this run.

        For this job run, they replace the default arguments set in the job definition itself.

        default
        :default: - Default arguments set in the job definition

        stability
        :stability: deprecated
        """
        return self._values.get('arguments')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to start the Glue job.

        The valid value for Glue is either FIRE_AND_FORGET or SYNC.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: deprecated
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """After a job run starts, the number of minutes to wait before sending a job run delay notification.

        Must be at least 1 minute.

        default
        :default: - Default delay set in the job definition

        stability
        :stability: deprecated
        """
        return self._values.get('notify_delay_after')

    @builtins.property
    def security_configuration(self) -> typing.Optional[str]:
        """The name of the SecurityConfiguration structure to be used with this job run.

        This must match the Glue API
        `single-line string pattern <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html#aws-glue-api-regex-oneLine>`_.

        default
        :default: - Default configuration set in the job definition

        stability
        :stability: deprecated
        """
        return self._values.get('security_configuration')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The job run timeout.

        This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status.
        Must be at least 1 minute.

        default
        :default: - Default timeout set in the job definition

        stability
        :stability: deprecated
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RunGlueJobTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class RunLambdaTask(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunLambdaTask"):
    """Invoke a Lambda function as a Task.

    OUTPUT: the output of this task is either the return value of Lambda's
    Invoke call, or whatever the Lambda Function posted back using
    ``SendTaskSuccess/SendTaskFailure`` in ``waitForTaskToken`` mode.

    deprecated
    :deprecated: Use ``LambdaInvoke``

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html
    stability
    :stability: deprecated
    """
    def __init__(self, lambda_function: aws_cdk.aws_lambda.IFunction, *, client_context: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, invocation_type: typing.Optional["InvocationType"]=None, payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]=None, qualifier: typing.Optional[str]=None) -> None:
        """
        :param lambda_function: -
        :param client_context: Client context to pass to the function. Default: - No context
        :param integration_pattern: The service integration pattern indicates different ways to invoke Lambda function. The valid value for Lambda is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN, it determines whether to pause the workflow until a task token is returned. If this is set to WAIT_FOR_TASK_TOKEN, the Context.taskToken value must be included somewhere in the payload and the Lambda must call ``SendTaskSuccess/SendTaskFailure`` using that token. Default: FIRE_AND_FORGET
        :param invocation_type: Invocation type of the Lambda function. Default: RequestResponse
        :param payload: The JSON that you want to provide to your Lambda function as input. Default: - The state input (JSON path '$')
        :param qualifier: Version or alias of the function to be invoked. Default: - No qualifier

        stability
        :stability: deprecated
        """
        props = RunLambdaTaskProps(client_context=client_context, integration_pattern=integration_pattern, invocation_type=invocation_type, payload=payload, qualifier=qualifier)

        jsii.create(RunLambdaTask, self, [lambda_function, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunLambdaTaskProps", jsii_struct_bases=[], name_mapping={'client_context': 'clientContext', 'integration_pattern': 'integrationPattern', 'invocation_type': 'invocationType', 'payload': 'payload', 'qualifier': 'qualifier'})
class RunLambdaTaskProps():
    def __init__(self, *, client_context: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, invocation_type: typing.Optional["InvocationType"]=None, payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]=None, qualifier: typing.Optional[str]=None) -> None:
        """Properties for RunLambdaTask.

        :param client_context: Client context to pass to the function. Default: - No context
        :param integration_pattern: The service integration pattern indicates different ways to invoke Lambda function. The valid value for Lambda is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN, it determines whether to pause the workflow until a task token is returned. If this is set to WAIT_FOR_TASK_TOKEN, the Context.taskToken value must be included somewhere in the payload and the Lambda must call ``SendTaskSuccess/SendTaskFailure`` using that token. Default: FIRE_AND_FORGET
        :param invocation_type: Invocation type of the Lambda function. Default: RequestResponse
        :param payload: The JSON that you want to provide to your Lambda function as input. Default: - The state input (JSON path '$')
        :param qualifier: Version or alias of the function to be invoked. Default: - No qualifier

        deprecated
        :deprecated: Use ``LambdaInvoke``

        stability
        :stability: deprecated
        """
        self._values = {
        }
        if client_context is not None: self._values["client_context"] = client_context
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if invocation_type is not None: self._values["invocation_type"] = invocation_type
        if payload is not None: self._values["payload"] = payload
        if qualifier is not None: self._values["qualifier"] = qualifier

    @builtins.property
    def client_context(self) -> typing.Optional[str]:
        """Client context to pass to the function.

        default
        :default: - No context

        stability
        :stability: deprecated
        """
        return self._values.get('client_context')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to invoke Lambda function.

        The valid value for Lambda is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN,
        it determines whether to pause the workflow until a task token is returned.

        If this is set to WAIT_FOR_TASK_TOKEN, the Context.taskToken value must be included
        somewhere in the payload and the Lambda must call
        ``SendTaskSuccess/SendTaskFailure`` using that token.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: deprecated
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def invocation_type(self) -> typing.Optional["InvocationType"]:
        """Invocation type of the Lambda function.

        default
        :default: RequestResponse

        stability
        :stability: deprecated
        """
        return self._values.get('invocation_type')

    @builtins.property
    def payload(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """The JSON that you want to provide to your Lambda function as input.

        default
        :default: - The state input (JSON path '$')

        stability
        :stability: deprecated
        """
        return self._values.get('payload')

    @builtins.property
    def qualifier(self) -> typing.Optional[str]:
        """Version or alias of the function to be invoked.

        default
        :default: - No qualifier

        stability
        :stability: deprecated
        """
        return self._values.get('qualifier')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RunLambdaTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3DataDistributionType")
class S3DataDistributionType(enum.Enum):
    """S3 Data Distribution Type.

    stability
    :stability: experimental
    """
    FULLY_REPLICATED = "FULLY_REPLICATED"
    """Fully replicated S3 Data Distribution Type.

    stability
    :stability: experimental
    """
    SHARDED_BY_S3_KEY = "SHARDED_BY_S3_KEY"
    """Sharded By S3 Key Data Distribution Type.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3DataSource", jsii_struct_bases=[], name_mapping={'s3_location': 's3Location', 'attribute_names': 'attributeNames', 's3_data_distribution_type': 's3DataDistributionType', 's3_data_type': 's3DataType'})
class S3DataSource():
    def __init__(self, *, s3_location: "S3Location", attribute_names: typing.Optional[typing.List[str]]=None, s3_data_distribution_type: typing.Optional["S3DataDistributionType"]=None, s3_data_type: typing.Optional["S3DataType"]=None) -> None:
        """S3 location of the channel data.

        :param s3_location: S3 Uri.
        :param attribute_names: List of one or more attribute names to use that are found in a specified augmented manifest file. Default: - No attribute names
        :param s3_data_distribution_type: S3 Data Distribution Type. Default: - None
        :param s3_data_type: S3 Data Type. Default: S3_PREFIX

        see
        :see: https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_S3DataSource.html
        stability
        :stability: experimental
        """
        self._values = {
            's3_location': s3_location,
        }
        if attribute_names is not None: self._values["attribute_names"] = attribute_names
        if s3_data_distribution_type is not None: self._values["s3_data_distribution_type"] = s3_data_distribution_type
        if s3_data_type is not None: self._values["s3_data_type"] = s3_data_type

    @builtins.property
    def s3_location(self) -> "S3Location":
        """S3 Uri.

        stability
        :stability: experimental
        """
        return self._values.get('s3_location')

    @builtins.property
    def attribute_names(self) -> typing.Optional[typing.List[str]]:
        """List of one or more attribute names to use that are found in a specified augmented manifest file.

        default
        :default: - No attribute names

        stability
        :stability: experimental
        """
        return self._values.get('attribute_names')

    @builtins.property
    def s3_data_distribution_type(self) -> typing.Optional["S3DataDistributionType"]:
        """S3 Data Distribution Type.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('s3_data_distribution_type')

    @builtins.property
    def s3_data_type(self) -> typing.Optional["S3DataType"]:
        """S3 Data Type.

        default
        :default: S3_PREFIX

        stability
        :stability: experimental
        """
        return self._values.get('s3_data_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3DataSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3DataType")
class S3DataType(enum.Enum):
    """S3 Data Type.

    stability
    :stability: experimental
    """
    MANIFEST_FILE = "MANIFEST_FILE"
    """Manifest File Data Type.

    stability
    :stability: experimental
    """
    S3_PREFIX = "S3_PREFIX"
    """S3 Prefix Data Type.

    stability
    :stability: experimental
    """
    AUGMENTED_MANIFEST_FILE = "AUGMENTED_MANIFEST_FILE"
    """Augmented Manifest File Data Type.

    stability
    :stability: experimental
    """

class S3Location(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3Location"):
    """Constructs ``IS3Location`` objects.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _S3LocationProxy

    def __init__(self) -> None:
        jsii.create(S3Location, self, [])

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(cls, bucket: aws_cdk.aws_s3.IBucket, key_prefix: str) -> "S3Location":
        """An ``IS3Location`` built with a determined bucket and key prefix.

        :param bucket: is the bucket where the objects are to be stored.
        :param key_prefix: is the key prefix used by the location.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromBucket", [bucket, key_prefix])

    @jsii.member(jsii_name="fromJsonExpression")
    @builtins.classmethod
    def from_json_expression(cls, expression: str) -> "S3Location":
        """An ``IS3Location`` determined fully by a JSON Path from the task input.

        Due to the dynamic nature of those locations, the IAM grants that will be set by ``grantRead`` and ``grantWrite``
        apply to the ``*`` resource.

        :param expression: the JSON expression resolving to an S3 location URI.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJsonExpression", [expression])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, task: "ISageMakerTask", *, for_reading: typing.Optional[bool]=None, for_writing: typing.Optional[bool]=None) -> "S3LocationConfig":
        """Called when the S3Location is bound to a StepFunctions task.

        :param task: -
        :param for_reading: Allow reading from the S3 Location. Default: false
        :param for_writing: Allow writing to the S3 Location. Default: false

        stability
        :stability: experimental
        """
        ...


class _S3LocationProxy(S3Location):
    @jsii.member(jsii_name="bind")
    def bind(self, task: "ISageMakerTask", *, for_reading: typing.Optional[bool]=None, for_writing: typing.Optional[bool]=None) -> "S3LocationConfig":
        """Called when the S3Location is bound to a StepFunctions task.

        :param task: -
        :param for_reading: Allow reading from the S3 Location. Default: false
        :param for_writing: Allow writing to the S3 Location. Default: false

        stability
        :stability: experimental
        """
        opts = S3LocationBindOptions(for_reading=for_reading, for_writing=for_writing)

        return jsii.invoke(self, "bind", [task, opts])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3LocationBindOptions", jsii_struct_bases=[], name_mapping={'for_reading': 'forReading', 'for_writing': 'forWriting'})
class S3LocationBindOptions():
    def __init__(self, *, for_reading: typing.Optional[bool]=None, for_writing: typing.Optional[bool]=None) -> None:
        """Options for binding an S3 Location.

        :param for_reading: Allow reading from the S3 Location. Default: false
        :param for_writing: Allow writing to the S3 Location. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if for_reading is not None: self._values["for_reading"] = for_reading
        if for_writing is not None: self._values["for_writing"] = for_writing

    @builtins.property
    def for_reading(self) -> typing.Optional[bool]:
        """Allow reading from the S3 Location.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('for_reading')

    @builtins.property
    def for_writing(self) -> typing.Optional[bool]:
        """Allow writing to the S3 Location.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('for_writing')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3LocationBindOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3LocationConfig", jsii_struct_bases=[], name_mapping={'uri': 'uri'})
class S3LocationConfig():
    def __init__(self, *, uri: str) -> None:
        """Stores information about the location of an object in Amazon S3.

        :param uri: Uniquely identifies the resource in Amazon S3.

        stability
        :stability: experimental
        """
        self._values = {
            'uri': uri,
        }

    @builtins.property
    def uri(self) -> str:
        """Uniquely identifies the resource in Amazon S3.

        stability
        :stability: experimental
        """
        return self._values.get('uri')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3LocationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_iam.IGrantable, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class SagemakerTrainTask(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.SagemakerTrainTask"):
    """Class representing the SageMaker Create Training Job task.

    stability
    :stability: experimental
    """
    def __init__(self, *, algorithm_specification: "AlgorithmSpecification", input_data_config: typing.List["Channel"], output_data_config: "OutputDataConfig", training_job_name: str, hyperparameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, resource_config: typing.Optional["ResourceConfig"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, stopping_condition: typing.Optional["StoppingCondition"]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, vpc_config: typing.Optional["VpcConfig"]=None) -> None:
        """
        :param algorithm_specification: Identifies the training algorithm to use.
        :param input_data_config: Describes the various datasets (e.g. train, validation, test) and the Amazon S3 location where stored.
        :param output_data_config: Identifies the Amazon S3 location where you want Amazon SageMaker to save the results of model training.
        :param training_job_name: Training Job Name.
        :param hyperparameters: Algorithm-specific parameters that influence the quality of the model. Set hyperparameters before you start the learning process. For a list of hyperparameters provided by Amazon SageMaker Default: - No hyperparameters
        :param integration_pattern: The service integration pattern indicates different ways to call SageMaker APIs. The valid value is either FIRE_AND_FORGET or SYNC. Default: FIRE_AND_FORGET
        :param resource_config: Specifies the resources, ML compute instances, and ML storage volumes to deploy for model training. Default: - 1 instance of EC2 ``M4.XLarge`` with ``10GB`` volume
        :param role: Role for the Training Job. The role must be granted all necessary permissions for the SageMaker training job to be able to operate. See https://docs.aws.amazon.com/fr_fr/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-createtrainingjob-perms Default: - a role with appropriate permissions will be created.
        :param stopping_condition: Sets a time limit for training. Default: - max runtime of 1 hour
        :param tags: Tags to be applied to the train job. Default: - No tags
        :param vpc_config: Specifies the VPC that you want your training job to connect to. Default: - No VPC

        stability
        :stability: experimental
        """
        props = SagemakerTrainTaskProps(algorithm_specification=algorithm_specification, input_data_config=input_data_config, output_data_config=output_data_config, training_job_name=training_job_name, hyperparameters=hyperparameters, integration_pattern=integration_pattern, resource_config=resource_config, role=role, stopping_condition=stopping_condition, tags=tags, vpc_config=vpc_config)

        jsii.create(SagemakerTrainTask, self, [props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(self, security_group: aws_cdk.aws_ec2.ISecurityGroup) -> None:
        """Add the security group to all instances via the launch configuration security groups array.

        :param security_group: : The security group to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @jsii.member(jsii_name="bind")
    def bind(self, task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Allows specify security group connections for instances of this fleet.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The execution role for the Sagemaker training job.

        Only available after task has been added to a state machine.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.SagemakerTrainTaskProps", jsii_struct_bases=[], name_mapping={'algorithm_specification': 'algorithmSpecification', 'input_data_config': 'inputDataConfig', 'output_data_config': 'outputDataConfig', 'training_job_name': 'trainingJobName', 'hyperparameters': 'hyperparameters', 'integration_pattern': 'integrationPattern', 'resource_config': 'resourceConfig', 'role': 'role', 'stopping_condition': 'stoppingCondition', 'tags': 'tags', 'vpc_config': 'vpcConfig'})
class SagemakerTrainTaskProps():
    def __init__(self, *, algorithm_specification: "AlgorithmSpecification", input_data_config: typing.List["Channel"], output_data_config: "OutputDataConfig", training_job_name: str, hyperparameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, resource_config: typing.Optional["ResourceConfig"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, stopping_condition: typing.Optional["StoppingCondition"]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, vpc_config: typing.Optional["VpcConfig"]=None) -> None:
        """Properties for creating an Amazon SageMaker training job.

        :param algorithm_specification: Identifies the training algorithm to use.
        :param input_data_config: Describes the various datasets (e.g. train, validation, test) and the Amazon S3 location where stored.
        :param output_data_config: Identifies the Amazon S3 location where you want Amazon SageMaker to save the results of model training.
        :param training_job_name: Training Job Name.
        :param hyperparameters: Algorithm-specific parameters that influence the quality of the model. Set hyperparameters before you start the learning process. For a list of hyperparameters provided by Amazon SageMaker Default: - No hyperparameters
        :param integration_pattern: The service integration pattern indicates different ways to call SageMaker APIs. The valid value is either FIRE_AND_FORGET or SYNC. Default: FIRE_AND_FORGET
        :param resource_config: Specifies the resources, ML compute instances, and ML storage volumes to deploy for model training. Default: - 1 instance of EC2 ``M4.XLarge`` with ``10GB`` volume
        :param role: Role for the Training Job. The role must be granted all necessary permissions for the SageMaker training job to be able to operate. See https://docs.aws.amazon.com/fr_fr/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-createtrainingjob-perms Default: - a role with appropriate permissions will be created.
        :param stopping_condition: Sets a time limit for training. Default: - max runtime of 1 hour
        :param tags: Tags to be applied to the train job. Default: - No tags
        :param vpc_config: Specifies the VPC that you want your training job to connect to. Default: - No VPC

        stability
        :stability: experimental
        """
        if isinstance(algorithm_specification, dict): algorithm_specification = AlgorithmSpecification(**algorithm_specification)
        if isinstance(output_data_config, dict): output_data_config = OutputDataConfig(**output_data_config)
        if isinstance(resource_config, dict): resource_config = ResourceConfig(**resource_config)
        if isinstance(stopping_condition, dict): stopping_condition = StoppingCondition(**stopping_condition)
        if isinstance(vpc_config, dict): vpc_config = VpcConfig(**vpc_config)
        self._values = {
            'algorithm_specification': algorithm_specification,
            'input_data_config': input_data_config,
            'output_data_config': output_data_config,
            'training_job_name': training_job_name,
        }
        if hyperparameters is not None: self._values["hyperparameters"] = hyperparameters
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if resource_config is not None: self._values["resource_config"] = resource_config
        if role is not None: self._values["role"] = role
        if stopping_condition is not None: self._values["stopping_condition"] = stopping_condition
        if tags is not None: self._values["tags"] = tags
        if vpc_config is not None: self._values["vpc_config"] = vpc_config

    @builtins.property
    def algorithm_specification(self) -> "AlgorithmSpecification":
        """Identifies the training algorithm to use.

        stability
        :stability: experimental
        """
        return self._values.get('algorithm_specification')

    @builtins.property
    def input_data_config(self) -> typing.List["Channel"]:
        """Describes the various datasets (e.g. train, validation, test) and the Amazon S3 location where stored.

        stability
        :stability: experimental
        """
        return self._values.get('input_data_config')

    @builtins.property
    def output_data_config(self) -> "OutputDataConfig":
        """Identifies the Amazon S3 location where you want Amazon SageMaker to save the results of model training.

        stability
        :stability: experimental
        """
        return self._values.get('output_data_config')

    @builtins.property
    def training_job_name(self) -> str:
        """Training Job Name.

        stability
        :stability: experimental
        """
        return self._values.get('training_job_name')

    @builtins.property
    def hyperparameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Algorithm-specific parameters that influence the quality of the model.

        Set hyperparameters before you start the learning process.
        For a list of hyperparameters provided by Amazon SageMaker

        default
        :default: - No hyperparameters

        see
        :see: https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html
        stability
        :stability: experimental
        """
        return self._values.get('hyperparameters')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call SageMaker APIs.

        The valid value is either FIRE_AND_FORGET or SYNC.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def resource_config(self) -> typing.Optional["ResourceConfig"]:
        """Specifies the resources, ML compute instances, and ML storage volumes to deploy for model training.

        default
        :default: - 1 instance of EC2 ``M4.XLarge`` with ``10GB`` volume

        stability
        :stability: experimental
        """
        return self._values.get('resource_config')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role for the Training Job.

        The role must be granted all necessary permissions for the SageMaker training job to
        be able to operate.

        See https://docs.aws.amazon.com/fr_fr/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-createtrainingjob-perms

        default
        :default: - a role with appropriate permissions will be created.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def stopping_condition(self) -> typing.Optional["StoppingCondition"]:
        """Sets a time limit for training.

        default
        :default: - max runtime of 1 hour

        stability
        :stability: experimental
        """
        return self._values.get('stopping_condition')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Tags to be applied to the train job.

        default
        :default: - No tags

        stability
        :stability: experimental
        """
        return self._values.get('tags')

    @builtins.property
    def vpc_config(self) -> typing.Optional["VpcConfig"]:
        """Specifies the VPC that you want your training job to connect to.

        default
        :default: - No VPC

        stability
        :stability: experimental
        """
        return self._values.get('vpc_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SagemakerTrainTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.SagemakerTransformProps", jsii_struct_bases=[], name_mapping={'model_name': 'modelName', 'transform_input': 'transformInput', 'transform_job_name': 'transformJobName', 'transform_output': 'transformOutput', 'batch_strategy': 'batchStrategy', 'environment': 'environment', 'integration_pattern': 'integrationPattern', 'max_concurrent_transforms': 'maxConcurrentTransforms', 'max_payload_in_mb': 'maxPayloadInMB', 'role': 'role', 'tags': 'tags', 'transform_resources': 'transformResources'})
class SagemakerTransformProps():
    def __init__(self, *, model_name: str, transform_input: "TransformInput", transform_job_name: str, transform_output: "TransformOutput", batch_strategy: typing.Optional["BatchStrategy"]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, max_concurrent_transforms: typing.Optional[jsii.Number]=None, max_payload_in_mb: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, transform_resources: typing.Optional["TransformResources"]=None) -> None:
        """Properties for creating an Amazon SageMaker training job task.

        :param model_name: Name of the model that you want to use for the transform job.
        :param transform_input: Dataset to be transformed and the Amazon S3 location where it is stored.
        :param transform_job_name: Training Job Name.
        :param transform_output: S3 location where you want Amazon SageMaker to save the results from the transform job.
        :param batch_strategy: Number of records to include in a mini-batch for an HTTP inference request. Default: - No batch strategy
        :param environment: Environment variables to set in the Docker container. Default: - No environment variables
        :param integration_pattern: The service integration pattern indicates different ways to call SageMaker APIs. The valid value is either FIRE_AND_FORGET or SYNC. Default: FIRE_AND_FORGET
        :param max_concurrent_transforms: Maximum number of parallel requests that can be sent to each instance in a transform job. Default: - Amazon SageMaker checks the optional execution-parameters to determine the settings for your chosen algorithm. If the execution-parameters endpoint is not enabled, the default value is 1.
        :param max_payload_in_mb: Maximum allowed size of the payload, in MB. Default: 6
        :param role: Role for the Training Job. Default: - A role is created with ``AmazonSageMakerFullAccess`` managed policy
        :param tags: Tags to be applied to the train job. Default: - No tags
        :param transform_resources: ML compute instances for the transform job. Default: - 1 instance of type M4.XLarge

        stability
        :stability: experimental
        """
        if isinstance(transform_input, dict): transform_input = TransformInput(**transform_input)
        if isinstance(transform_output, dict): transform_output = TransformOutput(**transform_output)
        if isinstance(transform_resources, dict): transform_resources = TransformResources(**transform_resources)
        self._values = {
            'model_name': model_name,
            'transform_input': transform_input,
            'transform_job_name': transform_job_name,
            'transform_output': transform_output,
        }
        if batch_strategy is not None: self._values["batch_strategy"] = batch_strategy
        if environment is not None: self._values["environment"] = environment
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if max_concurrent_transforms is not None: self._values["max_concurrent_transforms"] = max_concurrent_transforms
        if max_payload_in_mb is not None: self._values["max_payload_in_mb"] = max_payload_in_mb
        if role is not None: self._values["role"] = role
        if tags is not None: self._values["tags"] = tags
        if transform_resources is not None: self._values["transform_resources"] = transform_resources

    @builtins.property
    def model_name(self) -> str:
        """Name of the model that you want to use for the transform job.

        stability
        :stability: experimental
        """
        return self._values.get('model_name')

    @builtins.property
    def transform_input(self) -> "TransformInput":
        """Dataset to be transformed and the Amazon S3 location where it is stored.

        stability
        :stability: experimental
        """
        return self._values.get('transform_input')

    @builtins.property
    def transform_job_name(self) -> str:
        """Training Job Name.

        stability
        :stability: experimental
        """
        return self._values.get('transform_job_name')

    @builtins.property
    def transform_output(self) -> "TransformOutput":
        """S3 location where you want Amazon SageMaker to save the results from the transform job.

        stability
        :stability: experimental
        """
        return self._values.get('transform_output')

    @builtins.property
    def batch_strategy(self) -> typing.Optional["BatchStrategy"]:
        """Number of records to include in a mini-batch for an HTTP inference request.

        default
        :default: - No batch strategy

        stability
        :stability: experimental
        """
        return self._values.get('batch_strategy')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables to set in the Docker container.

        default
        :default: - No environment variables

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call SageMaker APIs.

        The valid value is either FIRE_AND_FORGET or SYNC.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def max_concurrent_transforms(self) -> typing.Optional[jsii.Number]:
        """Maximum number of parallel requests that can be sent to each instance in a transform job.

        default
        :default:

        - Amazon SageMaker checks the optional execution-parameters to determine the settings for your chosen algorithm.
          If the execution-parameters endpoint is not enabled, the default value is 1.

        stability
        :stability: experimental
        """
        return self._values.get('max_concurrent_transforms')

    @builtins.property
    def max_payload_in_mb(self) -> typing.Optional[jsii.Number]:
        """Maximum allowed size of the payload, in MB.

        default
        :default: 6

        stability
        :stability: experimental
        """
        return self._values.get('max_payload_in_mb')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role for the Training Job.

        default
        :default: - A role is created with ``AmazonSageMakerFullAccess`` managed policy

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Tags to be applied to the train job.

        default
        :default: - No tags

        stability
        :stability: experimental
        """
        return self._values.get('tags')

    @builtins.property
    def transform_resources(self) -> typing.Optional["TransformResources"]:
        """ML compute instances for the transform job.

        default
        :default: - 1 instance of type M4.XLarge

        stability
        :stability: experimental
        """
        return self._values.get('transform_resources')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SagemakerTransformProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class SagemakerTransformTask(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.SagemakerTransformTask"):
    """Class representing the SageMaker Create Training Job task.

    stability
    :stability: experimental
    """
    def __init__(self, *, model_name: str, transform_input: "TransformInput", transform_job_name: str, transform_output: "TransformOutput", batch_strategy: typing.Optional["BatchStrategy"]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, max_concurrent_transforms: typing.Optional[jsii.Number]=None, max_payload_in_mb: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, transform_resources: typing.Optional["TransformResources"]=None) -> None:
        """
        :param model_name: Name of the model that you want to use for the transform job.
        :param transform_input: Dataset to be transformed and the Amazon S3 location where it is stored.
        :param transform_job_name: Training Job Name.
        :param transform_output: S3 location where you want Amazon SageMaker to save the results from the transform job.
        :param batch_strategy: Number of records to include in a mini-batch for an HTTP inference request. Default: - No batch strategy
        :param environment: Environment variables to set in the Docker container. Default: - No environment variables
        :param integration_pattern: The service integration pattern indicates different ways to call SageMaker APIs. The valid value is either FIRE_AND_FORGET or SYNC. Default: FIRE_AND_FORGET
        :param max_concurrent_transforms: Maximum number of parallel requests that can be sent to each instance in a transform job. Default: - Amazon SageMaker checks the optional execution-parameters to determine the settings for your chosen algorithm. If the execution-parameters endpoint is not enabled, the default value is 1.
        :param max_payload_in_mb: Maximum allowed size of the payload, in MB. Default: 6
        :param role: Role for the Training Job. Default: - A role is created with ``AmazonSageMakerFullAccess`` managed policy
        :param tags: Tags to be applied to the train job. Default: - No tags
        :param transform_resources: ML compute instances for the transform job. Default: - 1 instance of type M4.XLarge

        stability
        :stability: experimental
        """
        props = SagemakerTransformProps(model_name=model_name, transform_input=transform_input, transform_job_name=transform_job_name, transform_output=transform_output, batch_strategy=batch_strategy, environment=environment, integration_pattern=integration_pattern, max_concurrent_transforms=max_concurrent_transforms, max_payload_in_mb=max_payload_in_mb, role=role, tags=tags, transform_resources=transform_resources)

        jsii.create(SagemakerTransformTask, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The execution role for the Sagemaker training job.

        Only available after task has been added to a state machine.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class SendToQueue(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.SendToQueue"):
    """A StepFunctions Task to send messages to SQS queue.

    A Function can be used directly as a Resource, but this class mirrors
    integration with other AWS services via a specific class instance.

    deprecated
    :deprecated: Use ``SqsSendMessage``

    stability
    :stability: deprecated
    """
    def __init__(self, queue: aws_cdk.aws_sqs.IQueue, *, message_body: aws_cdk.aws_stepfunctions.TaskInput, delay: typing.Optional[aws_cdk.core.Duration]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, message_deduplication_id: typing.Optional[str]=None, message_group_id: typing.Optional[str]=None) -> None:
        """
        :param queue: -
        :param message_body: The text message to send to the queue.
        :param delay: The length of time, in seconds, for which to delay a specific message. Valid values are 0-900 seconds. Default: Default value of the queue is used
        :param integration_pattern: The service integration pattern indicates different ways to call SendMessage to SQS. The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param message_deduplication_id: The token used for deduplication of sent messages. Default: Use content-based deduplication
        :param message_group_id: The tag that specifies that a message belongs to a specific message group. Required for FIFO queues. FIFO ordering applies to messages in the same message group. Default: No group ID

        stability
        :stability: deprecated
        """
        props = SendToQueueProps(message_body=message_body, delay=delay, integration_pattern=integration_pattern, message_deduplication_id=message_deduplication_id, message_group_id=message_group_id)

        jsii.create(SendToQueue, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param _task: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.SendToQueueProps", jsii_struct_bases=[], name_mapping={'message_body': 'messageBody', 'delay': 'delay', 'integration_pattern': 'integrationPattern', 'message_deduplication_id': 'messageDeduplicationId', 'message_group_id': 'messageGroupId'})
class SendToQueueProps():
    def __init__(self, *, message_body: aws_cdk.aws_stepfunctions.TaskInput, delay: typing.Optional[aws_cdk.core.Duration]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, message_deduplication_id: typing.Optional[str]=None, message_group_id: typing.Optional[str]=None) -> None:
        """Properties for SendMessageTask.

        :param message_body: The text message to send to the queue.
        :param delay: The length of time, in seconds, for which to delay a specific message. Valid values are 0-900 seconds. Default: Default value of the queue is used
        :param integration_pattern: The service integration pattern indicates different ways to call SendMessage to SQS. The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param message_deduplication_id: The token used for deduplication of sent messages. Default: Use content-based deduplication
        :param message_group_id: The tag that specifies that a message belongs to a specific message group. Required for FIFO queues. FIFO ordering applies to messages in the same message group. Default: No group ID

        deprecated
        :deprecated: Use ``SqsSendMessage``

        stability
        :stability: deprecated
        """
        self._values = {
            'message_body': message_body,
        }
        if delay is not None: self._values["delay"] = delay
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if message_deduplication_id is not None: self._values["message_deduplication_id"] = message_deduplication_id
        if message_group_id is not None: self._values["message_group_id"] = message_group_id

    @builtins.property
    def message_body(self) -> aws_cdk.aws_stepfunctions.TaskInput:
        """The text message to send to the queue.

        stability
        :stability: deprecated
        """
        return self._values.get('message_body')

    @builtins.property
    def delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time, in seconds, for which to delay a specific message.

        Valid values are 0-900 seconds.

        default
        :default: Default value of the queue is used

        stability
        :stability: deprecated
        """
        return self._values.get('delay')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call SendMessage to SQS.

        The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN.

        default
        :default: FIRE_AND_FORGET

        stability
        :stability: deprecated
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def message_deduplication_id(self) -> typing.Optional[str]:
        """The token used for deduplication of sent messages.

        default
        :default: Use content-based deduplication

        stability
        :stability: deprecated
        """
        return self._values.get('message_deduplication_id')

    @builtins.property
    def message_group_id(self) -> typing.Optional[str]:
        """The tag that specifies that a message belongs to a specific message group.

        Required for FIFO queues. FIFO ordering applies to messages in the same message
        group.

        default
        :default: No group ID

        stability
        :stability: deprecated
        """
        return self._values.get('message_group_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SendToQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.ShuffleConfig", jsii_struct_bases=[], name_mapping={'seed': 'seed'})
class ShuffleConfig():
    def __init__(self, *, seed: jsii.Number) -> None:
        """Configuration for a shuffle option for input data in a channel.

        :param seed: Determines the shuffling order.

        stability
        :stability: experimental
        """
        self._values = {
            'seed': seed,
        }

    @builtins.property
    def seed(self) -> jsii.Number:
        """Determines the shuffling order.

        stability
        :stability: experimental
        """
        return self._values.get('seed')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ShuffleConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class SnsPublish(aws_cdk.aws_stepfunctions.TaskStateBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.SnsPublish"):
    """A Step Functions Task to publish messages to SNS topic.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, message: aws_cdk.aws_stepfunctions.TaskInput, topic: aws_cdk.aws_sns.ITopic, message_per_subscription_type: typing.Optional[bool]=None, subject: typing.Optional[str]=None, comment: typing.Optional[str]=None, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, input_path: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param message: The message you want to send. With the exception of SMS, messages must be UTF-8 encoded strings and at most 256 KB in size. For SMS, each message can contain up to 140 characters.
        :param topic: The SNS topic that the task will publish to.
        :param message_per_subscription_type: Send different messages for each transport protocol. For example, you might want to send a shorter message to SMS subscribers and a more verbose message to email and SQS subscribers. Your message must be a JSON object with a top-level JSON key of "default" with a value that is a string You can define other top-level keys that define the message you want to send to a specific transport protocol (i.e. "sqs", "email", "http", etc) Default: false
        :param subject: Used as the "Subject" line when the message is delivered to email endpoints. This field will also be included, if present, in the standard JSON messages delivered to other endpoints. Default: - No subject
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        stability
        :stability: experimental
        """
        props = SnsPublishProps(message=message, topic=topic, message_per_subscription_type=message_per_subscription_type, subject=subject, comment=comment, heartbeat=heartbeat, input_path=input_path, integration_pattern=integration_pattern, output_path=output_path, result_path=result_path, timeout=timeout)

        jsii.create(SnsPublish, self, [scope, id, props])

    @jsii.member(jsii_name="renderTask")
    def _render_task(self) -> typing.Any:
        """Provides the SNS Publish service integration task configuration.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderTask", [])

    @builtins.property
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.SnsPublishProps", jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps], name_mapping={'comment': 'comment', 'heartbeat': 'heartbeat', 'input_path': 'inputPath', 'integration_pattern': 'integrationPattern', 'output_path': 'outputPath', 'result_path': 'resultPath', 'timeout': 'timeout', 'message': 'message', 'topic': 'topic', 'message_per_subscription_type': 'messagePerSubscriptionType', 'subject': 'subject'})
class SnsPublishProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(self, *, comment: typing.Optional[str]=None, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, input_path: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, message: aws_cdk.aws_stepfunctions.TaskInput, topic: aws_cdk.aws_sns.ITopic, message_per_subscription_type: typing.Optional[bool]=None, subject: typing.Optional[str]=None) -> None:
        """Properties for publishing a message to an SNS topic.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param message: The message you want to send. With the exception of SMS, messages must be UTF-8 encoded strings and at most 256 KB in size. For SMS, each message can contain up to 140 characters.
        :param topic: The SNS topic that the task will publish to.
        :param message_per_subscription_type: Send different messages for each transport protocol. For example, you might want to send a shorter message to SMS subscribers and a more verbose message to email and SQS subscribers. Your message must be a JSON object with a top-level JSON key of "default" with a value that is a string You can define other top-level keys that define the message you want to send to a specific transport protocol (i.e. "sqs", "email", "http", etc) Default: false
        :param subject: Used as the "Subject" line when the message is delivered to email endpoints. This field will also be included, if present, in the standard JSON messages delivered to other endpoints. Default: - No subject

        stability
        :stability: experimental
        """
        self._values = {
            'message': message,
            'topic': topic,
        }
        if comment is not None: self._values["comment"] = comment
        if heartbeat is not None: self._values["heartbeat"] = heartbeat
        if input_path is not None: self._values["input_path"] = input_path
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if output_path is not None: self._values["output_path"] = output_path
        if result_path is not None: self._values["result_path"] = result_path
        if timeout is not None: self._values["timeout"] = timeout
        if message_per_subscription_type is not None: self._values["message_per_subscription_type"] = message_per_subscription_type
        if subject is not None: self._values["subject"] = subject

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: - No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('heartbeat')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: - The entire task input (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        default
        :default: IntegrationPattern.REQUEST_RESPONSE

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default:

        - The entire JSON node determined by the state input, the task result,
          and resultPath is passed to the next state (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: - Replaces the entire input with the result (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def message(self) -> aws_cdk.aws_stepfunctions.TaskInput:
        """The message you want to send.

        With the exception of SMS, messages must be UTF-8 encoded strings and
        at most 256 KB in size.
        For SMS, each message can contain up to 140 characters.

        stability
        :stability: experimental
        """
        return self._values.get('message')

    @builtins.property
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        """The SNS topic that the task will publish to.

        stability
        :stability: experimental
        """
        return self._values.get('topic')

    @builtins.property
    def message_per_subscription_type(self) -> typing.Optional[bool]:
        """Send different messages for each transport protocol.

        For example, you might want to send a shorter message to SMS subscribers
        and a more verbose message to email and SQS subscribers.

        Your message must be a JSON object with a top-level JSON key of
        "default" with a value that is a string
        You can define other top-level keys that define the message you want to
        send to a specific transport protocol (i.e. "sqs", "email", "http", etc)

        default
        :default: false

        see
        :see: https://docs.aws.amazon.com/sns/latest/api/API_Publish.html#API_Publish_RequestParameters
        stability
        :stability: experimental
        """
        return self._values.get('message_per_subscription_type')

    @builtins.property
    def subject(self) -> typing.Optional[str]:
        """Used as the "Subject" line when the message is delivered to email endpoints.

        This field will also be included, if present, in the standard JSON messages
        delivered to other endpoints.

        default
        :default: - No subject

        stability
        :stability: experimental
        """
        return self._values.get('subject')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SnsPublishProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.SplitType")
class SplitType(enum.Enum):
    """Method to use to split the transform job's data files into smaller batches.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """Input data files are not split,.

    stability
    :stability: experimental
    """
    LINE = "LINE"
    """Split records on a newline character boundary.

    stability
    :stability: experimental
    """
    RECORD_IO = "RECORD_IO"
    """Split using MXNet RecordIO format.

    stability
    :stability: experimental
    """
    TF_RECORD = "TF_RECORD"
    """Split using TensorFlow TFRecord format.

    stability
    :stability: experimental
    """

class SqsSendMessage(aws_cdk.aws_stepfunctions.TaskStateBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.SqsSendMessage"):
    """A StepFunctions Task to send messages to SQS queue.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, message_body: aws_cdk.aws_stepfunctions.TaskInput, queue: aws_cdk.aws_sqs.IQueue, delay: typing.Optional[aws_cdk.core.Duration]=None, message_deduplication_id: typing.Optional[str]=None, message_group_id: typing.Optional[str]=None, comment: typing.Optional[str]=None, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, input_path: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param message_body: The text message to send to the queue.
        :param queue: The SQS queue that messages will be sent to.
        :param delay: The length of time, for which to delay a message. Messages that you send to the queue remain invisible to consumers for the duration of the delay period. The maximum allowed delay is 15 minutes. Default: - delay set on the queue. If a delay is not set on the queue, messages are sent immediately (0 seconds).
        :param message_deduplication_id: The token used for deduplication of sent messages. Any messages sent with the same deduplication ID are accepted successfully, but aren't delivered during the 5-minute deduplication interval. Default: - None
        :param message_group_id: The tag that specifies that a message belongs to a specific message group. Messages that belong to the same message group are processed in a FIFO manner. Messages in different message groups might be processed out of order. Default: - None
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        stability
        :stability: experimental
        """
        props = SqsSendMessageProps(message_body=message_body, queue=queue, delay=delay, message_deduplication_id=message_deduplication_id, message_group_id=message_group_id, comment=comment, heartbeat=heartbeat, input_path=input_path, integration_pattern=integration_pattern, output_path=output_path, result_path=result_path, timeout=timeout)

        jsii.create(SqsSendMessage, self, [scope, id, props])

    @jsii.member(jsii_name="renderTask")
    def _render_task(self) -> typing.Any:
        """Provides the SQS SendMessage service integration task configuration.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderTask", [])

    @builtins.property
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.SqsSendMessageProps", jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps], name_mapping={'comment': 'comment', 'heartbeat': 'heartbeat', 'input_path': 'inputPath', 'integration_pattern': 'integrationPattern', 'output_path': 'outputPath', 'result_path': 'resultPath', 'timeout': 'timeout', 'message_body': 'messageBody', 'queue': 'queue', 'delay': 'delay', 'message_deduplication_id': 'messageDeduplicationId', 'message_group_id': 'messageGroupId'})
class SqsSendMessageProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(self, *, comment: typing.Optional[str]=None, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, input_path: typing.Optional[str]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, message_body: aws_cdk.aws_stepfunctions.TaskInput, queue: aws_cdk.aws_sqs.IQueue, delay: typing.Optional[aws_cdk.core.Duration]=None, message_deduplication_id: typing.Optional[str]=None, message_group_id: typing.Optional[str]=None) -> None:
        """Properties for sending a message to an SQS queue.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param message_body: The text message to send to the queue.
        :param queue: The SQS queue that messages will be sent to.
        :param delay: The length of time, for which to delay a message. Messages that you send to the queue remain invisible to consumers for the duration of the delay period. The maximum allowed delay is 15 minutes. Default: - delay set on the queue. If a delay is not set on the queue, messages are sent immediately (0 seconds).
        :param message_deduplication_id: The token used for deduplication of sent messages. Any messages sent with the same deduplication ID are accepted successfully, but aren't delivered during the 5-minute deduplication interval. Default: - None
        :param message_group_id: The tag that specifies that a message belongs to a specific message group. Messages that belong to the same message group are processed in a FIFO manner. Messages in different message groups might be processed out of order. Default: - None

        stability
        :stability: experimental
        """
        self._values = {
            'message_body': message_body,
            'queue': queue,
        }
        if comment is not None: self._values["comment"] = comment
        if heartbeat is not None: self._values["heartbeat"] = heartbeat
        if input_path is not None: self._values["input_path"] = input_path
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if output_path is not None: self._values["output_path"] = output_path
        if result_path is not None: self._values["result_path"] = result_path
        if timeout is not None: self._values["timeout"] = timeout
        if delay is not None: self._values["delay"] = delay
        if message_deduplication_id is not None: self._values["message_deduplication_id"] = message_deduplication_id
        if message_group_id is not None: self._values["message_group_id"] = message_group_id

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: - No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('heartbeat')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: - The entire task input (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        default
        :default: IntegrationPattern.REQUEST_RESPONSE

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default:

        - The entire JSON node determined by the state input, the task result,
          and resultPath is passed to the next state (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: - Replaces the entire input with the result (JSON path '$')

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def message_body(self) -> aws_cdk.aws_stepfunctions.TaskInput:
        """The text message to send to the queue.

        stability
        :stability: experimental
        """
        return self._values.get('message_body')

    @builtins.property
    def queue(self) -> aws_cdk.aws_sqs.IQueue:
        """The SQS queue that messages will be sent to.

        stability
        :stability: experimental
        """
        return self._values.get('queue')

    @builtins.property
    def delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time, for which to delay a message.

        Messages that you send to the queue remain invisible to consumers for the duration
        of the delay period. The maximum allowed delay is 15 minutes.

        default
        :default:

        - delay set on the queue. If a delay is not set on the queue,
          messages are sent immediately (0 seconds).

        stability
        :stability: experimental
        """
        return self._values.get('delay')

    @builtins.property
    def message_deduplication_id(self) -> typing.Optional[str]:
        """The token used for deduplication of sent messages.

        Any messages sent with the same deduplication ID are accepted successfully,
        but aren't delivered during the 5-minute deduplication interval.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('message_deduplication_id')

    @builtins.property
    def message_group_id(self) -> typing.Optional[str]:
        """The tag that specifies that a message belongs to a specific message group.

        Messages that belong to the same message group are processed in a FIFO manner.
        Messages in different message groups might be processed out of order.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('message_group_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SqsSendMessageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class StartExecution(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions-tasks.StartExecution"):
    """A Step Functions Task to call StartExecution on another state machine.

    It supports three service integration patterns: FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

    stability
    :stability: experimental
    """
    def __init__(self, state_machine: aws_cdk.aws_stepfunctions.IStateMachine, *, input: typing.Optional[typing.Mapping[str, typing.Any]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, name: typing.Optional[str]=None) -> None:
        """
        :param state_machine: -
        :param input: The JSON input for the execution, same as that of StartExecution. Default: - No input
        :param integration_pattern: The service integration pattern indicates different ways to call StartExecution to Step Functions. Default: FIRE_AND_FORGET
        :param name: The name of the execution, same as that of StartExecution. Default: - None

        stability
        :stability: experimental
        """
        props = StartExecutionProps(input=input, integration_pattern=integration_pattern, name=name)

        jsii.create(StartExecution, self, [state_machine, props])

    @jsii.member(jsii_name="bind")
    def bind(self, task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.StartExecutionProps", jsii_struct_bases=[], name_mapping={'input': 'input', 'integration_pattern': 'integrationPattern', 'name': 'name'})
class StartExecutionProps():
    def __init__(self, *, input: typing.Optional[typing.Mapping[str, typing.Any]]=None, integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]=None, name: typing.Optional[str]=None) -> None:
        """Properties for StartExecution.

        :param input: The JSON input for the execution, same as that of StartExecution. Default: - No input
        :param integration_pattern: The service integration pattern indicates different ways to call StartExecution to Step Functions. Default: FIRE_AND_FORGET
        :param name: The name of the execution, same as that of StartExecution. Default: - None

        stability
        :stability: experimental
        """
        self._values = {
        }
        if input is not None: self._values["input"] = input
        if integration_pattern is not None: self._values["integration_pattern"] = integration_pattern
        if name is not None: self._values["name"] = name

    @builtins.property
    def input(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The JSON input for the execution, same as that of StartExecution.

        default
        :default: - No input

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        stability
        :stability: experimental
        """
        return self._values.get('input')

    @builtins.property
    def integration_pattern(self) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call StartExecution to Step Functions.

        default
        :default: FIRE_AND_FORGET

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html
        stability
        :stability: experimental
        """
        return self._values.get('integration_pattern')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """The name of the execution, same as that of StartExecution.

        default
        :default: - None

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        stability
        :stability: experimental
        """
        return self._values.get('name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StartExecutionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.StoppingCondition", jsii_struct_bases=[], name_mapping={'max_runtime': 'maxRuntime'})
class StoppingCondition():
    def __init__(self, *, max_runtime: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Specifies a limit to how long a model training job can run.

        When the job reaches the time limit, Amazon SageMaker ends the training job.

        :param max_runtime: The maximum length of time, in seconds, that the training or compilation job can run. Default: - 1 hour

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max_runtime is not None: self._values["max_runtime"] = max_runtime

    @builtins.property
    def max_runtime(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum length of time, in seconds, that the training or compilation job can run.

        default
        :default: - 1 hour

        stability
        :stability: experimental
        """
        return self._values.get('max_runtime')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StoppingCondition(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.TaskEnvironmentVariable", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
class TaskEnvironmentVariable():
    def __init__(self, *, name: str, value: str) -> None:
        """An environment variable to be set in the container run as a task.

        :param name: Name for the environment variable. Exactly one of ``name`` and ``namePath`` must be specified.
        :param value: Value of the environment variable. Exactly one of ``value`` and ``valuePath`` must be specified.

        stability
        :stability: experimental
        """
        self._values = {
            'name': name,
            'value': value,
        }

    @builtins.property
    def name(self) -> str:
        """Name for the environment variable.

        Exactly one of ``name`` and ``namePath`` must be specified.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def value(self) -> str:
        """Value of the environment variable.

        Exactly one of ``value`` and ``valuePath`` must be specified.

        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TaskEnvironmentVariable(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformDataSource", jsii_struct_bases=[], name_mapping={'s3_data_source': 's3DataSource'})
class TransformDataSource():
    def __init__(self, *, s3_data_source: "TransformS3DataSource") -> None:
        """S3 location of the input data that the model can consume.

        :param s3_data_source: S3 location of the input data.

        stability
        :stability: experimental
        """
        if isinstance(s3_data_source, dict): s3_data_source = TransformS3DataSource(**s3_data_source)
        self._values = {
            's3_data_source': s3_data_source,
        }

    @builtins.property
    def s3_data_source(self) -> "TransformS3DataSource":
        """S3 location of the input data.

        stability
        :stability: experimental
        """
        return self._values.get('s3_data_source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TransformDataSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformInput", jsii_struct_bases=[], name_mapping={'transform_data_source': 'transformDataSource', 'compression_type': 'compressionType', 'content_type': 'contentType', 'split_type': 'splitType'})
class TransformInput():
    def __init__(self, *, transform_data_source: "TransformDataSource", compression_type: typing.Optional["CompressionType"]=None, content_type: typing.Optional[str]=None, split_type: typing.Optional["SplitType"]=None) -> None:
        """Dataset to be transformed and the Amazon S3 location where it is stored.

        :param transform_data_source: S3 location of the channel data.
        :param compression_type: The compression type of the transform data. Default: NONE
        :param content_type: Multipurpose internet mail extension (MIME) type of the data. Default: - None
        :param split_type: Method to use to split the transform job's data files into smaller batches. Default: NONE

        stability
        :stability: experimental
        """
        if isinstance(transform_data_source, dict): transform_data_source = TransformDataSource(**transform_data_source)
        self._values = {
            'transform_data_source': transform_data_source,
        }
        if compression_type is not None: self._values["compression_type"] = compression_type
        if content_type is not None: self._values["content_type"] = content_type
        if split_type is not None: self._values["split_type"] = split_type

    @builtins.property
    def transform_data_source(self) -> "TransformDataSource":
        """S3 location of the channel data.

        stability
        :stability: experimental
        """
        return self._values.get('transform_data_source')

    @builtins.property
    def compression_type(self) -> typing.Optional["CompressionType"]:
        """The compression type of the transform data.

        default
        :default: NONE

        stability
        :stability: experimental
        """
        return self._values.get('compression_type')

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        """Multipurpose internet mail extension (MIME) type of the data.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('content_type')

    @builtins.property
    def split_type(self) -> typing.Optional["SplitType"]:
        """Method to use to split the transform job's data files into smaller batches.

        default
        :default: NONE

        stability
        :stability: experimental
        """
        return self._values.get('split_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TransformInput(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformOutput", jsii_struct_bases=[], name_mapping={'s3_output_path': 's3OutputPath', 'accept': 'accept', 'assemble_with': 'assembleWith', 'encryption_key': 'encryptionKey'})
class TransformOutput():
    def __init__(self, *, s3_output_path: str, accept: typing.Optional[str]=None, assemble_with: typing.Optional["AssembleWith"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> None:
        """S3 location where you want Amazon SageMaker to save the results from the transform job.

        :param s3_output_path: S3 path where you want Amazon SageMaker to store the results of the transform job.
        :param accept: MIME type used to specify the output data. Default: - None
        :param assemble_with: Defines how to assemble the results of the transform job as a single S3 object. Default: - None
        :param encryption_key: AWS KMS key that Amazon SageMaker uses to encrypt the model artifacts at rest using Amazon S3 server-side encryption. Default: - default KMS key for Amazon S3 for your role's account.

        stability
        :stability: experimental
        """
        self._values = {
            's3_output_path': s3_output_path,
        }
        if accept is not None: self._values["accept"] = accept
        if assemble_with is not None: self._values["assemble_with"] = assemble_with
        if encryption_key is not None: self._values["encryption_key"] = encryption_key

    @builtins.property
    def s3_output_path(self) -> str:
        """S3 path where you want Amazon SageMaker to store the results of the transform job.

        stability
        :stability: experimental
        """
        return self._values.get('s3_output_path')

    @builtins.property
    def accept(self) -> typing.Optional[str]:
        """MIME type used to specify the output data.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('accept')

    @builtins.property
    def assemble_with(self) -> typing.Optional["AssembleWith"]:
        """Defines how to assemble the results of the transform job as a single S3 object.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('assemble_with')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """AWS KMS key that Amazon SageMaker uses to encrypt the model artifacts at rest using Amazon S3 server-side encryption.

        default
        :default: - default KMS key for Amazon S3 for your role's account.

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TransformOutput(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformResources", jsii_struct_bases=[], name_mapping={'instance_count': 'instanceCount', 'instance_type': 'instanceType', 'volume_kms_key_id': 'volumeKmsKeyId'})
class TransformResources():
    def __init__(self, *, instance_count: jsii.Number, instance_type: aws_cdk.aws_ec2.InstanceType, volume_kms_key_id: typing.Optional[aws_cdk.aws_kms.Key]=None) -> None:
        """ML compute instances for the transform job.

        :param instance_count: Number of ML compute instances to use in the transform job.
        :param instance_type: ML compute instance type for the transform job.
        :param volume_kms_key_id: AWS KMS key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance(s). Default: - None

        stability
        :stability: experimental
        """
        self._values = {
            'instance_count': instance_count,
            'instance_type': instance_type,
        }
        if volume_kms_key_id is not None: self._values["volume_kms_key_id"] = volume_kms_key_id

    @builtins.property
    def instance_count(self) -> jsii.Number:
        """Number of ML compute instances to use in the transform job.

        stability
        :stability: experimental
        """
        return self._values.get('instance_count')

    @builtins.property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        """ML compute instance type for the transform job.

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def volume_kms_key_id(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        """AWS KMS key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance(s).

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('volume_kms_key_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TransformResources(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformS3DataSource", jsii_struct_bases=[], name_mapping={'s3_uri': 's3Uri', 's3_data_type': 's3DataType'})
class TransformS3DataSource():
    def __init__(self, *, s3_uri: str, s3_data_type: typing.Optional["S3DataType"]=None) -> None:
        """Location of the channel data.

        :param s3_uri: Identifies either a key name prefix or a manifest.
        :param s3_data_type: S3 Data Type. Default: 'S3Prefix'

        stability
        :stability: experimental
        """
        self._values = {
            's3_uri': s3_uri,
        }
        if s3_data_type is not None: self._values["s3_data_type"] = s3_data_type

    @builtins.property
    def s3_uri(self) -> str:
        """Identifies either a key name prefix or a manifest.

        stability
        :stability: experimental
        """
        return self._values.get('s3_uri')

    @builtins.property
    def s3_data_type(self) -> typing.Optional["S3DataType"]:
        """S3 Data Type.

        default
        :default: 'S3Prefix'

        stability
        :stability: experimental
        """
        return self._values.get('s3_data_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TransformS3DataSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions-tasks.VpcConfig", jsii_struct_bases=[], name_mapping={'vpc': 'vpc', 'subnets': 'subnets'})
class VpcConfig():
    def __init__(self, *, vpc: aws_cdk.aws_ec2.IVpc, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """Specifies the VPC that you want your Amazon SageMaker training job to connect to.

        :param vpc: VPC.
        :param subnets: VPC subnets. Default: - Private Subnets are selected

        stability
        :stability: experimental
        """
        if isinstance(subnets, dict): subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values = {
            'vpc': vpc,
        }
        if subnets is not None: self._values["subnets"] = subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC subnets.

        default
        :default: - Private Subnets are selected

        stability
        :stability: experimental
        """
        return self._values.get('subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VpcConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "ActionOnFailure",
    "AlgorithmSpecification",
    "AssembleWith",
    "BatchStrategy",
    "CallDynamoDB",
    "Channel",
    "CommonEcsRunTaskProps",
    "CompressionType",
    "ContainerOverride",
    "ContainerOverrides",
    "DataSource",
    "DockerImage",
    "DockerImageConfig",
    "DynamoAttribute",
    "DynamoAttributeValue",
    "DynamoAttributeValueMap",
    "DynamoConsumedCapacity",
    "DynamoDeleteItem",
    "DynamoDeleteItemProps",
    "DynamoGetItem",
    "DynamoGetItemProps",
    "DynamoItemCollectionMetrics",
    "DynamoProjectionExpression",
    "DynamoPutItem",
    "DynamoPutItemProps",
    "DynamoReturnValues",
    "DynamoUpdateItem",
    "DynamoUpdateItemProps",
    "EcsRunTaskBase",
    "EcsRunTaskBaseProps",
    "EmrAddStep",
    "EmrAddStepProps",
    "EmrCancelStep",
    "EmrCancelStepProps",
    "EmrCreateCluster",
    "EmrCreateClusterProps",
    "EmrModifyInstanceFleetByName",
    "EmrModifyInstanceFleetByNameProps",
    "EmrModifyInstanceGroupByName",
    "EmrModifyInstanceGroupByNameProps",
    "EmrSetClusterTerminationProtection",
    "EmrSetClusterTerminationProtectionProps",
    "EmrTerminateCluster",
    "EmrTerminateClusterProps",
    "EvaluateExpression",
    "EvaluateExpressionProps",
    "GlueStartJobRun",
    "GlueStartJobRunProps",
    "ISageMakerTask",
    "InputMode",
    "InvocationType",
    "InvokeActivity",
    "InvokeActivityProps",
    "InvokeFunction",
    "InvokeFunctionProps",
    "JobDependency",
    "LambdaInvocationType",
    "LambdaInvoke",
    "LambdaInvokeProps",
    "MetricDefinition",
    "OutputDataConfig",
    "PublishToTopic",
    "PublishToTopicProps",
    "RecordWrapperType",
    "ResourceConfig",
    "RunBatchJob",
    "RunBatchJobProps",
    "RunEcsEc2Task",
    "RunEcsEc2TaskProps",
    "RunEcsFargateTask",
    "RunEcsFargateTaskProps",
    "RunGlueJobTask",
    "RunGlueJobTaskProps",
    "RunLambdaTask",
    "RunLambdaTaskProps",
    "S3DataDistributionType",
    "S3DataSource",
    "S3DataType",
    "S3Location",
    "S3LocationBindOptions",
    "S3LocationConfig",
    "SagemakerTrainTask",
    "SagemakerTrainTaskProps",
    "SagemakerTransformProps",
    "SagemakerTransformTask",
    "SendToQueue",
    "SendToQueueProps",
    "ShuffleConfig",
    "SnsPublish",
    "SnsPublishProps",
    "SplitType",
    "SqsSendMessage",
    "SqsSendMessageProps",
    "StartExecution",
    "StartExecutionProps",
    "StoppingCondition",
    "TaskEnvironmentVariable",
    "TransformDataSource",
    "TransformInput",
    "TransformOutput",
    "TransformResources",
    "TransformS3DataSource",
    "VpcConfig",
]

publication.publish()
