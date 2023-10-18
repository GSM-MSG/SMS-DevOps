import datetime as dt

from pendulum import timezone

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    'crawl_test',
    description='test desc',
    start_date=dt.datetime(2023,10,13, tzinfo=timezone("Asia/Seoul")),
    catchup=False,
    schedule_interval='0 9 * * *',
    tags=['cron', 'crawl']
) as dag:

    start = BashOperator(
        task_id="start",
        bash_command='pwd'
    )

    t1 = BashOperator(
        task_id="crawling",
        bash_command="python /Users/humanlearning/SMS/SMS-DevOps/automation/discord-bot/fee-bot/webhook-fitcloud-crawl-data.py"
    )

    end = BashOperator(
        task_id="end",
        bash_command='echo "end"'
    )

    start >> t1 >> end
