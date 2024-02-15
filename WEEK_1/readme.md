# Project Progress Report - Week 1 (Date: 16-02-2024)

## Minutes of Meeting (MoM)

- Tathagatha gave a brief talk about the project.
- Renjith presented details about network flows and flowDB (Network flow database), context and requirements.
- Assigned the next set of AI’s for each student.
- Next meeting to be scheduled tentatively on 2/16 for follow-up on AI’s.
- Students informed about their exams beginning from 2/20 to 3/4.
- Q&A.

## AI Assignments

- Each student agreed to pick up an opensource database from those listed in the slide.
- Perform primarily 3 operations (insert/update/delete) to the database. The dataset should be network flows with 5 tuples.
- Start with a small dataset (like 100’s or 1000’s) and scale up later.
- It would be good to automate some of these DB operations. So, start looking at writing python scripts to do the operations to DB.
- The following is the assignment order of DB to each student:
  - MongoDB - Raghavendra
  - PostgreSQL - Amshu
  - MariaDB - Naga Ashrith
  - SQLite - Monica
  - ArangoDB - Deeksha

## My Progress (PostgreSQL)
1. Installed PostgreSQL in WSl and pgadmin4 in Windows ([Reference](https://www.datacamp.com/tutorial/tutorial-postgresql-python)).
2. Tried out operations like create, delete, update, insert, alter in Postgres DB ([Reference](https://www.datacamp.com/tutorial/tutorial-postgresql-python)).
3. Created a table called flow_db and assigned values like src_ip, dest_ip, src_port, dest_port, ip_type, and id.
4. Made the combination of src_port and dest_port as a composite key.
5. Wrote a script in Python to automatically insert values into the database using psycopg2 module ([Reference](https://www.datacamp.com/tutorial/tutorial-postgresql-python)).