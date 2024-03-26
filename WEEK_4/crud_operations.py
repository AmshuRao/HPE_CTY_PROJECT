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

          for filename in files_to_delete:
               time_before_deletion = datetime.now()
               with open(filename, 'r') as file:
                    for line in file:
                         data = line.strip().split(",")
                         cur.execute(f"DELETE FROM flow_table WHERE src_ip='{data[0]}' AND dest_ip='{data[1]}' AND src_port={int(data[2])} AND dest_port={int(data[3])} AND ip_type='{data[4]}'")
               conn.commit()
               time_after_deletion = datetime.now()
               time_for_deletion.append(time_after_deletion - time_before_deletion)
               # note : here to maintain the structure of the database we are reinserting the tuples back into the database
               with open(filename, 'r') as file:
                    cur.copy_expert(f"COPY flow_table FROM STDIN WITH CSV HEADER", file)
                    conn.commit()
               

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

    else:
        exit(0)
