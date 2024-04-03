# Weekly Assignment - 3 (Date: 16-03-2024)

## Tasks:

1. Measure the time required for inserting 100, 1000, 10000 tuples into the database and compare them.
2. Provide functionality to delete the reverse of the packet.

## My Work:

1. Created a Python script to generate CSV files with 100, 1000, and 10000 tuples. Each file contains random IP addresses and port numbers, ensuring that no two tuples are identical. The script generates the tuple and its reverse (the packet one would receive as a response from the server or process to which the request packet is sent).

2. Developed another Python script that:
   - Inserts the tuples from the CSV files into the database and measures the time required for insertion.
   - Provides a graphical view of the insertion time for better understanding of the time complexity.
   - Implements functionality to obtain details about a packet from the user and deletes its reverse from the database.

## Additional Points to Note:

1. The primary key of the database in the PostgreSQL server includes all five tuples (src_port, dest_port, src_ip, dest_ip, ip_type).
2. Graphs are plotted using the matplotlib module in Python ([Reference](https://www.geeksforgeeks.org/simple-plot-in-python-using-matplotlib/)).

## Observations:

- The time required for insertion in PostgreSQL is usually higher compared to other databases like MongoDB, MySQL, etc. ([Reference](https://www.mongodb.com/compare/mongodb-postgresql))