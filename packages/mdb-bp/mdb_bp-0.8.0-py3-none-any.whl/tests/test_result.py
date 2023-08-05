from mdb_bp import Result


def test_exec_result_basics():
    res = Result.result(10, 3)

    assert res.affected_rows == 10, "incorrect affected rows"
    assert res.insert_id == 3, "incorrect insert id"
