# This files contains your custom actions which can be used to run
# custom Python code.

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from transformers import pipeline
from sqlite3 import Error
from .utils import DatabaseUtility


def ordinal_to_index(ordinal: str) -> int:
    """Convert ordinal string to a zero-based index."""
    ordinals = {"first": 0, "second": 1, "third": 2, "fourth": 3, "fifth": 4}
    return ordinals.get(ordinal.lower(), -1)


class AnalyzeFeedback(Action):
    def name(self):
        return "action_analyze_feedback"

    def run(self, dispatcher, tracker, domain):
        sentiment_pipeline = pipeline('sentiment-analysis')
        feedback_text = tracker.latest_message['text']
        result = sentiment_pipeline(feedback_text)
        sentiment = result[0]['label']
        response = "Yay! I'm glad I could help!" if sentiment == "POSITIVE" else ("I'm sorry to hear that. I will try "
                                                                                  "better next time.")
        dispatcher.utter_message(text=response)
        return []


class SearchProductsAction(Action):
    def name(self) -> Text:
        return "action_search_products"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = DatabaseUtility.create_connection()
        product_type = tracker.get_slot("ProductCategory")
        query = '''SELECT * FROM product_search WHERE product_search MATCH ? LIMIT 5;'''
        top_products = DatabaseUtility.execute_query(conn, query, (product_type,))
        if top_products:
            response = "Here are the top 5 products matching your search:\n\n" + "\n".join(
                f"{index}. {product[0]}" for index, product in enumerate(top_products, start=1))
        else:
            response = "Sorry, I couldn't find any products matching your search criteria."
        dispatcher.utter_message(text=response)
        product_details = {"slot_name": [product[0] for product in top_products],
                           "slot_description": [product[1] for product in top_products],
                           "slot_price": [str(product[5]) for product in top_products],
                           "slot_weight": [str(product[6]) for product in top_products],
                           "slot_dimensions": [product[7] for product in top_products]}
        return [SlotSet(slot, value) for slot, value in product_details.items()]



class ActionShowProductDetails(Action):
    def name(self) -> Text:
        return "action_show_product_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the ordinal product number from the slot
        ordinal_number = tracker.get_slot("ProductNumber")
        product_index = ordinal_to_index(ordinal_number)
        # Retrieve the list of presented products
        products = tracker.get_slot("slot_description")

        # Use the index to get the product name
        product_description = products[product_index]

        if product_description:
            dispatcher.utter_message(text=product_description)
        else:
            dispatcher.utter_message(text="I couldn't find details for that product.")

        return []


class ActionShowProductPrice(Action):
    def name(self) -> Text:
        return "action_show_product_price"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        ordinal_number = tracker.get_slot("ProductNumber")
        product_index = ordinal_to_index(ordinal_number)

        # Retrieve the list of presented products
        products = tracker.get_slot("slot_price")

        # Use the index to get the product name
        product_price = products[product_index]

        if product_price:
            dispatcher.utter_message(text=f"{product_price}$")
        else:
            dispatcher.utter_message(text="I couldn't find the price for that product.")

        return []


class ActionShowProductWeight(Action):
    def name(self) -> Text:
        return "action_show_product_weight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the ordinal product number from the slot
        ordinal_number = tracker.get_slot("ProductNumber")
        product_index = ordinal_to_index(ordinal_number)

        # Retrieve the list of presented products
        products = tracker.get_slot("slot_weight")

        # Use the index to get the product name
        product_weight = products[product_index]

        if product_weight:
            dispatcher.utter_message(text=f"{product_weight} pounds")
        else:
            dispatcher.utter_message(text="I couldn't find the weight for that product.")

        return []


class ActionShowProductDimensions(Action):
    def name(self) -> Text:
        return "action_show_product_dimensions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the ordinal product number from the slot
        ordinal_number = tracker.get_slot("ProductNumber")
        product_index = ordinal_to_index(ordinal_number)

        # Retrieve the list of presented products
        products = tracker.get_slot("slot_dimensions")

        # Use the index to get the product name
        product_dimensions = products[product_index]

        if product_dimensions:
            dispatcher.utter_message(text=product_dimensions)
        else:
            dispatcher.utter_message(text="I couldn't find the weight for that product.")

        return []

