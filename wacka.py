# import necessary libraries
from lxml import html
import requests
import json
import logging

# Configure basic logger with level set to ERROR
logging.basicConfig(level=logging.ERROR)

def extract_joke(id):
    """
    Function to download and parse a single joke.
    
    Parameters:
    id (int): ID of the joke to fetch
    """
    # Base URL for the joke site
    url_base = "http://www.wocka.com/{}.html"
    
    # Request the page
    response = requests.get(url_base.format(id))
    
    # Parse the HTML of the page
    tree = html.fromstring(response.content)
    
    # Extract the joke's 'content' div
    content = tree.xpath('//div[@id="content"]')[0]
    
    # Extract the h2 title from the 'content' div
    h2s = tree.xpath('//div[@id="content"]/h2')
    
    # Extract the 'Category' row from the 'content' div
    category_rows = content.xpath('./div[@class="right"]//tr/td/b[text()="Category"]/../..')
    
    # Remove all the HTML nodes in 'content' that are not plaintext or 'br'
    unwanted_nodes = tree.xpath('//div[@id="content"]/child::node()[not(self::text()) and not(self::br)]')

    for node in unwanted_nodes:
        content.remove(node)

    # Extract and clean the joke body
    body_text = content.text_content().strip()

    # Check if the joke does not exist or is dirty and need signup to be accessed
    if body_text in ["This joke does not exist", "This is a dirty joke, so it has been hidden.  To read this joke, you will need to create an account and signin."]:
        return None, body_text, None

    # Extract the category of the joke
    category = category_rows[0].xpath('./td/a/text()')[0]

    # Extract the joke title  
    title = h2s[0]
    joke_title = title.text_content()

    # Return joke details
    return joke_title, body_text, category

if __name__ == "__main__":
    """
    Driver method to handle joke extraction and saving to json file.
    """

    # List to store joke objects
    jokes = []

    # Save to file after every 100 jokes fetched
    save_frequency = 100 

    # Maximum id 
    max_id = 19000

    # Iterate over specific range of IDs
    for id in range(500, 530): 
        try:
            # Extract joke details
            title, body, category = extract_joke(id)

            # If joke title is none, continue to next iteration
            if title is None:
                print("ID {} {}.".format(id, body))
                continue

            # Create joke object and append to list
            joke = {"id": id, "category": category, "title": title, "body": body}
            jokes.append(joke)
            print("ID {} [{}] {}".format(id, title, body))
        except Exception as ex:
            # Exception handling
            print("ID {} failed: ".format(id))
            logging.error(ex)

        # Save jokes to json file every save_frequency jokes, or at the max id
        if id % save_frequency == 0 or id == max_id:
            with open("wocka.json", "w") as f:
                json.dump(jokes, f, indent=4, sort_keys=True)
