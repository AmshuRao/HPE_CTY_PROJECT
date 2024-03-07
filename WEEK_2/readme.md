# Project Progress Report - Week 2 (Date: 08-03-2024)

## My Work (Date: 16-02-2024)

1. Created a virtual machine instance of Ubuntu ([Reference](https://youtu.be/hYaCCpvjsEY?si=u8PoXqS5MuIpX6ke)).
2. Installed PostgreSQL in Ubuntu ([Reference](https://youtu.be/INJl3PLVZMo?si=RmPwejbnIfHeWZYN) and [DigitalOcean Guide](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-22-04-quickstart)).
3. Installed psycopg2 and `sudo apt-get install libpq-dev` (required for psycopg2 installation).
4. Created CSV files with 5 tuples ({source_ip, dest_ip, src_port, dest_port, ip_format}).
5. Developed an automated bulk insertion script that inserts 'n' lines from a CSV file into the database (with 'n' being given by the user).

## Additional Notes:

1. Used a shared file structure in the virtual machine, allowing the use of the same files in both the base OS (Windows in my case) and the virtual machine (Ubuntu). Steps for doing the same ([Reference](https://carleton.ca/scs/tech-support/troubleshooting-guides/creating-a-shared-folder-in-virtualbox/)):
   - Go to Devices -> Shared Folder -> Add Folder.
   - Auto_mount -> Check.
   - Click OK.

2. File handling in Python ([Reference](https://www.geeksforgeeks.org/reading-csv-files-in-python/)).
