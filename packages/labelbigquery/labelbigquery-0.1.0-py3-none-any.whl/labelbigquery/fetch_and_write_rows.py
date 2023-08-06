import bigquery
from pathlib import Path

def fetch_and_write_rows(client: bigquery.Client, query:str):
    """
    Combines texts by conversation id into txt files and write them to disk under a `data` folder.
    Later on you can upload each txt file to Labelbox for annotation.
    The filename should be a unique identifier and the first column in the query (e.g. transaction id, conversation id, etc...)
    Query should have two columns, the first is the unique identifier and the second is the string data for that identifier

    Example: query = fr'SELECT conversation_id, STRING_AGG(normalized_query, "\n") FROM {table_name} GROUP BY conversation_id'
    """

    job = client.query(query)
    rows = list(job.result())

    Path("data").mkdir(exist_ok=True)
    for id, text in rows:
        with open(f"data/{id}.txt", "w") as outfile:
            outfile.write(text)
    return [f"data/{row[0]}.txt" for row in rows]