# Updation Results

**Note 1:** Average values (time required to update a single record) are taken for comparison.

**Note 2:** Python script values and YCSB values are in seconds.

| Number of tuples | Python Script Values | YCSB (avg latency) | Ratio  |
|------------------|----------------------|---------------------|--------|
| 100              | 0.000828             | 0.1667              | 201.32 |
| 1000             | 0.000712             | 0.11984             | 168.31 |
| 10000            | 0.0007957            | 0.12254             | 153.94 |

![Comparison Graph](./images/updation_graph_normal.png)

**Observation:** As we can see, every ratio is in the order of 100, indicating that the Python script values match the corresponding values with the YCSB tool.