from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "sugashini",
    "start_date": datetime(2026, 1, 1)
}

with DAG(
    dag_id="sec_10k_rag_pipeline",
    default_args=default_args,
    schedule=None,
    catchup=False
) as dag:

    parse_html = BashOperator(
        task_id="parse_html",
        bash_command="""
        python3 /Users/sugashinikaliappan/sec-rag-project/src/parsing/parse_10k.py
        """
    )

    extract_sections = BashOperator(
        task_id="extract_sections",
        bash_command="""
        python3 /Users/sugashinikaliappan/sec-rag-project/src/parsing/extract_sections.py
        """
    )

    chunk_sections = BashOperator(
        task_id="chunk_sections",
        bash_command="""
        python3 /Users/sugashinikaliappan/sec-rag-project/src/chunking/chunk_sections.py
        """
    )

    create_vector_db = BashOperator(
        task_id="create_vector_db",
        bash_command="""
        python3 /Users/sugashinikaliappan/sec-rag-project/src/embeddings/create_vector_db.py
        """
    )

    parse_html >> extract_sections >> chunk_sections >> create_vector_db
