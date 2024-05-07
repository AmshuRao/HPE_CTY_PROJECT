import traceback
import psycopg2
from datetime import datetime, timedelta
import json

# Function to read data from file
def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip().split(',') for line in file]
        # Convert port values to integers
        data = [(src_ip, dest_ip, int(src_port), int(dest_port), ip_type) for src_ip, dest_ip, src_port, dest_port, ip_type in data]
    return data

try:
    # Establish database connection
    conn = psycopg2.connect(database="postgres", user="postgres", host='127.0.0.1', password="postgres", port=5432)
    cur = conn.cursor()

    def check_data_existence(data_tuple):
        cur.execute("SELECT EXISTS (SELECT 1 FROM json_table WHERE data = %s)", (json.dumps({"src_ip": data_tuple[0], "dest_ip": data_tuple[1], "src_port": data_tuple[2], "dest_port": data_tuple[3], "ip_type": data_tuple[4]}),))
        result = cur.fetchone()[0]
        return result

    def insert_data(batch_size, num_batches):
        # Read data from file
        data = read_data_from_file("..//data//data_1000000_tuples.csv")

        # Insert data into database using JSONB format in batches
        insert_query = "INSERT INTO json_table (data) VALUES (%s)"
        batch_data = [(json.dumps({"src_ip": src_ip, "dest_ip": dest_ip, "src_port": src_port, "dest_port": dest_port, "ip_type": ip_type}),) for src_ip, dest_ip, src_port, dest_port, ip_type in data]

        start_time = datetime.now()
        inserted_count = 0
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(batch_data))
            for data_tuple in batch_data[start_idx:end_idx]:
                data_dict = json.loads(data_tuple[0])
                data_tuple = (data_dict["src_ip"], data_dict["dest_ip"], data_dict["src_port"], data_dict["dest_port"], data_dict["ip_type"])
                if not check_data_existence(data_tuple):
                    cur.execute(insert_query, (json.dumps({"src_ip": data_tuple[0], "dest_ip": data_tuple[1], "src_port": data_tuple[2], "dest_port": data_tuple[3], "ip_type": data_tuple[4]}),))
                    inserted_count += 1
                    conn.commit()

        end_time = datetime.now()
        total_time = end_time - start_time
        print(f"{inserted_count} records inserted successfully! Total time taken: {total_time}")


    def delete_data(batch_size, num_batches):
        # Read data from file
        data = read_data_from_file("..//data//shuffled.csv")
        delete_query = "DELETE FROM json_table WHERE data = %s"

        start_time = datetime.now()
        deleted_count = 0
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(data))
            for row in data[start_idx:end_idx]:
                data_tuple = (row[0], row[1], int(row[2]), int(row[3]), row[4])  # Assuming data format matches table schema
                if check_data_existence(data_tuple):
                    cur.execute(delete_query, (json.dumps({"src_ip": data_tuple[0], "dest_ip": data_tuple[1], "src_port": data_tuple[2], "dest_port": data_tuple[3], "ip_type": data_tuple[4]}),))
                    deleted_count += 1
                    conn.commit()
                    print(f"Data with attributes {data_tuple} deleted successfully!")

        end_time = datetime.now()
        total_time = end_time - start_time
        print(f"{deleted_count} records deleted successfully! Total time taken for deletion: {total_time}")

    def update_data(batch_size, num_batches):
        # Read data from file
        data = read_data_from_file("..//data//shuffled.csv")
        update_query = "UPDATE json_table SET data = jsonb_set(data, '{src_port}', to_jsonb(%s)) WHERE data = %s"

        start_time = datetime.now()
        updated_count = 0
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(data))
            for row in data[start_idx:end_idx]:
                data_tuple = (row[0], row[1], int(row[2]), int(row[3]), row[4])  # Assuming data format matches table schema
                if check_data_existence(data_tuple):
                    cur.execute(update_query, (int(row[2]), json.dumps({"src_ip": data_tuple[0], "dest_ip": data_tuple[1], "src_port": data_tuple[2], "dest_port": data_tuple[3], "ip_type": data_tuple[4]}),))
                    updated_count += 1
                    conn.commit()
                    print(f"Data with attributes {data_tuple} updated successfully!")

        end_time = datetime.now()
        total_time = end_time - start_time
        print(f"{updated_count} records updated successfully! Total time taken for updation: {total_time}")

    while True:
        print("\nMAIN MENU\n1) Insert Data\n2) Delete Data\n3) Update Data\n4) Exit\n")
        choice = input("Enter your choice: ")

        if choice == '1':
            batch_size = int(input("Enter the batch size: "))
            num_batches = int(input("Enter the number of batches: "))
            insert_data(batch_size, num_batches)
        elif choice == '2':
            batch_size = int(input("Enter the batch size: "))
            num_batches = int(input("Enter the number of batches: "))
            delete_data(batch_size, num_batches)
        elif choice == '3':
            batch_size = int(input("Enter the batch size: "))
            num_batches = int(input("Enter the number of batches: "))
            update_data(batch_size, num_batches)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

except psycopg2.Error as e:
    print("Error while connecting to PostgreSQL:", e)

except Exception as e:
    print("An error occurred:", e)
    print(traceback.format_exc()) 

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
