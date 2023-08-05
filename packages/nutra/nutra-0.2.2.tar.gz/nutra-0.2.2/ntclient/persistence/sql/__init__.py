"""Main SQL persistence module, need to rethink circular imports and shared code"""


def sql_entries(sql_result, headers=False):
    """Formats and returns an sql_result for console digestion and output"""
    # TODO: return object: metadata, command, status, errors, etc?
    rows = sql_result.fetchall()
    if headers:
        headers = [x[0] for x in sql_result.description]
        return headers, rows
    return rows


def version(con):
    """Gets the latest entry from version table"""
    cur = con.cursor()
    result = cur.execute("SELECT * FROM version;").fetchall()
    close_con_and_cur(con, cur, commit=False)
    return result[-1][1]


def close_con_and_cur(con, cur, commit=True):
    """Cleans up after a command is run"""
    cur.close()
    if commit:
        con.commit()
    con.close()


def _sql(con, query, db_name, values=None, headers=False):
    from ntclient import DEBUG  # pylint: disable=import-outside-toplevel

    cur = con.cursor()
    if DEBUG:
        print("%s.sqlite: %s" % (db_name, query))
        print(values)
    # TODO: separate `entry` & `entries` entity for single vs. bulk insert?
    if values:
        if isinstance(values, list):
            rows = cur.executemany(query, values)
        else:  # tuple
            rows = cur.execute(query, values)
    else:
        rows = cur.execute(query)
    result = sql_entries(rows, headers=headers)
    close_con_and_cur(con, cur)
    return result
