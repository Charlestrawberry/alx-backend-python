#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields user ages one by one from user_data"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def compute_average_age():
    """Compute average age using the stream_user_ages generator"""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    compute_average_age()
