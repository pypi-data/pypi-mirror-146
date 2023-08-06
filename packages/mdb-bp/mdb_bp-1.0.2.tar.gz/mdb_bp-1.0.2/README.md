# mdb-bp

Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Documentation](#documentation)
- [Example](#example)


This package contains a pure-Python MDB client library.

### Requirements
- Python >= 3.9.0
- [MDB](https://blockpointdb.com/) >= 1.0

### Installation

Package is uploaded on [PyPI](https://pypi.org/project/mdb-bp/0.0.1/).

Install with pip:

```
$ python3 -m pip install mdb-bp
```

### Documentation

bSQL documentation is available online:https://bsql.org/

For support, please refer to [StackOverflow](https://stackoverflow.com/questions/tagged/mdb-bp).

### Example

The following example makes use of a simple blockchain, inserts a value, and reads that value.

```python

from mdb_bp import driver

# Connect to the database
conn = driver.connect(
    username="user",
    password="password",
    connection_protocol="tcp",
    server_address="216.27.61.137",
    server_port=8080,
    database_name="master",
    parameters={"interpolateParams": True},
)

# Prepare a statement
stmt = conn.prepare(
    "CREATE BLOCKCHAIN user TRADITIONAL ("
    + "id uint64 PRIMARY KEY AUTO INCREMENT,"
    + " first_name string size = 25 PACKED,"
    + " last_name string size = 50 PACKED,"
    + " age uint8,"
    + " username string size=30 PACKED UNIQUE)")

# Execute the statement.
resp = stmt.exec()
print(resp)

# Run an insertion and handle error
xact = conn.begin()

# Insert a value non-atomically
try:
    result = xact.exec(
        "INSERT user (first_name, last_name, age, username) "
        + "VALUES (\"it's NOT CHABOY\", \"Smith\", 45, \"NOT CHABOY\")")
    print(result)
    xact.commit()

except Exception as err:
    # Rollback the transaction if there was a failure
    print(err)
    xact.rollback()

# Query from the blockchain
rows = conn.query("SELECT * FROM user")

# Print the rows
itr = iter(rows)

for row in itr:
    print(row)

# Store a file
store_file_resp = conn.store_file(
    "space",
    "test_files/space.png",
    "png"
)
print(store_file_resp)

# Export a file 
export_file_resp = conn.export_file(
    "space",
    "test_files/out_space.png",
    "png"
)
print(export_file_resp)
```

## Resources 
- bSQL documentation: https://bsql.org/
- DB-API 2.0: https://www.python.org/dev/peps/pep-0249/