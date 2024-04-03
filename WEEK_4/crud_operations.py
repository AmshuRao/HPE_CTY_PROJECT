import psycopg2
from datetime import datetime
import matplotlib.pyplot as plt
import time

def print_table(time_seconds):
        header = f"| {'Number of tuples':^20} | {'Time (seconds)':^15} |"

        # Define separator line
        separator = '-' * len(header)

        # Print header and separator
        print(separator)
        print(header)
        print(separator)
        points = []
        for i in range(0,len(time_seconds)):
             points.append(100*(10**i))
        # Print table rows
        for i, time in enumerate(time_seconds):
            number_of_tuples =points[i]
            time_str = str(time)
            print(f"| {number_of_tuples:^20} | {time_str:^15} |")

        # Print bottom separator
        print(separator)


def print_graph(time_seconds):
    
        time_seconds_in_seconds = [time.total_seconds() for time in time_seconds]
        points = []
        for i in range(0,len(time_seconds)):
             points.append(100*(10**i))
        
        # Plot the graph
        plt.figure(figsize=(8, 6))
        plt.plot(points, time_seconds_in_seconds, marker='o', linestyle='-')
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




while(1):
    print("\n\nMAIN MENU\n\n1)Delete random tuples from the database\n2)Insert random tuples from csv\n3)Update random tuples in database\n4)Exit\n")
    choice = int(input("Enter your choice : "))
    if choice==1:
          time_for_deletion = []

          # Perform bulk deletion for different file sizes
          files_to_delete = ['data_100_delete.csv', 'data_1000_delete.csv', 'data_10000_delete.csv', 'data_100000_delete.csv']
          cur.execute("delete from flow_table;")
          conn.commit()
          with open('data_1000000_tuples.csv', 'r') as file:
               cur.copy_expert(f"COPY flow_table FROM STDIN WITH CSV HEADER", file)
               conn.commit()

          for filename in files_to_delete:
               time_before_deletion = datetime.now()
               #cnt = 0
               with open(filename, 'r') as file:
                    for line in file:
                         data = line.strip().split(",")
                         cur.execute("select * from flow_table where src_ip=%s and dest_ip=%s and src_port=%s and dest_port=%s and ip_type=%s",(data[0], data[1], int(data[2]), int(data[3]), data[4]))
                         rows = cur.fetchall()
                         if(len(rows)>0):
                              #cnt+=1
                              cur.execute("delete from flow_table where src_ip=%s and dest_ip=%s and src_port=%s and dest_port=%s and ip_type=%s",(data[0], data[1], int(data[2]), int(data[3]), data[4]))
                              conn.commit()
               #print(cnt)
                         
               time_after_deletion = datetime.now()
               time_for_deletion.append(time_after_deletion - time_before_deletion)
          # Print time taken for each deletion
          print_table(time_for_deletion)
          print_graph(time_for_deletion)



        
    elif choice==2:
          time_for_insertions = []
          files = ["data_100_tuples.csv", "data_1000_tuples.csv", "data_10000_tuples.csv", "data_100000_tuples.csv", "data_1000000_tuples.csv"]
          for filename in files:
               time_before_insertion = datetime.now()
               with open(filename, 'r') as file:
                    cur.copy_expert(f"COPY flow_table FROM STDIN WITH CSV HEADER", file)
                    conn.commit()
                    if(filename!="data_1000000_tuples.csv"):
                         cur.execute("delete from flow_table;")
               time_after_insertion = datetime.now()
               time_for_insertions.append(time_after_insertion - time_before_insertion)

          # Print time taken for each insertion
          print_table(time_for_insertions)
          print_graph(time_for_insertions)
    elif choice==3:
        time_for_updation = []
        files = ["data_100_tuples.csv", "data_1000_tuples.csv", "data_10000_tuples.csv", "data_100000_tuples.csv"]
        for filename in files:
            time_before_updation = datetime.now()
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(",")
                    cur.execute("UPDATE flow_table SET src_ip=%s WHERE src_ip=%s AND dest_ip=%s AND src_port=%s AND dest_port=%s AND ip_type=%s",(data[1], data[0], data[1], int(data[2]), int(data[3]), data[4]))
            conn.commit()
            time_after_updation = datetime.now()
            time_for_updation.append(time_after_updation - time_before_updation)
        print_table(time_for_updation)
        print_graph(time_for_updation)
    else:
        exit(0)