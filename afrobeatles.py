from dataclasses import dataclass


@dataclass
class Price: 
    id: "price_1MoBy5LkdIwHu7ixZhnattbh"
    nickname: "null"
    currency: "usd"
    unit_amount: 1000
    lookup_key: null

    from dataclasses import dataclass
from models.price import Price


@dataclass
class Product:
    id: "price_1MoBy5LkdIwHu7ixZhnattbh"
    name: "null"
    price: "null"

    from dataclasses import dataclass


@dataclass
class Seller:
    name: str
    email: str
    amount: int

    import json
import os
import stripe
from dataclasses import asdict
from models.product import Product
from models.price import Price

T_SHIRT_PRODUCT_NAME = "The Afrobeatles T-Shirt"
T_SHIRT_PRODUCT_DESC = "Afrobeatles Tour"
T_SHIRT_LOOKUP_KEY = os.getenv("CHALLENGE_ID")
T_SHIRT_URL = os.getenv("CHALLENGE_ID")
T_SHIRT_COST = 2500


def find_product(url):
    """find_product Find existing Product
    Milestone 1
    Args:
        url (string): Unique Url

    Returns:
        product: Product
    """
    stripe_product = None
    # TODO: set stripe_product to an instance of the product model, i.e.
    # stripe_product = Product(<product id>,<name>, <price>)
    return stripe_product


def find_price(product_id, lookup_key):
    """find_price Finds an existing Price with Stripe for the product.
    Milestone 1
    Args:
        product_id (string): Stripe Product Id
        lookup_key (string): Lookup Key

    Returns:
        price: a Price object
    """
    result = None
    # TODO: Returns an instance of the local Price model
    # result = Price(<id>, <nickname>, <currency>, <amount>, <lookup_key>)
    return result


def create_price(product, unit_amount, nickname, lookup_keys):
    """create_price Create Price
    Milestone 1
    We may want to adjust the details of this price over time, without having to change how we refer to it, so use the transfer_lookup_key parameter.
    Args:
        product (string): Product Id
        unit_amount (int): Unit Amount
        nickname (string): Nickname
        lookup_keys (string): lookup_key

    Returns:
        price: Price
    """
    result = Price("id", "nickname", "currency", 2500, "lookup_key")
    # TODO: Return Price
    # Returns an instance of the local Price model
    # result = Price(<id>, <nickname>, <currency>, <amount>, <lookup_key>)
    return result


def create_product(name, description, url):
    """create_product Create a Product with in Stripe
    Milestone 1
    Args:
        name (string): Name
        description (string): Description
        url (string): Url

    Returns:
        product: a Stripe Product
    """
    product = None
    # TODO: Return the Product created in Stripe
    return product


def provision(cache):
    """Create the Product and Price for challenge.
    Leverage Challenge ID as unique URL for the product.
    Leverage Challenge ID as unique lookup key for the price.
    Milestone 1
    """
    try:
        # Clear in-memory cache
        cache.clear()

        # Check if Product exists with correct shape in Stripe Account
        stripe_product = find_product(T_SHIRT_URL)
        price = None
        if stripe_product is not None:
            # Check for Prices
            price = find_price(stripe_product.id, [T_SHIRT_LOOKUP_KEY])

            # Throw error if either Price doesn't exist
            if price is None:
                price = create_price(
                    stripe_product.id,
                    T_SHIRT_COST,
                    T_SHIRT_PRODUCT_NAME,
                    T_SHIRT_LOOKUP_KEY,
                )
        else:
            # Product does not exist in Stripe, create it and its Prices
            stripe_product = create_product(
                T_SHIRT_PRODUCT_NAME, T_SHIRT_PRODUCT_DESC, T_SHIRT_URL
            )
            if stripe_product is not None:
                price = create_price(
                    stripe_product.id,
                    T_SHIRT_COST,
                    T_SHIRT_PRODUCT_NAME,
                    T_SHIRT_LOOKUP_KEY,
                )

        if stripe_product is not None:
            stripe_product.price = asdict(price)

        if price is None or stripe_product is None:
            print("TODO: Implement provisioning service to create a Product & Price")
        else:
            cache.set("product", stripe_product, timeout=10 * 60)
    except Exception:
        print("Error during provisioning")
        raise
        #! /usr/bin/env python3.9

"""
server.py
Associate Developer Challenge
Python 3.9 or newer required.
"""

import json
import os
import stripe
import re
import datetime
import calendar
import logging
from dataclasses import asdict
from itertools import groupby
from models.seller import Seller
from service.provision import provision

from flask import Flask, render_template, request
from dotenv import load_dotenv, find_dotenv
from flask_caching import Cache

if not os.path.exists("./.env"):
    logging.error("Please make sure valid .env file exist in code/server directory.")


load_dotenv(find_dotenv())

static_dir = str(os.path.abspath(os.path.join(__file__, "..", os.getenv("STATIC_DIR"))))

frontend = ""
if os.path.isfile("/".join([static_dir, "index.html"])):
    frontend = "vanilla"
else:
    frontend = "react"
    static_dir = str(os.path.abspath(os.path.join(__file__, "..", "./templates")))

server_dir = str(os.path.abspath(os.path.join(__file__, "../..")))

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

config = {
    "CACHE_TYPE": "SimpleCache",  # caching type
    "CACHE_DEFAULT_TIMEOUT": 300,  # default Cache Timeout
}

app = Flask(
    __name__, static_folder=static_dir, static_url_path="", template_folder=static_dir
)

# Flask to use the above defined config
app.config.from_mapping(config)

cache = Cache(app)
cache.init_app(app)


@app.route("/", methods=["GET"])
def get_main_page():
    """Display langing page"""
    # Display landing page
    if frontend == "vanilla":
        return render_template("index.html")
    else:
        return render_template("react_redirect.html")


@app.route("/signup", methods=["GET"])
def get_signup_page():
    """Display the signup page"""
    # Display signup page
    if frontend == "vanilla":
        return render_template("signup.html")
    else:
        return render_template("react_redirect.html")


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard_page():
    """Display the leaderboard page"""
    # Display leaderboard page
    if frontend == "vanilla":
        return render_template("leaderboard.html")
    else:
        return render_template("react_redirect.html")


@cache.cached(timeout=6000, key_prefix="price")
def get_price_id_from_cache():
    """Get the Price Id of the Product

    Returns:
        string: Price Id from the Cache
    """
    price_id = ""
    # TODO: Integrate Stripe
    return price_id


def validate_email(input_email):
    """Validate the Email Address is valid String format. Use this function to ensure that only one payment link is created per email.

    Args:
        input_email (string): Input Email Address

    Returns:
        boolean: True, if valid Email Format
    """
    mail_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(mail_regex, input_email):
        return True
    else:
        return False


# TODO: Integrate Stripe


@app.route("/create-payment-link", methods=["POST"])
def create_payment_link():
    """Create Stripe Payment Link
    Note:
    Milestone 1: Creating Payment Links
    Validate the Email Address is valid String format.
    After email address validation, create a new Payment Link for the fan, if one does not exists.

    Returns:
        object: Stripe Payment Link
    """
    try:
        payment_link = None
        # TODO: Integrate Stripe
        # returns config information that is used by the client JavaScript to display the page.
        return {
            "paymentLink": payment_link,
        }
    except Exception as e:
        return {"error": str(e)}, 403


@app.route("/leaders", methods=["GET"])
def get_leaders():
    """Get the Leaderboard data leveraging manual pagination of the Checkout sessions to total amount by fan email address
    Note:
    Milestone 2: Leaderboard
    Returns:
        Json Array: seller array with name, email, and total amount that is sorted desc by total amount
    """
    try:
        sellers = []
        # TODO: Integrate Stripe
        # returns config information that is used by the client JavaScript to display the page.
        return {
            "sellers": sellers,
        }

    except Exception as e:
        err_msg = 'Error in GET /leaders: Threw {} with args {}'.format(type(e).__name__, e.args)
        print(err_msg)
        return {"error": err_msg}, 500


# TODO: Integrate Stripe

provision(cache)

if __name__ == "__main__":
    app.run()

    import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.Price.modify(
  "price_1MoBy5LkdIwHu7ixZhnattbh",
  metadata={"order_id": "6735"},
)

import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.Price.retrieve("price_1MoBy5LkdIwHu7ixZhnattbh")

import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.Price.list(limit=3)

import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.Price.search(query="active:'true' AND metadata['order_id']:'6735'")

env
.env
__pycache__

import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.PaymentLink.create(
  line_items=[{"price": "price_1MoC3TLkdIwHu7ixcIbKelAC", "quantity": 1}],
)

import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.PaymentLink.modify(
  "plink_1MoC3ULkdIwHu7ixZjtGpVl2",
  metadata={"order_id": "6735"},
)
import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.PaymentLink.list_line_items("plink_1N4CWjLkdIwHu7ix2Y2F1kqb")
import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.PaymentLink.retrieve("plink_1MoC3ULkdIwHu7ixZjtGpVl2")

import stripe
stripe.api_key = "sk_test_51Q7DpLBAfCTkZVSmRBe0avcutoXqCyfwRwCLRJfOQ4XYrvB9HFqG5bRvbDaZSSnoc3PRry48G4zMKYOhXTf4Gavb00BXdJtTr2"

stripe.PaymentLink.list(limit=3)

## Running the test suite

1. From this directory, run `npm i` to install Playwright's npm dependencies.
2. Run `npx playwright install --with-deps chromium` to install Playwright's copy of Chromium.
3. Check the current milestone's pull request to find the command to run its test suite.


Note: Playwright installs browsers into a shared system directory by default.  If you can only run programs from a specific directory, then you can tell Playwright to install browsers within this project by setting the following environment variable before running the commands above: `export PLAYWRIGHT_BROWSERS_PATH=0`.