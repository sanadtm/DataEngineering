# this program loads Census ACS data using basic, slow INSERTs 
# run it with -h to see the command line options

import time
import psycopg2
import argparse
import re
import csv

DBname = "postgres"
DBuser = "postgres"
DBpwd = "qwerty"   # replace with your PostgreSQL password
TableName = 'CensusData'
Datafile = "filedoesnotexist"
CreateDB = False

def initialize():
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--datafile", required=True)
  parser.add_argument("-c", "--createtable", action="store_true")
  args = parser.parse_args()
  global Datafile, CreateDB
  Datafile = args.datafile
  CreateDB = args.createtable

def dbconnect():
  return psycopg2.connect(host="localhost", database=DBname, user=DBuser, password=DBpwd)

def createTable(conn):
  with conn.cursor() as cursor:
    cursor.execute(f"""
      DROP TABLE IF EXISTS {TableName};
      CREATE TABLE {TableName} (
        TractId NUMERIC,
        State TEXT,
        County TEXT,
        TotalPop INTEGER,
        Men INTEGER,
        Women INTEGER,
        Hispanic DECIMAL,
        White DECIMAL,
        Black DECIMAL,
        Native DECIMAL,
        Asian DECIMAL,
        Pacific DECIMAL,
        VotingAgeCitizen DECIMAL,
        Income DECIMAL,
        IncomeErr DECIMAL,
        IncomePerCap DECIMAL,
        IncomePerCapErr DECIMAL,
        Poverty DECIMAL,
        ChildPoverty DECIMAL,
        Professional DECIMAL,
        Service DECIMAL,
        Office DECIMAL,
        Construction DECIMAL,
        Production DECIMAL,
        Drive DECIMAL,
        Carpool DECIMAL,
        Transit DECIMAL,
        Walk DECIMAL,
        OtherTransp DECIMAL,
        WorkAtHome DECIMAL,
        MeanCommute DECIMAL,
        Employed INTEGER,
        PrivateWork DECIMAL,
        PublicWork DECIMAL,
        SelfEmployed DECIMAL,
        FamilyWork DECIMAL,
        Unemployment DECIMAL
      );
    """)
    print(f"Created {TableName}")

def clean_csv(original, cleaned):
  with open(original, "r") as infile, open(cleaned, "w", newline='') as outfile:
    dr = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=dr.fieldnames)
    writer.writeheader()
    for row in dr:
      for k in row:
        if row[k] == "":
          row[k] = "0"
        if k == "County":
          row[k] = row[k].replace("'", "")
      writer.writerow(row)

def load_with_copy_from(conn, cleaned_file):
  with conn.cursor() as cursor:
    print(f"Loading using copy_from from: {cleaned_file}")
    start = time.perf_counter()
    with open(cleaned_file, 'r') as f:
      next(f)
      cursor.copy_expert(f"COPY {TableName} FROM STDIN WITH CSV", f)
    conn.commit()
    elapsed = time.perf_counter() - start
    print(f"Finished Loading. Elapsed Time: {elapsed:.2f} seconds")

def addConstraintsAndIndexes(conn):
  with conn.cursor() as cursor:
    cursor.execute(f"ALTER TABLE {TableName} ADD PRIMARY KEY (TractId);")
    cursor.execute(f"CREATE INDEX idx_{TableName}_State ON {TableName}(State);")
    print("Added constraints and indexes.")

def main():
  initialize()
  conn = dbconnect()
  if CreateDB:
    createTable(conn)
  cleaned = "cleaned_data.csv"
  clean_csv(Datafile, cleaned)
  load_with_copy_from(conn, cleaned)
  if CreateDB:
    addConstraintsAndIndexes(conn)

if __name__ == "__main__":
  main()
