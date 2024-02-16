import psycopg2
import random
import ipaddress

conn = psycopg2.connect(database = "customer", 
                        user = "admin", 
                        host= '127.0.0.1',
                        password = "admin",
                        port = 5432)
cur = conn.cursor()

def generate_random_ip(ip_type, min_value, max_value):
    if ip_type == 'IPv4':
        return '.'.join(str(random.randint(min_value, max_value)) for _ in range(4))
    elif ip_type == 'IPv6':
        return ':'.join('{:04x}'.format(random.randint(min_value, max_value)) for _ in range(8))

def generate_random_port():
    return random.randint(1, 65535)

def generate_random_ip_type():
    return random.choice(['IPv4', 'IPv6'])


min_ip_value = 1
max_ip_value = 255


while(1):
    print("\n\nMAIN MENU\n\n1)Update a tuple\n2)Delete a tuple\n3)Insert random tuples\n4)Show table\n5)Exit\n")
    choice = int(input("Enter your choice : "))
    if choice==1:
        src,dest = input("Enter the src and dest port to identify the document\n").split(" ")
        src=int(src)
        dest=int(dest)
        cur.execute(f"update flow_table set src_ip = '{generate_random_ip(generate_random_ip_type(), min_ip_value, max_ip_value)}' where src_port = {src} and dest_port = {dest};")
        conn.commit()
    elif choice==2:
        src,dest = input("Enter the src and dest port to identify the document\n").split(" ")
        src=int(src)
        dest=int(dest)
        cur.execute(f"delete from flow_table where src_port = {src} and dest_port = {dest};")
        conn.commit()
    elif choice==3:
        num = int(input("Enter the number of records you want to insert\n"))
        for i in range(0,num):
            src_ip_type = generate_random_ip_type()
            dest_ip_type = generate_random_ip_type()

            src_ip = generate_random_ip(src_ip_type, min_ip_value, max_ip_value)
            dest_ip = generate_random_ip(dest_ip_type, min_ip_value, max_ip_value)

            src_port = generate_random_port()
            dest_port = generate_random_port()
            cur.execute(f"insert into flow_table(src_ip,dest_ip,src_port,dest_port,ip_type) values('{src_ip}','{dest_ip}',{src_port},{dest_port},'{src_ip_type}');")
            conn.commit()
    elif choice==4:
            cur.execute("select * from flow_table;")
            rows = cur.fetchall()
            for row in rows:
                print(row)
    else:
        exit(0)