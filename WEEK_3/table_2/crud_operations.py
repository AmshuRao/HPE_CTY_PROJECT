import psycopg2
from datetime import datetime
import matplotlib.pyplot as plt

def print_table(time_seconds):
        header = f"| {'Number of tuples':^20} | {'Time (seconds)':^15} |"

        # Define separator line
        separator = '-' * len(header)

        # Print header and separator
        print(separator)
        print(header)
        print(separator)

        # Print table rows
        for i, time in enumerate(time_seconds):
            number_of_tuples = 0
            if i == 0:
                number_of_tuples = 100
            elif i == 1:
                number_of_tuples = 1000
            else:
                number_of_tuples = 10000
    
            time_str = str(time)
            print(f"| {number_of_tuples:^20} | {time_str:^15} |")

        # Print bottom separator
        print(separator)


def print_graph(time_seconds):
    
        time_seconds_in_seconds = [time.total_seconds() for time in time_seconds]

        x_axis_points = [100, 1000, 10000]
        
        # Plot the graph
        plt.figure(figsize=(8, 6))
        plt.plot(x_axis_points, time_seconds_in_seconds, marker='o', linestyle='-')
        plt.title('Time in Seconds')
        plt.xlabel('Number of Tuples')
        plt.ylabel('Time (seconds)')
        plt.grid(True)
        plt.xscale('log') 
        plt.show()


    

conn = psycopg2.connect(database = "postgres", 
                        user = "postgres", 
                        host= '127.0.0.1',
                        password = "postgres",
                        port = 5432)
cur = conn.cursor()

time_for_insertions = []


while(1):
    print("\n\nMAIN MENU\n\n1)Delete a tuple\n2)Insert random tuples from csv\n3)Exit\n")
    choice = int(input("Enter your choice : "))
    if choice==1:
        src,dest,src_ip,dest_ip,ip_type = input("Enter the five tuples to identify the document (src_port, dest_port, src_ip, dest_ip, ip_type)\n").split(" ")
        src=int(src)
        dest=int(dest)
        cur.execute(f"DELETE FROM flow_table2 WHERE src_port = {dest} AND dest_port = {src} AND src_ip = '{dest_ip}' AND dest_ip = '{src_ip}' AND ip_type = '{ip_type}';")
        conn.commit()
    elif choice==2:
        time_before_insertion = datetime.now()
        with open("data_100_tuples.csv")as file:
            for line in file:
                    data = line.split(",")
                    cur.execute(f"insert into flow_table2(src_ip,dest_ip,src_port,dest_port,ip_type) values('{data[0]}','{data[1]}',{int(data[2])},{int(data[3])},'{data[4].strip()}');")
                    conn.commit()
        time_after_insertion = datetime.now()
        time_for_insertions.append(time_after_insertion-time_before_insertion)

        time_before_insertion = datetime.now()
        with open("data_1000_tuples.csv")as file:
            for line in file:
                    data = line.split(",")
                    cur.execute(f"insert into flow_table2(src_ip,dest_ip,src_port,dest_port,ip_type) values('{data[0]}','{data[1]}',{int(data[2])},{int(data[3])},'{data[4].strip()}');")
                    conn.commit()
        time_after_insertion = datetime.now()
        time_for_insertions.append(time_after_insertion-time_before_insertion)

        time_before_insertion = datetime.now()
        with open("data_10000_tuples.csv")as file:
            for line in file:
                    data = line.split(",")
                    cur.execute(f"insert into flow_table2(src_ip,dest_ip,src_port,dest_port,ip_type) values('{data[0]}','{data[1]}',{int(data[2])},{int(data[3])},'{data[4].strip()}');")
                    conn.commit()
        time_after_insertion = datetime.now()
        time_for_insertions.append(time_after_insertion-time_before_insertion)

        print_table(time_for_insertions)
        print_graph(time_for_insertions)

    else:
        exit(0)
