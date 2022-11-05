# RDS Database Backup to S3 using Lambda

Takes individual database backups in an RDS instance and pushes them to S3 periodically. Deployed as an AWS Lambda function and triggered by CronExpression.

🔐 User credentials are read from the SecretsManager service

**_Structure_**

- `database-backup` - Code for the application's Lambda function and project Dockerfile
- `template.yaml` - A template that defines the application's AWS resources.
- `env.json` - JSON representation of the environment
- `events.json` - Sample event to trigger lambda execution

## Use the SAM CLI to build and test locally

1️⃣ Build your application with the `sam build` command.

```bash
sam build
```

2️⃣ Run functions locally and invoke them with the `sam local invoke` command.

```bash
sam local invoke --event event.json --env-vars env.json
```

### PreRequisites

1. While running locally make sure that the user has all the required access. I had created a user and provided the following permissions -

- AmazonEC2ContainerRegistryFullAccess
- SecretsManagerReadWrite
- AmazonS3FullAccess
- AmazonElasticContainerRegistryPublicFullAccess

2. For testing purposes, I had created a S3 bucket upfront.

## Steps

Check the prerequisites section above if something is wrong

1. Log in to ECR

```bash
aws ecr get-login-password  --region ap-south-1 | docker login --username AWS --password-stdin 030740437667.dkr.ecr.ap-south-1.amazonaws.com
```

2. Create a new repository in ECR for storing the Lambda function container.

```bash
aws ecr create-repository --repository-name lambda-postgres-s3-backup --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true
```

👉 Copy the URL of the repository. Note that the repository is created in the private registry

3. Deploy the application

```bash
sam deploy --guided

Configuring SAM deploy
======================

	Looking for config file [samconfig.toml] :  Not found

	Setting default arguments for 'sam deploy'
	=========================================
	Stack Name [sam-app]: lambda-postgres-s3-backup
	AWS Region [ap-south-1]:
	Parameter CronExpression [cron(* */12 * * *)]: cron(0 */12 * * *)
	# Shows you resources changes to be deployed and require a 'Y' to initiate deploy
	Confirm changes before deploy [y/N]: N
	# SAM needs permission to be able to create roles to connect to the resources in your template
	Allow SAM CLI IAM role creation [Y/n]: Y
	# Preserves the state of previously provisioned resources when an operation fails
	Disable rollback [y/N]: N
	Save arguments to configuration file [Y/n]:
	SAM configuration file [samconfig.toml]:
	SAM configuration environment [default]:

	Looking for resources needed for deployment:
	 Managed S3 bucket: aws-sam-cli-managed-default-samclisourcebucket-1kae4nsvz8jia
	 A different default S3 bucket can be set in samconfig.toml
	 Image repositories: Not found.
	 # Managed repositories will be deleted when their functions are removed from the template and deployed
	 Create managed ECR repositories for all functions? [Y/n]: n
	 # Paste repository URL from previous  step
	 ECR repository for Lambda: 030740437667.dkr.ecr.ap-south-1.amazonaws.com/lambda-postgres-s3-backup

	Saved arguments to config file
	Running 'sam deploy' for future deployments will use the parameters saved above.
	The above parameters can be changed by modifying samconfig.toml
	Learn more about samconfig.toml syntax at
	https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html

a4d42427e486: Layer already exists
447541f7a407: Layer already exists
7b7ef25fd692: Layer already exists
cda56f7129b1: Layer already exists
d30c2b57d770: Layer already exists
2caf5b5c925e: Layer already exists
ea184d2d0020: Layer already exists
6f6e69c2c592: Layer already exists
53b8bfee7a0a: Layer already exists
5b3f1ed98915: Layer already exists
6b183c62e3d7: Layer already exists
882fd36bfd35: Layer already exists
d1dec9917839: Layer already exists
d38adf39e1dd: Layer already exists
4ed121b04368: Layer already exists
d9d07d703dd5: Layer already exists
lambda-db68adbf31fa-latest: digest: sha256:6d9b4ce4c6ebb9815d360080d8795e9a9cc52125e090a4b9e6d54ece8cedd846 size: 3692

	Deploying with following values
	===============================
	Stack name                   : lambda-postgres-s3-backup
	Region                       : ap-south-1
	Confirm changeset            : False
	Disable rollback             : False
	Deployment image repository  :
                                       {
                                           "Lambda": "030740437667.dkr.ecr.ap-south-1.amazonaws.com/lambda-postgres-s3-backup"
                                       }
	Deployment s3 bucket         : aws-sam-cli-managed-default-samclisourcebucket-1kae4nsvz8jia
	Capabilities                 : ["CAPABILITY_IAM"]
	Parameter overrides          : {"CronExpression": "cron(0 */12 * * *)"}
	Signing Profiles             : {}

Initiating deployment
=====================
Uploading to lambda-postgres-s3-backup/ae374b85b98376806ac8cda2dcb11a81.template  3159 / 3159  (100.00%)

Waiting for changeset to be created..
CloudFormation stack changeset
---------------------------------------------------------------------------------------------------------------------
Operation                     LogicalResourceId             ResourceType                  Replacement
---------------------------------------------------------------------------------------------------------------------
+ Add                         Cron                          AWS::Events::Rule             N/A
+ Add                         LambdaExecutionRole           AWS::IAM::Role                N/A
+ Add                         Lambda                        AWS::Lambda::Function         N/A
+ Add                         S3BUCKET                      AWS::S3::Bucket               N/A
---------------------------------------------------------------------------------------------------------------------

Changeset created successfully. arn:aws:cloudformation:ap-south-1:030740437667:changeSet/samcli-deploy1667641739/d42692e1-4a11-4536-9966-831bf3321b6e


2022-11-05 15:19:05 - Waiting for stack create/update to complete

CloudFormation events from stack operations (refresh every 0.5 seconds)
---------------------------------------------------------------------------------------------------------------------
ResourceStatus                ResourceType                  LogicalResourceId             ResourceStatusReason
---------------------------------------------------------------------------------------------------------------------
CREATE_IN_PROGRESS            AWS::CloudFormation::Stack    lambda-postgres-s3-backup     User Initiated
CREATE_IN_PROGRESS            AWS::S3::Bucket               S3BUCKET                      -
CREATE_IN_PROGRESS            AWS::S3::Bucket               S3BUCKET                      Resource creation Initiated
CREATE_COMPLETE               AWS::S3::Bucket               S3BUCKET                      -
CREATE_IN_PROGRESS            AWS::IAM::Role                LambdaExecutionRole           -
CREATE_IN_PROGRESS            AWS::IAM::Role                LambdaExecutionRole           Resource creation Initiated
CREATE_COMPLETE               AWS::IAM::Role                LambdaExecutionRole           -
CREATE_IN_PROGRESS            AWS::Lambda::Function         Lambda                        -
CREATE_FAILED                 AWS::Lambda::Function         Lambda                        Resource handler returned
                                                                                          message: "null (Service:
                                                                                          Lambda, Status Code: 403,
                                                                                          Request ID: 265ebc42-f3c2-4
                                                                                          422-847e-63f4a9f7c6e1)"
                                                                                          (RequestToken: 6a933d15-b1a
                                                                                          6-e45c-a19c-847e0f98e446,
                                                                                          HandlerErrorCode:
                                                                                          GeneralServiceException)
ROLLBACK_IN_PROGRESS          AWS::CloudFormation::Stack    lambda-postgres-s3-backup     The following resource(s)
                                                                                          failed to create: [Lambda].
                                                                                          Rollback requested by user.
DELETE_COMPLETE               AWS::Lambda::Function         Lambda                        -
DELETE_IN_PROGRESS            AWS::IAM::Role                LambdaExecutionRole           -
DELETE_COMPLETE               AWS::IAM::Role                LambdaExecutionRole           -
DELETE_IN_PROGRESS            AWS::S3::Bucket               S3BUCKET                      -
DELETE_COMPLETE               AWS::S3::Bucket               S3BUCKET                      -
ROLLBACK_COMPLETE             AWS::CloudFormation::Stack    lambda-postgres-s3-backup     -
---------------------------------------------------------------------------------------------------------------------
Error: Failed to create/update the stack: lambda-postgres-s3-backup, Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "ROLLBACK_COMPLETE" at least once
```

## Cleanup

Delete the stack

```bash
sam delete --stack-name lambda-postgres-s3-backup
```
