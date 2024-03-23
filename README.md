# Overview
This project is an implementation of a conversational chatbot for e-commerce platforms. It's built using 
he Rasa framework and utilizes custom actions in Python for dynamic interactions with users. The chatbot is capable of searching products(by category), providing product details, and analyzing user feedback using sentiment analysis.

# Features 
- **Product Search**: Users can inquire about products in various categories. The chatbot searches for relevant products and presents a list of options.
- **Product Details**: Upon request, the chatbot provides detailed information about products, including descriptions, prices, weights, and dimensions.
- **Sentiment Analysis**: User feedback is analyzed for sentiment, allowing for more nuanced responses and future improvements.

# Installation 
- Python 3.8, 3.9 or 3.10
- Rasa 2.0 or higher
- Transformers library
- SQLite

# Setup
1. Clone the repository to your local machine.
2. Train the Rasa model with rasa train.
3. Start the action server with rasa run actions.
4. In a new terminal, launch the Rasa shell with rasa shell to interact with the chatbot.

# Files and Directories
- actions.py: Contains custom actions to perform tasks like product search, details retrieval, and feedback analysis.
- utils.py: Includes utility functions for database operations, such as connecting to the SQLite database and executing queries.
- db_utils.py: Scripts for setting up the database, including creating a database from a CSV file and setting up a full-text search table.
- nlu: Defines the NLU model for understanding user intents and extracting entities.
- stories: Provides example conversation paths that the bot can handle.
- domain: Specifies the chatbot's domain, including intents, entities, responses, and actions.

# Database Setup
Before running the chatbot, ensure the SQLite database is set up correctly. Run db_utils.py with the appropriate CSV file path to create the database and prepare it for product searches.

![Product Image](https://github.com/199406/simple_rasa_chatbot/blob/main/1.JPG)

