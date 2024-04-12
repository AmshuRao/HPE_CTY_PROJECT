# Minutes of Meeting

- Discussed the script code and shared comments.
- Discussed checking the built-in batch transaction capability of DBs. Also, requested students to explore any methods/features provided by the respective DBs to reduce CRUD latency.
- Requested students to share the plotted graphs listing all DBs.
- Each student presented the requested data for their DBs along with the code.
- Introduced the YCSB (Yahoo! Cloud Serving Benchmark) tool to students and requested them to run the tool for their respective DBs ([Link](https://github.com/brianfrankcooper/YCSB/wiki)).

## My Work

1. Made changes to the week 4 scripts as suggested by the mentors:
   - Added try-catch blocks for error handling.
   - Attempted to optimize the query using temporary tables.
   - Added functionality to visualize the time needed for insertion, deletion, and updating in a single graph.

2. Explored the YCSB tool and learned how it is used for benchmarking.

3. Installed the YCSB tool in the virtual machine and configured it for PostgreSQL.

4. Tried out the basic load and run operations using the default workload given in the workload folder of YCSB.

### Installation Process 

- **Download the latest release of YCSB:**
``` 
wget https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/ycsb-0.17.0.tar.gz
tar xfvz ycsb-0.17.0.tar.gz
cd ycsb-0.17.0 
```

- **Set up a database to benchmark. There is a README file under each binding directory.**
- The following commands can be used for setting up the PostgreSQL database:
  ```
  CREATE DATABASE test;
  CREATE TABLE usertable (YCSB_KEY VARCHAR(255) PRIMARY KEY not NULL, YCSB_VALUE JSONB not NULL);
  GRANT ALL PRIVILEGES ON DATABASE test to postgres;
  ```

- **Run YCSB command.**
- On Linux:
  ```
  bin/ycsb.sh load basic -P workloads/workloada
  bin/ycsb.sh run basic -P workloads/workloada
  ```

### Common Errors Encountered

1. **Maven Binding Errors:** If you try to install YCSB by cloning the GitHub repository, you might encounter errors during the compilation process (compilation is done using the command: `mvn clean package`).
 - **Solution:** Download the latest version of YCSB using the link provided in the installation process. Extract it using tar.

2. **Python Syntax Error:** YCSB latest version (YCSB 0.17.0) is meant to run with Python 2, but by default Ubuntu machines execute the code in Python 3.
 - **Solution:** Go to `YCSB/your_database_folder/YCSB.py`. There, in the first line, change `python` to `python2`.

3. **Java Class Exception Error:** When you try to execute `./bin/ycsb` commands, you might encounter a "java class not defined" error.
 - **Solution:** Install OpenJDK-8 using the command `sudo apt install openjdk-8-jdk`.

### Results

- **Common graph for insertion, deletion, and updating:**
![Common Plot](C:\Users\amshu\Desktop\FOLDER\HPE_project\WEEK_5\common_plot.png)

- **YCSB tool basic load and run operations:**
1) Load operation: 

![Load Operation](ycsb_load_operation.png)

2) Run operation: 

![Run Operation](ycsb_run_operation.png)