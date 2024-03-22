import sqlite3
import pandas as pd


def create_database(csv_file_path, db_name):
    """
    Creates a SQLite database from a CSV file.

    """

    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()
    conn = sqlite3.connect(db_name)
    df.to_sql('products', conn, if_exists='replace')
    conn.close()


def create_search_table(db_name):
    """
    Creates a virtual table for full-text search in the SQLite database.

    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Uncomment the next line if you need to drop the existing virtual table and recreate it
    # c.execute('''DROP TABLE IF EXISTS product_search;''')

    # Create the virtual table for full-text search
    c.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS product_search USING fts5(
            "product_name", "about_product", "main_category", "subcategory_1",
            "subcategory_2", "selling_price","shipping_weight","product_dimensions",content="products"
        )
    ''')

    conn.commit()

    # Rebuild the FTS5 index for the virtual table from the content table
    c.execute("INSERT INTO product_search(product_search) VALUES('rebuild');")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    csv_file_path = r'C:\Users\User-PC\PycharmProjects\rasa_test\EcommerceChatbot\chatbot_db\cleaned_data.csv'
    db_name = 'testdatabase.db'

    create_database(csv_file_path, db_name)
    create_search_table(db_name)
