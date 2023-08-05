from mdb_bp import connect


def test_deserialization():
    print("running test")

    conn = connect(
        username="system",
        password="biglove",
        connection_protocol="tcp",
        server_address="localhost",
        server_port=5461,
        database_name="defi_llama",
        parameters={"interpolateParams": True},
    )

    # rows = conn.query(
    #     "select  p.protocol_id, p.name as protocol_name, sys_timestamp, string(sys_timestamp) from protocol as p filter 5"
    # )
    #
    # print(rows)

    rows = conn.query(
        "select  p.protocol_id, p.name as protocol_name, float32(m.tvl), string(m.tvl) from protocol as p join map_protocol_to_chain as m on m.protocol_id = p.protocol_id where m.primary_chain = true filter 5"
    )

    print(rows)
    # for (row in rows):
    #     row.to
