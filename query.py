"""Running queries against the flight database."""
from validator import parse_datetime

STRING_KEYS = {"flight_id", "origin", "destination"}
DATETIME_KEYS = {"departure_datetime", "arrival_datetime"}
NUMBER_KEYS = {"price", "min_price"}
SORT_KEYS = {"flight_id", "origin", "destination",
             "departure_datetime", "arrival_datetime", "price"}


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_valid_query(query):
    if not isinstance(query, dict):
        return False
    for key, value in query.items():
        if key in STRING_KEYS:
            if not isinstance(value, str):
                return False
        elif key in DATETIME_KEYS:
            if not isinstance(value, str) or parse_datetime(value) is None:
                return False
        elif key in NUMBER_KEYS:
            if not is_number(value):
                return False
        elif key == "sort_by":
            if not isinstance(value, str) or value not in SORT_KEYS:
                return False
        elif key == "order":
            if value not in ("asc", "desc"):
                return False
        elif key == "limit":
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                return False
        else:
            return False
    if "order" in query and "sort_by" not in query:
        return False
    return True


def matches(flight, query):
    for key in ("flight_id", "origin", "destination"):
        if key in query and flight[key] != query[key]:
            return False
    if "departure_datetime" in query and flight["departure_datetime"] < query["departure_datetime"]:
        return False
    if "arrival_datetime" in query and flight["arrival_datetime"] > query["arrival_datetime"]:
        return False
    if "price" in query and flight["price"] > query["price"]:
        return False
    if "min_price" in query and flight["price"] < query["min_price"]:
        return False
    return True

def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object.

    Valid query:   {"query": query, "matches": [...]}
    Invalid query: {"query": query, "error": "INVALID_QUERY", "matches": []}
    """
    if not is_valid_query(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}
    result = [flight for flight in db if matches(flight, query)]
    if "sort_by" in query:
        result = sorted(result,
                        key=lambda flight: flight[query["sort_by"]],
                        reverse=query.get("order", "asc") == "desc")
    if "limit" in query:
        result = result[:query["limit"]]
    return {"query": query, "matches": result}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of them; always return a list."""
    if isinstance(queries, dict):
        queries = [queries]
    return [run_query(db, query) for query in queries]
