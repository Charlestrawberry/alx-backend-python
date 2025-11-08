#!/usr/bin/python3
import seed  # use your seed.py from the previous task

def stream_users():
    """Generator function to stream users one by one from user_data table"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    # Select all rows
    cursor.execute("SELECT * FROM user_data")

    # Loop over rows and yield one at a time
    for row in cursor:
        yield row

    # Close after streaming
    cursor.close()
    connection.close()
