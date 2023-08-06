# ua-node-avail

A simple script to host on pip to allow the user to analyze the queues for available nodes.

Installation:
```
pip install ua-node-avail
```

Usage:
```
avail_nodes
```

Output:
```
                              CPU CORES                MEMORY GB
  NODE                VENDOR  FREE       ALLOC  TOTAL  FREE       ALLOC  TOTAL

  chpc-compute-12-2   AMD     32         32     64     123        128    251
  chpc-compute-12-8   AMD     32         32     64     123        128    251
  chpc-compute-12-17  AMD     32         32     64     123        128    251
  chpc-compute-12-22  AMD     32         32     64     123        128    251
  chpc-compute-12-24  AMD     32         32     64     133        118    251
  chpc-compute-12-0   AMD     16         48     64     67         184    251
  chpc-compute-12-1   AMD     16         48     64     64         187    251
  chpc-compute-12-3   AMD     16         48     64     64         187    251
  chpc-compute-12-4   AMD     16         48     64     64         187    251
  chpc-compute-12-6   AMD     16         48     64     64         187    251
  chpc-compute-12-7   AMD     16         48     64     67         184    251
  chpc-compute-12-9   AMD     16         48     64     73         178    251
  chpc-compute-12-15  AMD     16         48     64     64         187    251
  chpc-compute-12-16  AMD     16         48     64     64         187    251
  chpc-compute-12-18  AMD     16         48     64     64         187    251
  chpc-compute-12-12  AMD     10         54     64     50         201    251
  chpc-compute-12-10  AMD     0          64     64     14         237    251
  chpc-compute-12-11  AMD     0          64     64     14         237    251
  chpc-compute-12-13  AMD     0          64     64     14         237    251
  chpc-compute-12-14  AMD     0          64     64     10         241    251
  chpc-compute-12-19  AMD     0          64     64     14         237    251
  chpc-compute-12-20  AMD     0          64     64     14         237    251
  chpc-compute-12-21  AMD     0          64     64     10         241    251
  chpc-compute-12-23  AMD     0          64     64     14         237    251
  chpc-gpu-12-1       AMD     64         0      64     251        0      251
  chpc-gpu-10-0       AMD     0          64     64     14         237    251
  chpc-gpu-10-2       AMD     0          64     64     14         237    251
  chpc-gpu-12-0       AMD     0          64     64     14         237    251
  chpc-highmem-12-0   AMD     40         8      48     1906       109    2015
  chpc-highmem-10-0   AMD     0          48     48     15         2000   2015
  chpc-highmem-10-1   AMD     0          48     48     926        1089   2015
  chpc-highmem-12-1   AMD     0          48     48     1411       604    2015
```
