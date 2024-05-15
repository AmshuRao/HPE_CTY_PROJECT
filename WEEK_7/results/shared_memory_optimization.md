# Performance Optimization Using Shared Memory

This method involves configuring the PostgreSQL file to enhance performance, particularly by increasing the number of cache hits in the main memory caches.

## Configuration Changes

Refer to the configuration file for exact changes made in the database. The changes typically involve adjusting shared memory settings. 

### References

1. [Overview of Caching in PostgreSQL](https://severalnines.com/blog/overview-caching-postgresql/)
2. [PostgreSQL Runtime Config Resource Documentation](https://www.postgresql.org/docs/8.4/runtime-config-resource.html)

## Performance Metrics

The table below shows performance metrics for different numbers of batch size and shared memory sizes (keeping 10 lakh tuples in the database):

| Number of Tuples in each batch | Shared Memory Size | Insert (ms) | Delete (ms) | Update (ms) |
|------------------|--------------------|-------------|-------------|-------------|
| 100              | 128 MB             | 172.18      | 488.66      | 4589.2      |
|                  | 8 GB               | 105.52      | 22.88       | 2206.82     |
| 1000             | 128 MB             | 136.57      | 422.75      | 482.004     |
|                  | 8 GB               | 17.25       | 10.66       | 380.79      |
| 10000            | 128 MB             | 13.56       | 132.05      | 220.68      |
|                  | 8 GB               | 6.43        | 3.29        | 46.71       |
| 1 lakh           | 128 MB             | 18.17       | 10.35       | 140.08      |
|                  | 8 GB               | 4.87        | 3.92        | 14.27       |

These metrics showcase the impact of shared memory size on various database operations.
