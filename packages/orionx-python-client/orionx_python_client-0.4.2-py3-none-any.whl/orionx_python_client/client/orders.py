import asyncio
import json
import logging


from typing import List, Dict
from ..currency import CEROS
from ..queries import get_cancel_order_query, get_open_orders_query, get_new_position_query, get_cancel_multiple_orders_query, get_order_status_query


def close_order_by_id(self, order_id: str):
    try:
        logging.info(f"Closing Order {order_id}")
        query_str = get_cancel_order_query(order_id=order_id)
        payload = {"query": query_str, "variables": {}}
        response = self.post(path="graphql", payload=payload)
        logging.info(response)
        logging.info(type(response))

        if response["data"].get("cancelOrder", None) == None:
            error_code = response["errors"][0]["details"]["code"]

            if error_code == "concurrent":
                logging.debug(f"Repeated attempt to close {order_id}. ")
                return True

            else:
                logging.debug(error_code)
                return False

        else:
            status = response["data"]["cancelOrder"].get("status")
            if status != "open":
                logging.debug(f"ORder ID {order_id} was closed.")
                return True
            else:
                logging.debug(
                    f"Order ID {order_id}  COULD NOT BE CLOSED closed.")
                return False

    except Exception as err:
        logging.error(err)
        return False


def get_open_orders(self):
    try:
        query_str = get_open_orders_query()
        payload = {"query": query_str, "variables": {}}
        response = self.post(path="graphql", payload=payload)
        logging.info(response)

        if "data" in response:
            ids = {
                order["_id"]: order["market"]["code"]
                for order in response["data"]["orders"]["items"]
            }
            logging.info(f"OPEN ORDERS: {ids}")
            return ids
        return []
    except Exception as err:
        logging.error(err)
        raise Exception("Could not get open ids")


def get_open_orders_by_market(
    self, selling: str, market: str
):
    try:
        query_str = get_open_orders_query()
        payload = {"query": query_str, "variables": {}}
        response = self.post(path="graphql", payload=payload)
        logging.info(response)

        if "data" in response:
            ids = {
                order["_id"]: order["market"]["code"]
                for order in response["data"]["orders"]["items"]
                if order["market"]["code"] == market.replace("/", "")
                and order["sell"] == selling
            }
            logging.info(f"OPEN ORDERS in {market}: {ids}")
            return ids
        return []
    except Exception as err:
        logging.error(err)
        raise Exception(f"Could not get open ids for market {market}")


def close_orders_by_market(self, market: str, selling: str):
    try:
        logging.info(f"CLOSING ORDERS BY {market}")
        market_orders = self.get_open_orders_by_market(
            market=market, selling=selling
        )
        self.close_orders(list(market_orders.keys()))
    except Exception as err:
        logging.error(err)
        raise err


def get_order_status(self, order_id: str):
    try:
        query_str = get_order_status_query(order_id=order_id)
        payload = {"query": query_str, "variables": {}}
        response = self.post(path="graphql", payload=payload)
        logging.debug(response)

        if "errors" in response:
            logging.debug(response)
            raise Exception("Errors in Get Status Status")

        if "data" in response:
            status = response["data"]["order"]["status"]
            return status
        return None
    except Exception as err:
        logging.error(err)
        logging.error("Could not get Order Status")
        return None


def close_orders(self, order_ids: List[str]):
    try:
        logging.info(f"CLOSING ORDERS: {order_ids}")
        if order_ids:
            str_ids = json.dumps(order_ids)
            query_str = get_cancel_multiple_orders_query(str_ids=str_ids)
            payload = {"query": query_str, "variables": {}}
            response = self.post(path="graphql", payload=payload)
            logging.debug(response)
            if 'errors' in response:
                return None

            return response
        else:
            return None
    except Exception as err:
        logging.error(err)
        raise Exception(
            "OrionXExchange Error: Could not close orders  {order_ids}")


def new_position(
    self,
    market_code: str,
    amount: float,
    limit_price: float,
    selling: str,
    ceros_map: Dict=CEROS

):
    try:
        first_currency_code, second_currency_code = market_code.split("/")

        logging.info(
            f"\n\tPlacing New Order {first_currency_code}{second_currency_code}. Selling: {selling}")
        limit_price = limit_price * 10 ** ceros_map[second_currency_code]
        amount = amount * 10 ** ceros_map[first_currency_code]
        logging.info(f"\t\tLimit Price: {limit_price}")
        logging.info(f"\t\tAmount: {amount}")

        query_place_order = get_new_position_query(
            market_code=market_code.replace("/", ""),
            amount=amount,
            limit_price=limit_price,
            selling=selling,
        )

        payload = {"query": query_place_order, "variables": {}}
        response = self.post(path="graphql", payload=payload)
        logging.info(response)

        if response["data"].get("errors", None) != None:

            error_code = response["errors"][0]["details"]["code"]

            logging.debug(
                f"Failed Order: {amount} {market_code} at {limit_price}. {error_code}"
            )
            if error_code == "insufficientFunds":
                return False
            elif error_code == "amountIsLow":
                return False
            elif error_code == "concurrent":
                return False
            else:
                return False

        if response["data"].get("placeLimitOrder", None) == None:

            return False
        else:
            order_id = response["data"].get("placeLimitOrder")["_id"]
            logging.info(
                f"ORDER {order_id} created for market {market_code}. Amount: {amount}, Limit Price: {limit_price}. Selling: {selling}"
            )
            return order_id
    except Exception as err:
        logging.error(err)
        raise err
