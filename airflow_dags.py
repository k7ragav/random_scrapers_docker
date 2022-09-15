from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from pendulum import timezone

default_args = {
    "owner": "random_scrapers_docker",
    "depends_on_past": False,
    "email": ["k7ragav@gmail.com"],
    "email_on_failure": True,
    "email_on_success": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=15),
    "catchup": True,
}
intervals = {
    "daily_at_8am": "0 8 */1 * *",
    "every_3_days": "0 0 */3 * *",
    "weekly_monday_6pm": "0 18 * * 1",
    "every_hour": "0 * * * *",
}

bash_command = "docker exec random_scrapers_docker python {{ task.task_id }}.py "
bash_command_with_date = "docker exec random_scrapers_docker python {{ task.task_id }}.py {{ds}}"

with DAG(
        "women_volleyball",
        description="women_volleyball tickets",
        default_args=default_args,
        schedule_interval=intervals["every_hour"],
        start_date=datetime(2022, 9, 14, tzinfo=timezone("Europe/Amsterdam")),
) as women_volleyball_dag:
    women_volleyball_task = BashOperator(
        task_id="women_volleyball",
        bash_command=bash_command,
    )
