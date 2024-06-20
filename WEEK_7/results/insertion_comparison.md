# Insertion Operations Comparison

**Note 1:** Average values (time required to insert a single record) are taken for comparison.

**Note 2:** Python script values and YCSB values are in seconds.


| Count  | Python Script Values | YCSB Values (avg latency) | Ratio  |
|--------|----------------------|-------------|--------|
| 100    | 0.84             | 0.83    | 1.01  |
| 1000   | 12.7             | 10.64    | 1.19  |
| 10000  | 125.76             | 123.23    | 1.02  |

![Comparison Graph](./images/insertion_graph.png)

**Observation:** As we could see every ratio is in the order of 10, so the Python script values match the corresponding values with YCSB tool.