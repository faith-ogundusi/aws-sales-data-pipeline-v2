import boto3
import json
import time

athena = boto3.client("athena")
s3 = boto3.client("s3")

DATABASE = "sales_pipeline_v2"
OUTPUT_BUCKET = "faith-sales-pipeline-v2"
ATHENA_OUTPUT = "s3://faith-sales-pipeline-v2/athena-results/"
DASHBOARD_KEY = "dashboard/kpis.json"


def run_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            "Database": DATABASE
        },
        ResultConfiguration={
            "OutputLocation": ATHENA_OUTPUT
        }
    )

    query_id = response["QueryExecutionId"]

    while True:
        status = athena.get_query_execution(
            QueryExecutionId=query_id
        )["QueryExecution"]["Status"]["State"]

        if status == "SUCCEEDED":
            break

        if status in ["FAILED", "CANCELLED"]:
            raise Exception(f"Athena query {status}")

        time.sleep(1)

    result = athena.get_query_results(
        QueryExecutionId=query_id
    )

    return result["ResultSet"]["Rows"]


def get_value(rows):
    return rows[1]["Data"][0].get("VarCharValue", "0")


def lambda_handler(event, context):

    queries = {
        "total_processed": """
            SELECT
                (SELECT COUNT(*) FROM valid_sales)
                +
                (SELECT COUNT(*) FROM rejected_sales)
        """,

        "valid_count": """
            SELECT COUNT(*) FROM valid_sales
        """,

        "rejected_count": """
            SELECT COUNT(*) FROM rejected_sales
        """,

        "total_revenue": """
            SELECT ROUND(SUM(Revenue), 2) FROM valid_sales
        """,

        "average_transaction_value": """
            SELECT ROUND(AVG(Revenue), 2) FROM valid_sales
        """,

        "country_revenue": """
            SELECT Country, ROUND(SUM(Revenue), 2) AS total_revenue
            FROM valid_sales
            GROUP BY Country
            ORDER BY total_revenue DESC
        """,

        "top_products": """
            SELECT StockCode, Description,
                   ROUND(SUM(Revenue), 2) AS total_revenue
            FROM valid_sales
            GROUP BY StockCode, Description
            ORDER BY total_revenue DESC
            LIMIT 10
        """,

        "monthly_revenue": """
            SELECT
                date_format(
                    date_parse(InvoiceDate, '%m/%d/%Y %H:%i'),
                    '%Y-%m'
                ) AS month,
                ROUND(SUM(Revenue), 2) AS total_revenue
            FROM valid_sales
            GROUP BY 1
            ORDER BY 1
        """
    }

    dashboard = {}

    for name, query in queries.items():
        rows = run_query(query)

        if name in [
            "total_processed",
            "valid_count",
            "rejected_count",
            "total_revenue",
            "average_transaction_value"
        ]:
            dashboard[name] = float(get_value(rows))
        else:
            dashboard[name] = [
                [cell.get("VarCharValue", "") for cell in row["Data"]]
                for row in rows[1:]
            ]

    dashboard["valid_percentage"] = round(
        dashboard["valid_count"]
        / dashboard["total_processed"]
        * 100,
        2
    )

    dashboard["rejected_percentage"] = round(
        dashboard["rejected_count"]
        / dashboard["total_processed"]
        * 100,
        2
    )

    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=DASHBOARD_KEY,
        Body=json.dumps(dashboard, indent=2),
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "message": "Dashboard data updated successfully",
        "dashboard_key": DASHBOARD_KEY
  }
