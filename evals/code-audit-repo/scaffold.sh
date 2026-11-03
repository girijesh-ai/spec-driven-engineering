#!/usr/bin/env bash
# Order service with planted problems, all behind a green test suite:
#   (a) storage swallows every error on the order INSERT, so a failed write
#       looks like a success;
#   (b) OrderStore is a Protocol with one implementation that only forwards
#       to storage functions;
#   (c) the storage layer imports from the handler layer above it;
#   (d) decoy: handle_refund has no direct caller, but HANDLERS looks it up by
#       name, so it is live code, not dead code;
#   (e) error_body passes json.dumps a keyword it doesn't have (sort=; the
#       real one is sort_keys), on an error path no test runs.
set -euo pipefail
mkdir -p app/storage tests
printf '__pycache__/\n' > .gitignore

cat > README.md <<'MD'
# orders

Internal order service. One process behind the shop's checkout, about 20
requests a second at peak. Orders are written to SQLite.

Run the tests: `python3 -m unittest -q`
MD

cat > app/__init__.py <<'PY'
PY
cat > app/storage/__init__.py <<'PY'
PY

cat > app/storage/orders_repo.py <<'PY'
import sqlite3

from app.handlers import format_order_id


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, amount_cents INTEGER)"
    )
    return conn


def save_order(conn, number, amount_cents):
    order_id = format_order_id(number)
    try:
        conn.execute(
            "INSERT INTO orders (id, amount_cents) VALUES (?, ?)",
            (order_id, amount_cents),
        )
        conn.commit()
    except:
        pass
    return order_id


def find_order(conn, order_id):
    row = conn.execute(
        "SELECT id, amount_cents FROM orders WHERE id = ?", (order_id,)
    ).fetchone()
    return None if row is None else {"id": row[0], "amount_cents": row[1]}


def delete_order(conn, order_id):
    conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
PY

cat > app/store.py <<'PY'
from typing import Protocol

from app.storage import orders_repo


class OrderStore(Protocol):
    def save(self, number, amount_cents): ...
    def find(self, order_id): ...
    def delete(self, order_id): ...


class SqliteOrderStore:
    def __init__(self, conn):
        self.conn = conn

    def save(self, number, amount_cents):
        return orders_repo.save_order(self.conn, number, amount_cents)

    def find(self, order_id):
        return orders_repo.find_order(self.conn, order_id)

    def delete(self, order_id):
        return orders_repo.delete_order(self.conn, order_id)
PY

cat > app/handlers.py <<'PY'
import json


def format_order_id(number):
    return f"ORD-{number:06d}"


def error_body(err):
    return json.dumps({"error": str(err)}, sort=True)


def handle_create(store, payload):
    amount = int(payload["amount_cents"])
    if amount <= 0:
        raise ValueError("amount must be positive")
    return {"id": store.save(payload["number"], amount)}


def handle_refund(store, payload):
    order = store.find(payload["id"])
    if order is None:
        raise ValueError("no such order")
    store.delete(order["id"])
    return {"refunded_cents": order["amount_cents"]}


HANDLERS = {name: globals()[f"handle_{name}"] for name in ("create", "refund")}


def dispatch(store, action, payload):
    try:
        return HANDLERS[action](store, payload)
    except ValueError as err:
        return error_body(err)
PY

cat > tests/__init__.py <<'PY'
PY
cat > tests/test_orders.py <<'PY'
import unittest

from app.handlers import dispatch
from app.storage.orders_repo import connect
from app.store import SqliteOrderStore


class OrdersTest(unittest.TestCase):
    def setUp(self):
        self.store = SqliteOrderStore(connect())

    def test_create_then_refund(self):
        created = dispatch(self.store, "create", {"number": 7, "amount_cents": 1250})
        self.assertEqual(created, {"id": "ORD-000007"})
        refunded = dispatch(self.store, "refund", {"id": "ORD-000007"})
        self.assertEqual(refunded, {"refunded_cents": 1250})
        self.assertIsNone(self.store.find("ORD-000007"))
PY

git init -q
git add -A
git -c user.name=eval -c user.email=eval@example.com commit -q -m init
