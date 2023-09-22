import dotenv
import os
import boto3
from datetime import datetime
import re

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

cw = boto3.client(
    "logs",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_KEY"],
    region_name=os.environ["REGION_NAME"],
)


def load_log(level: str, amount: int):
    amount = int(amount)
    present = datetime.now()
    today_string = \
        (f"{present.year}년 "
         f"{present.month}월 "
         f"{present.day}일 "
         f"0시 "
         f"0분 "
         f"0초 ")
    datetime_format = "%Y년 %m월 %d일 %H시 %M분 %S초 "

    today = datetime.strptime(today_string, datetime_format)

    res = cw.get_log_events(
        logGroupName='sms-logs',
        logStreamName='backend-start-logs',
        startTime=int(today.timestamp()*1000),
        endTime=int(present.timestamp()*1000),
    )

    is_not_query = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}")

    log_message = [r['message'] for r in res['events'] if is_not_query.match(r['message'][:23])]
    response_metadata = res['ResponseMetadata']

    if level == 'INFO':
        log_message = [m for m in log_message if m[25:].startswith(level)]
    elif level == 'WARN':
        log_message = [m for m in log_message if m[25:].startswith(level)]
    elif level == 'ERROR':
        log_message = [m for m in log_message if m[24].startswith(level)]
    else:
        print(f"{level} should be one of [INFO, WARN, ERROR]. return all data")

    return log_message[-amount:], response_metadata


