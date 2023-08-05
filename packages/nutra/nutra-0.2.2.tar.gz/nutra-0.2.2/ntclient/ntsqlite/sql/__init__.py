#!/usr/bin/env python3
"""Main module for building nt.sqlite"""

import csv
import os
import sqlite3

NT_DB_NAME = "nt.sqlite"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def build_ntsqlite(verbose=False):
    """Builds and inserts stock data into nt.sqlite"""
    # cd into this script's directory
    os.chdir(SCRIPT_DIR)

    if verbose:
        print("Cleanup...")
    if os.path.isfile(NT_DB_NAME):
        os.remove(NT_DB_NAME)

    if verbose:
        print("\nPack %s" % NT_DB_NAME)
    con = sqlite3.connect(NT_DB_NAME)
    cur = con.cursor()

    if verbose:
        print("\n-> Create tables")
    with open("tables.sql", encoding="utf-8") as tables:
        cur.executescript(tables.read())

    if verbose:
        print("-> Populate data")
    for file_path in os.listdir("data"):
        if not file_path.endswith(".csv"):
            continue
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        file_path_full = os.path.join("data", file_path)

        # Loop over CSV files
        with open(file_path_full, encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            values = ",".join("?" * len(reader.fieldnames))
            reader = csv.reader(csv_file)
            query = "INSERT INTO {0} VALUES ({1});".format(  # nosec: B608
                table_name, values
            )
            cur.executemany(query, reader)

    cur.close()
    con.commit()
    con.close()
    if verbose:
        print("\nDone!")
    return True


if __name__ == "__main__":
    build_ntsqlite(verbose=True)
