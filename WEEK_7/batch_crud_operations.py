import psycopg2
from datetime import datetime
import matplotlib.pyplot as plt
import io

# Function to read data from file
def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip().split(',') for line in file]
        # Convert port values to integers
        data = [(src_ip, dest_ip, int(src_port), int(dest_port), ip_type) for src_ip, dest_ip, src_port, dest_port, ip_type in data]
    return data

# Function to print table
def print_table(time_seconds):
    header = f"| {'Batch Number':^20} | {'Time (seconds)':^15} |"
    separator = '-' * len(header)
    print(separator)
    print(header)
    print(separator)
    for i, time in enumerate(time_seconds):
        number_of_batches = i + 1
        time_str = str(time)
        print(f"| {number_of_batches:^20} | {time_str:^15} |")
    print(separator)

# Function to plot graph
def print_graph(time_seconds):
    time_seconds_in_seconds = [time.total_seconds() for time in time_seconds]
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(time_seconds) + 1), time_seconds_in_seconds, marker='o', linestyle='-')
    plt.title('Time in Seconds')
    plt.xlabel('Batch Number')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.show()

try:
    # Establish database connection
    conn = psycopg2.connect(database="postgres", user="postgres", host='127.0.0.1', password="postgres", port=5432)
    cur = conn.cursor()

    # Create temporary table for deletion
    cur.execute("""
        CREATE TEMP TABLE temp_delete_table (
            src_ip TEXT,
            dest_ip TEXT,
            src_port INT,
            dest_port INT,
            ip_type TEXT
        );
    """)
    conn.commit()
    cur.execute("""
        CREATE TEMP TABLE temp_update_table (
            src_ip TEXT,
            dest_ip TEXT,
            src_port INT,
            dest_port INT,
            ip_type TEXT
        );
    """)
    conn.commit()

    cnt = 0
    time_for_deletion = []
    time_for_insertion = []
    time_for_updation = []

    while True:
        print("\n\nMAIN MENU FOR BATCH OPERATIONS(BATCHES OF 1,00,000)\n\n1) Delete tuples from the database\n2) Insert tuples from csv\n3) Update tuples in databases\n4)Exit\n")
        choice = int(input("Enter your choice : "))
        
        if choice == 1:
            # Delete tuples
            t=datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
            conn.commit()
            data = read_data_from_file("shuffled_data.csv")
            delete_query = "COPY temp_delete_table (src_ip, dest_ip, src_port, dest_port, ip_type) FROM STDIN WITH CSV"
            batch_size = int(input("enter the batch size: "))

            num_batches = int(input("enter the number of batches"))
            time_for_deletion = []

            for i in range(num_batches):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, len(data))
                batch_data = data[start_idx:end_idx]

                
                data_csv = "\n".join([",".join(map(str, row)) for row in batch_data])
                start_time = datetime.now()
                cur.copy_expert(sql=delete_query, file=io.StringIO(data_csv))
                conn.commit()
                cur.execute("DELETE FROM flow_table WHERE EXISTS (SELECT 1 FROM temp_delete_table WHERE flow_table.src_ip = temp_delete_table.src_ip AND flow_table.dest_ip = temp_delete_table.dest_ip AND flow_table.src_port = temp_delete_table.src_port AND flow_table.dest_port = temp_delete_table.dest_port AND flow_table.ip_type = temp_delete_table.ip_type)")
                conn.commit()
                end_time = datetime.now()
                time_for_deletion.append(end_time - start_time)
            for i in time_for_deletion:
                t+=i
            time_difference = t - datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)

            # Calculate the time required for insertion in seconds as a float
            time_required_seconds_float = (time_difference / num_batches).total_seconds() * (1000000 / batch_size)

            print("Time required for deleting (in seconds ) :", time_required_seconds_float) 

            
            # print_table(time_for_deletion)
            # print_graph(time_for_deletion)

        elif choice == 2:
            # Insert tuples
            data = read_data_from_file("data_1000000_tuples.csv")
            insert_query = "COPY flow_table (src_ip, dest_ip, src_port, dest_port, ip_type) FROM STDIN WITH CSV"
            batch_size = int(input("enter the batch size : "))

            num_batches = (len(data) + batch_size - 1) //batch_size
            time_for_insertion = []

            for i in range(num_batches):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, len(data))
                batch_data = data[start_idx:end_idx]
                data_csv = "\n".join([",".join(map(str, row)) for row in batch_data])
                start_time = datetime.now()
                cur.copy_expert(sql=insert_query, file=io.StringIO(data_csv))
                conn.commit()
                end_time = datetime.now()
                time_for_insertion.append(end_time - start_time)
            t = datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
            for i in time_for_insertion:
                t+=i
            time_difference = t - datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)

            # Calculate the time required for insertion in seconds as a float
            time_required_seconds_float = (time_difference.total_seconds())

            print("Time required for insertion (in seconds ) :", time_required_seconds_float) 

        elif choice == 3:
            # Update tuples
            t=datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
            data = read_data_from_file("shuffled_data.csv")
            update_query = "COPY temp_update_table (src_ip, dest_ip, src_port, dest_port, ip_type) FROM STDIN WITH CSV"
            batch_size = int(input("enter the batch size: "))

            num_batches = int(input("enter the number of batches"))
            time_for_updation = []

            for i in range(num_batches):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, len(data))
                batch_data = data[start_idx:end_idx]

                data_csv = "\n".join([",".join(map(str, row)) for row in batch_data])
                cur.copy_expert(sql=update_query, file=io.StringIO(data_csv))
                conn.commit()
                start_time = datetime.now()
                cur.execute("UPDATE flow_table SET src_port = 0 FROM temp_update_table WHERE flow_table.src_ip = temp_update_table.src_ip AND flow_table.dest_ip = temp_update_table.dest_ip AND flow_table.src_port = temp_update_table.src_port AND flow_table.dest_port = temp_update_table.dest_port AND flow_table.ip_type = temp_update_table.ip_type")
                conn.commit()
                end_time = datetime.now()
                time_for_updation.append(end_time - start_time)

            for i in time_for_updation:
                t+=i
            time_difference = t - datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)

            # Calculate the time required for insertion in seconds as a float
            time_required_seconds_float = (time_difference.total_seconds() / num_batches) * (1000000 / batch_size)

            print("Time required for updating (in seconds ) :", time_required_seconds_float) 

            
            # print_table(time_for_deletion)
            # print_graph(time_for_deletion)

        else:
            exit(0)

except psycopg2.Error as e:
    print("Error while connecting to PostgreSQL:", e)

except Exception as e:
    print("An error occurred:", e)

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
