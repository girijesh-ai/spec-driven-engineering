#!/usr/bin/env bash
# Shop pricing. Branch `feature` changes get_price to return a dict instead
# of integer cents and updates cart.py, but invoice.py, a caller the commit
# doesn't touch, still divides the result by 100: TypeError on every invoice.
# The suite only tests the cart, so it stays green on both branches.
set -euo pipefail
git init -q
git checkout -q -b main
mkdir -p app tests
printf '__pycache__/\n' > .gitignore

cat > README.md <<'MD'
# shop

Prices, carts and invoices for a small web shop. One process, a few
hundred orders a day.

Run the tests: `python3 -m unittest -q`
MD

cat > app/__init__.py <<'PY'
PY

cat > app/pricing.py <<'PY'
PRICES_CENTS = {"mug": 1200, "shirt": 2500}


def get_price(sku):
    return PRICES_CENTS[sku]
PY

cat > app/cart.py <<'PY'
from app.pricing import get_price


def cart_total_cents(skus):
    return sum(get_price(sku) for sku in skus)
PY

cat > app/invoice.py <<'PY'
from app.pricing import get_price


def invoice_line(sku, quantity):
    unit = get_price(sku) / 100
    return f"{sku} x{quantity}: {unit * quantity:.2f} EUR"
PY

cat > tests/__init__.py <<'PY'
PY
cat > tests/test_cart.py <<'PY'
import unittest

from app.cart import cart_total_cents


class CartTest(unittest.TestCase):
    def test_total_adds_prices(self):
        self.assertEqual(cart_total_cents(["mug", "shirt"]), 3700)
PY

git add -A
git -c user.name=eval -c user.email=eval@example.com commit -q -m "shop: prices, cart, invoice"

git checkout -q -b feature
cat > app/pricing.py <<'PY'
PRICES_CENTS = {"mug": 1200, "shirt": 2500}


def get_price(sku):
    return {"cents": PRICES_CENTS[sku], "currency": "EUR"}
PY
cat > app/cart.py <<'PY'
from app.pricing import get_price


def cart_total_cents(skus):
    return sum(get_price(sku)["cents"] for sku in skus)
PY
git add -A
git -c user.name=eval -c user.email=eval@example.com commit -q -m "pricing: return currency with the price"
