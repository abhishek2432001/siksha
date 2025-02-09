from django.db import connections
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor

def fetch_all(query, verbose=settings.DEBUG):
    """ Returns column_names, output of query

    :param query: query to be executed
    :param verbose: debug data display settings (data type - boolean)
    :return: columns_names, queryset
    """
    connection = connections['read_only']
    with connection.cursor() as cursor:
        if verbose:
            print("executing " + query)
        cursor.execute(query)
        rows = cursor.fetchall()
        keys = [i[0] for i in cursor.description]
        return keys, rows


def fetch_one(query, verbose=settings.DEBUG):
    """
    Fetch a single row from the database
    Args:
        query: The SQL query to execute
        verbose: Whether to log the query before executing
    Returns:
        row: The first row returned by the query or an empty list
    - Open a read-only database connection
    - Execute the query with the connection's cursor
    - Fetch the first row returned
    - Return the row or an empty list if no row was returned
    """
    connection = connections['read_only']
    with connection.cursor() as cursor:
        if verbose:
            print("executing " + query)
        cursor.execute(query)
        row = cursor.fetchone()
        if not row:
            row = []
    return row


def fetch_concurrently(query_list: list, workers=4):
    results = [None] * len(query_list)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Use enumerate to keep track of the query's original index
        futures = {executor.submit(fetch_all, query): index for index, query in enumerate(query_list)}
        for future in futures:
            index = futures[future]
            results[index] = future.result()
    return results