from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow')

# --- Callbacks ---
def on_failure_alert(context):
    print(f"❌ TASK FAILED: {context['task_instance'].task_id}")
    print(f"   DAG: {context['task_instance'].dag_id}")
    print(f"   Execution time: {context['execution_date']}")
    print(f"   Log URL: {context['task_instance'].log_url}")
    # Phase 6: replace print with Slack/email alert

# --- Default args — this is where self-healing lives ---
default_args = {
    'owner': 'yourname',
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'on_failure_callback': on_failure_alert,
    'email_on_failure': False,
}

# --- Task functions ---
def ingest_task(**kwargs):
    from ingestion.ingest_nyc_taxi import ingest
    # Using Olist later — for now test with taxi data
    print("Starting ingestion...")
    # result = ingest(2024, 1)
    # print(f"Ingested: {result}")
    print("Ingestion complete ✅")

def validate_task(**kwargs):
    import sys
    sys.path.insert(0, '/opt/airflow')
    from ge.validate_data import run_all_validations
    
    print("Running Great Expectations quality gates...")
    result = run_all_validations()
    
    if not result:
        raise Exception("Data quality gate failed — pipeline blocked!")
    
    print("All quality gates passed ✅")
    
def transform_task(**kwargs):
    print("Running dbt models...")
    # dbt comes in Phase 3
    print("Transformation complete ✅")

# --- DAG definition ---
with DAG(
    dag_id='ecommerce_pipeline',
    default_args=default_args,
    description='Self-healing ELT pipeline for e-commerce analytics',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ecommerce', 'self-healing'],
) as dag:

    ingest = PythonOperator(
        task_id='ingest_raw_data',
        python_callable=ingest_task,
    )

    validate = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_task,
    )

    transform = PythonOperator(
        task_id='transform_with_dbt',
        python_callable=transform_task,
    )

    # Task dependencies — the pipeline order
    ingest >> validate >> transform