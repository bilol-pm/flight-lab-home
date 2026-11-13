"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
import argparse
import json
import logging
import os
import sys
from datetime import datetime

from csv_loader import parse_files
from query import run_queries
from validator import load_airports

# TODO: fill in your details: plain ASCII, no spaces or underscores.
STUDENT_ID = "251ADB096"
FIRST_NAME = "Biloliddin"
LAST_NAME = "Gulomov"

def build_parser():
    parser = argparse.ArgumentParser(description="Flight schedule parser and query tool")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="FILE", help="parse a single CSV file")
    source.add_argument("-d", metavar="FOLDER", help="parse every .csv file in a folder")
    source.add_argument("-j", metavar="FILE", help="load an existing JSON database")
    parser.add_argument("-a", metavar="FILE", help="airport list file (with -i or -d)")
    parser.add_argument("-o", metavar="FILE", help="output JSON database (with -i or -d)")
    parser.add_argument("-q", metavar="FILE", help="JSON file with queries")
    parser.add_argument("-r", metavar="FOLDER", default=".", help="folder for the response file")
    return parser

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_database(path):
    data = load_json(path)
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError(f"{path} must contain a JSON array of objects")
    return data

def load_queries(path):
    data = load_json(path)
    if not isinstance(data, (dict, list)):
        raise ValueError(f"{path} must contain a query object or an array of queries")
    return data


def find_csv_files(folder):
    names = sorted(
        name for name in os.listdir(folder)
        if name.endswith(".csv") and os.path.isfile(os.path.join(folder, name))
    )
    if not names:
        raise ValueError(f"no .csv files found in {folder}")
    return [os.path.join(folder, name) for name in names]

def build_database(args):
    db_path = args.o if args.o is not None else "db.json"
    log_path = os.path.join(os.path.dirname(os.path.abspath(db_path)), "errors.log")

    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    try:
        airports = load_airports(args.a)
        paths = [args.i] if args.i is not None else find_csv_files(args.d)
        records, errors = parse_files(paths, airports)
        for message in errors:
            logger.warning(message)
        write_json(db_path, records)
        print(f"{len(records)} valid flights, {len(errors)} invalid rows")
    finally:
        logger.removeHandler(handler)
        handler.close()
    return records

def write_response(db, queries, folder):
    results = run_queries(db, queries)
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    name = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{stamp}.json"
    write_json(os.path.join(folder, name), results)

def run(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.j is None and args.a is None:
        parser.error("-a is required with -i or -d")
    if args.j is not None and args.o is not None:
        parser.error("-o cannot be used with -j")

    try:
        queries = load_queries(args.q) if args.q is not None else None
        if args.j is not None:
            db = load_database(args.j)
        else:
            db = build_database(args)
        if args.q is not None:
            write_response(db, queries, args.r)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0

def main(argv=None):
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    # TODO: parse arguments with argparse (-i, -d, -j, -a, -o, -q, -r).
    # TODO: load or parse the data, write the database and errors.log.
    # TODO: run the queries and write the response file.
    # Remember: remove and close the logging handler before returning,
    # also when returning early because of an error (use try/finally).
    try:
        return run(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 0



if __name__ == "__main__":
    sys.exit(main())
