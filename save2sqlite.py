import csv
import sqlite3

def sanitize_column_name(column_name):
    # Remove any characters that are not alphanumeric or underscores
    sanitized_name = ''.join(c for c in column_name if c.isalnum() or c == '_')
    return sanitized_name

def create_table_from_csv(csv_file, table_name, db_connection):
    # Read the CSV file and extract the header and data
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the first row as the header
        data = list(csv_reader)

    # Sanitize column names
    sanitized_header = [sanitize_column_name(column) for column in header]

    # Create the table with sanitized column names
    cursor = db_connection.cursor()
    column_names = ', '.join(sanitized_header)
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_names})"
    cursor.execute(create_table_query)

    # Insert the CSV data into the table
    insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(sanitized_header))})"
    cursor.executemany(insert_query, data)

    # Commit the changes and close the database connection
    db_connection.commit()
    db_connection.close()

# Example usage
csv_file = 'errors.csv'  # Replace with your CSV file path
table_name = 'errors'  # Replace with the desired table name
db_connection = sqlite3.connect('errors.db')  # Replace with your database file

create_table_from_csv(csv_file, table_name, db_connection)
