from google.cloud import bigquery
import csv

def load_data_to_big_query(client: bigquery.Client, table_name: str,
                           file_name: str, SELECTED_HEADERS: set, SCHEMA_FIELDS: list):
    """
    Reads data from a csv `file_name` and writes it to bigquery in the `table_name` table
    How to use: Takes in the headers you want to load into BigQuery, along with a list of bigquery SchemaField definitions. Example:

    SELECTED_HEADERS = {
        'conversation_id',
        'normalized_query'
    }

    SCHEMA_FIELDS = [
        bigquery.SchemaField("conversation_id", "STRING"),
        bigquery.SchemaField("normalized_query", "STRING"),
    ]

    """
    with open(file_name, 'r') as infile:
        rows = csv.DictReader(infile)
        filtered_rows = [
            {k: v for k, v in row.items() if k in SELECTED_HEADERS}
            for row in
            rows
        ]

    print("Inserted %s rows" % len(filtered_rows))
    client.insert_rows(table_name, filtered_rows, SCHEMA_FIELDS)