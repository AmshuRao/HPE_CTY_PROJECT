import psycopg2
from datetime import datetime
import matplotlib.pyplot as plt


def main():
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            host='127.0.0.1',
                            password="postgres",
                            port=5432)
    cur = conn.cursor()
    time_for_deletion = []
    time_for_insertions = []
    time_for_updation = []

    while True:
        print("\n\nMAIN MENU\n\n1)Delete random tuples from the database\n2)Insert random tuples from csv\n3)Update random tuples in database")
        
        print("4)Exit\n")
        choice = int(input("Enter your choice : "))
        try:
            if choice == 1:
                
                # Perform bulk deletion for different file sizes
                files_to_delete = ['data_100_delete.csv', 'data_1000_delete.csv', 'data_10000_delete.csv', 'data_100000_delete.csv']
                cur.execute("delete from flow_table;")
                conn.commit()
                with open('data_1000000_tuples.csv', 'r') as file:
                    cur.copy_expert(f"COPY flow_table FROM STDIN WITH CSV HEADER", file)
                    conn.commit()

                for filename in files_to_delete:
                    time_for_deletion = []
                    with open(filename, 'r') as file:
                        for line in file:
                            data = line.strip().split(",")
                            time_before_deletion = datetime.now()
                            cur.execute("delete from flow_table where src_ip=%s and dest_ip=%s and src_port=%s and dest_port=%s and ip_type=%s",(data[0], data[1], int(data[2]), int(data[3]), data[4]))
                            conn.commit()
                            time_after_deletion = datetime.now()
                            time_difference = time_after_deletion - time_before_deletion
                            time_for_deletion.append(time_difference.total_seconds())
                    print("Time required for deletion (in seconds per record ) for :",filename," ", sum(time_for_deletion)/len(time_for_deletion)) 

            elif choice == 2:
                
                files = ["data_100_tuples.csv", "data_1000_tuples.csv", "data_10000_tuples.csv", "data_100000_tuples.csv", "data_1000000_tuples.csv"]
                for filename in files:
                    time_for_insertions.clear()
                    with open(filename, 'r') as file:
                        time_before_insertion = datetime.now()
                        cur.copy_expert(f"COPY flow_table FROM STDIN WITH CSV HEADER", file)
                        conn.commit()
                        time_after_insertion = datetime.now()
                        if filename != "data_1000000_tuples.csv":
                            cur.execute("delete from flow_table;")
                    
                        time_difference = time_after_insertion - time_before_insertion
                        time_for_insertions.append(time_difference.total_seconds())
                    print("Time required for insertion (in seconds per record ) for  :",filename," ", sum(time_for_insertions)/len(time_for_insertions))

            elif choice == 3:
                
                files = ["data_100_delete.csv", "data_1000_delete.csv", "data_10000_delete.csv", "data_100000_delete.csv"]
                for filename in files:
                    time_for_updation.clear()
                    with open(filename, 'r') as file:
                        for line in file:
                            data = line.strip().split(",")
                            time_before_updation = datetime.now()
                            cur.execute("UPDATE flow_table SET src_port=%s WHERE src_ip=%s AND dest_ip=%s AND src_port=%s AND dest_port=%s AND ip_type=%s",(100, data[0], data[1], int(data[2]), int(data[3]), data[4]))
                            time_after_updation = datetime.now()
                            time_difference = time_after_updation - time_before_updation
                            time_for_updation.append(time_difference.total_seconds())
                    print("Time required for updation (in seconds per record ) for  :",filename," ", sum(time_for_updation)/len(time_for_updation))
                    conn.commit()
                    
                    
                
            else:
                exit(0)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
