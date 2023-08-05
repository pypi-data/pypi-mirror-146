from mdb_bp import connect


def test_store_file():
    conn = connect(
        username="system",
        password="biglove",
        connection_protocol="tcp",
        server_address="localhost",
        server_port=5461,
        database_name="defi_llama",
        parameters={"interpolateParams": True},
    )

    # resp = conn.exec("use defi_llama")
    # print(resp)

    file_resp = conn.store_file(
        "space",
        "test_files/space.png",
        "png"
    )
    print(file_resp)

def test_export_file():
    conn = connect(
        username="system",
        password="biglove",
        connection_protocol="tcp",
        server_address="localhost",
        server_port=5461,
        database_name="defi_llama",
        parameters={"interpolateParams": True},
    )

    # resp = conn.exec("use defi_llama")
    # print(resp)

    file_resp = conn.export_file(
        "space",
        "test_files/out_space.png",
        "png"
    )
    print(file_resp)
