# RDS Database Backup to S3 using Lambda

Takes individual database backups in an RDS instance and pushes them to S3 periodically. Deployed as an AWS Lambda function and triggered by CronExpression.

🔐 User credentials are read from the SecretsManager service

***Structure***
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

👉 Note that the repository is created in the private registry

3. Tag the docker image & push to ECR

```bash
docker tag lambda-postgres-s3-backup:latest 030740437667.dkr.ecr.ap-south-1.amazonaws.com/lambda-postgres-s3-backup:latest
```

4. Push to ECR

```bash
docker push 030740437667.dkr.ecr.ap-south-1.amazonaws.com/lambda-postgres-s3-backup:latest

The push refers to repository [030740437667.dkr.ecr.ap-south-1.amazonaws.com/lambda-postgres-s3-backup]
5f70bf18a086: Pushed
59890a829311: Pushed
4a562de0b5fa: Pushed
7dc5b21da742: Pushed
03b08d9ca7a9: Pushed
2adae8f0ea6d: Pushed
b6f97f0ca2a4: Pushed
9a5bfac8360a: Pushed
95e2ab903c53: Pushed
77ae8a3dc18a: Pushed
8b02b802651d: Pushed
b4fc9d6647b5: Pushed
latest: digest: sha256:4ccb423b0b0af9ba320bd90dbb6a25cb03a47f6a8e140aa140b28ec3c18e09c7 size: 2837
```

5. Deploy the application

```bash
sam deploy --guided

Configuring SAM deploy
======================

	Looking for config file [samconfig.toml] :  Not found

	Setting default arguments for 'sam deploy'
	=========================================
	Stack Name [sam-app]: lambda-postgres-s3-backup
	AWS Region [ap-south-1]:
	Parameter CronExpression [cron(*/5 * * * *)]: cron(0 */12 * * *)
	#Shows you resources changes to be deployed and require a 'Y' to initiate deploy
	Confirm changes before deploy [y/N]: y
	#SAM needs permission to be able to create roles to connect to the resources in your template
	Allow SAM CLI IAM role creation [Y/n]: Y
	#Preserves the state of previously provisioned resources when an operation fails
	Disable rollback [y/N]: N
	Save arguments to configuration file [Y/n]: Y
	SAM configuration file [samconfig.toml]:
	SAM configuration environment [default]:

	Looking for resources needed for deployment:
	Creating the required resources...
	Successfully created!
	 Managed S3 bucket: aws-sam-cli-managed-default-samclisourcebucket-bty01fkaij5q
	 A different default S3 bucket can be set in samconfig.toml
	 Image repositories: Not found.
	 #Managed repositories will be deleted when their functions are removed from the template and deployed
	 Create managed ECR repositories for all functions? [Y/n]: Y

	Saved arguments to config file
	Running 'sam deploy' for future deployments will use the parameters saved above.
	The above parameters can be changed by modifying samconfig.toml
	Learn more about samconfig.toml syntax at
	https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html

The push refers to repository [030740437667.dkr.ecr.ap-south-1.amazonaws.com/lambdapostgress3b74500620a6f5: Pushed
ac21a090c2f4: Pushed
f8befe1521b8: Pushed
189e331f9ac7: Pushed
084e8ec2cf49: Pushed
1cc2d5adf6fe: Pushed
120051af13b1: Pushed
6f6e69c2c592: Pushed
53b8bfee7a0a: Pushed
5b3f1ed98915: Pushed
6b183c62e3d7: Pushed
882fd36bfd35: Pushed
d1dec9917839: Pushed
d38adf39e1dd: Pushed
4ed121b04368: Pushed
d9d07d703dd5: Pushed
lambda-58eddc9f6935-latest: digest: sha256:02f319d2edea31d3d7664288b85a161d89a46580b34839eafcaf8a553ab030f0 size: 3692

	Deploying with following values
	===============================
	Stack name                   : lambda-postgres-s3-backup
	Region                       : ap-south-1
	Confirm changeset            : True
	Disable rollback             : False
	Deployment image repository  :
                                       {
                                           "Lambda": "030740437667.dkr.ecr.ap-south-1.amazonaws.com/lambdapostgress3backup1121c8a9/lambda04a7da3crepo"
                                       }
	Deployment s3 bucket         : aws-sam-cli-managed-default-samclisourcebucket-bty01fkaij5q
	Capabilities                 : ["CAPABILITY_IAM"]
	Parameter overrides          : {"CronExpression": "cron(0 */12 * * *)"}
	Signing Profiles             : {}

Initiating deployment
=====================
Uploading to lambda-postgres-s3-backup/e4d3a87adf28683ee097805d3a6ed268.template  3300 / 3300  (100.00%)

Waiting for changeset to be created..
CloudFormation stack changeset
-------------------------------------------------------------------------------------------------
Operation                LogicalResourceId        ResourceType             Replacement
-------------------------------------------------------------------------------------------------
+ Add                    Cron                     AWS::Events::Rule        N/A
+ Add                    LambdaExecutionRole      AWS::IAM::Role           N/A
+ Add                    Lambda                   AWS::Lambda::Function    N/A
+ Add                    S3BUCKET                 AWS::S3::Bucket          N/A
-------------------------------------------------------------------------------------------------

Changeset created successfully. arn:aws:cloudformation:ap-south-1:030740437667:changeSet/samcli-deploy1667480966/4dd17792-f673-43ac-86d3-936ba4ae7401


Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y

2022-11-03 18:39:36 - Waiting for stack create/update to complete

CloudFormation events from stack operations (refresh every 0.5 seconds)
-------------------------------------------------------------------------------------------------
ResourceStatus           ResourceType             LogicalResourceId        ResourceStatusReason
-------------------------------------------------------------------------------------------------
CREATE_IN_PROGRESS       AWS::CloudFormation::S   lambda-                  User Initiated
                         tack                     postgres-s3-backup
CREATE_IN_PROGRESS       AWS::S3::Bucket          S3BUCKET                 -
CREATE_IN_PROGRESS       AWS::S3::Bucket          S3BUCKET                 Resource creation
                                                                           Initiated
CREATE_COMPLETE          AWS::S3::Bucket          S3BUCKET                 -
CREATE_IN_PROGRESS       AWS::IAM::Role           LambdaExecutionRole      -
CREATE_IN_PROGRESS       AWS::IAM::Role           LambdaExecutionRole      Resource creation
                                                                           Initiated
CREATE_COMPLETE          AWS::IAM::Role           LambdaExecutionRole      -
CREATE_IN_PROGRESS       AWS::Lambda::Function    Lambda                   -
CREATE_FAILED            AWS::Lambda::Function    Lambda                   Resource handler
                                                                           returned message:
                                                                           "null (Service:
                                                                           Lambda, Status Code:
                                                                           403, Request ID: 19cbe
                                                                           b73-0c81-4615-98d7-804
                                                                           789fe3032)"
                                                                           (RequestToken: 1e3cb4a
                                                                           b-82b9-b8cb-b701-4ab23
                                                                           4ba85a2,
                                                                           HandlerErrorCode: Gene
                                                                           ralServiceException)
ROLLBACK_IN_PROGRESS     AWS::CloudFormation::S   lambda-                  The following
                         tack                     postgres-s3-backup       resource(s) failed to
                                                                           create: [Lambda].
                                                                           Rollback requested by
                                                                           user.
DELETE_COMPLETE          AWS::Lambda::Function    Lambda                   -
DELETE_IN_PROGRESS       AWS::IAM::Role           LambdaExecutionRole      -
DELETE_COMPLETE          AWS::IAM::Role           LambdaExecutionRole      -
DELETE_IN_PROGRESS       AWS::S3::Bucket          S3BUCKET                 -
DELETE_COMPLETE          AWS::S3::Bucket          S3BUCKET                 -
ROLLBACK_COMPLETE        AWS::CloudFormation::S   lambda-                  -
                         tack                     postgres-s3-backup
-------------------------------------------------------------------------------------------------
Error: Failed to create/update the stack: lambda-postgres-s3-backup, Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "ROLLBACK_COMPLETE" at least once
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name lambda-postgres-s3-backup
```
