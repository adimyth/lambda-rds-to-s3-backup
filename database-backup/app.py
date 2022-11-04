import json
import os
import subprocess
import pathlib
from datetime import datetime

import boto3
import pytz
from botocore.exceptions import ClientError


def get_secrets():
    secret_name = "sharpsell-nonprod-secrets"
    region_name = "ap-south-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response["SecretString"])
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key
    host = secret["host"]
    port = secret["port"]
    username = secret["username"]
    password = secret["password"]
    return host, port, username, password


def handler(event, context):
    S3_BUCKET = os.getenv("S3_BUCKET", "backup-rds-single-database")
    timezone = pytz.timezone("Asia/Kolkata")

    host, port, username, password = get_secrets()

    for db_name in event["DATABASES"]:
        start = datetime.now(timezone)
        start_formatted = start.strftime("%Y-%m-%d-%H-%M-%S")
        print("==================================")
        print(f"Exporting {db_name} at {start}")
        print("==================================")

        year = start.strftime("%Y")
        month = start.strftime("%m")
        day = start.strftime("%d")

        backup_dir = f"backup/{year}/{month}/{day}/{db_name}/"
        backup_full_path = f"{backup_dir}/{db_name}-{start_formatted}.sql.gz"
        s3_url = f"s3://{S3_BUCKET}/{year}/{month}/{day}/{db_name}/"

        pathlib.Path(backup_dir).mkdir(parents=True, exist_ok=True)

        command = (
            "export PGPASSWORD=%s; pg_dump -Ft -h %s -U %s -p %s -d %s --no-owner --no-acl | gzip -c >%s  && aws s3 cp %s %s"
            % (
                password,
                host,
                username,
                port,
                db_name,
                backup_full_path,
                backup_full_path,
                s3_url,
            )
        )

        subprocess.Popen(command, shell=True).wait()

        end = datetime.now(timezone)
        print("Time taken: %s\n\n" % (end - start))


if __name__ == "__main__":
    event = {
        "DATABASES": [
            "sharpsell-dev-postgresql-sharpsell",
            "sharpsell-uat-postgresql-sharpsell",
        ]
    }
    handler(event, None)
