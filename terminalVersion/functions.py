import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import base64
import time
from colorama import Fore, Style




# This function will handle website creation; it should perform actual file writing in a real-world scenario.
def create_website(html_code, css_code, js_code=None):
    # Perform the desired action (e.g., create files). For now, it just prints information as an example.

    # Check and see if the directory exists. If not, create it.
    if not os.path.exists("website"):
        os.makedirs("website")

    # Create the HTML file.
    html_file = open("website/index.html", "w")
    html_file.write(html_code)
    html_file.close()

    # Create the CSS file.
    css_file = open("website/style.css", "w")
    css_file.write(css_code)
    css_file.close()

    # Create the JS file if it exists.
    if js_code:
        js_file = open("website/script.js", "w")
        js_file.write(js_code)
        js_file.close()

    # Return a message to the user.
    return "Website created successfully!, files are in the website folder, (index.html, style.css, script.js) "

def webpageImageRender():
    # Set up the ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Headless mode means the browser window will not be shown
    service = Service(ChromeDriverManager().install())

    # Initialize the browser
    browser = webdriver.Chrome(service=service, options=options)

    # Open your local HTML file. relative to the directory you're running this script from. websites/index.html
    path = os.path.abspath("website/index.html")
    url = 'file://' + path
    browser.get(url)

    # Give the page some time to render JavaScript, if needed
    time.sleep(2)  # waits for 2 seconds

    # Calculate the total height of the webpage
    total_height = browser.execute_script("return document.body.parentNode.scrollHeight")

    # Scroll to the end of the webpage to ensure all lazy-loaded elements are loaded
    browser.execute_script("window.scrollTo(0, document.body.parentNode.scrollHeight)")

    # Give the page some time to load any lazy-loaded elements
    time.sleep(1)  # waits for 2 seconds

    # Change the size of the window to the full height of the page
    browser.set_window_size(1200, total_height)  # Width is set to 1200px, or whatever is required

    # Take a screenshot of the entire page
    browser.save_screenshot('websiteSaved.png')

    # Close the browser
    browser.quit()

    return "websiteSaved.png"

def convertImageFileToBase64String(pictureFilename):
    with open(pictureFilename, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def communications(agent, message, autoOrcomms):
    if autoOrcomms == "auto":
        if agent == "PromptAI":
            print(Fore.RED + f"{agent}: <A>" + Style.RESET_ALL + Fore.LIGHTBLACK_EX + f" {message}" + Style.RESET_ALL)
        elif agent == "CodingAI":
            print(Fore.GREEN + f"{agent}: <A>" + Style.RESET_ALL + Fore.LIGHTBLACK_EX + f" {message}" + Style.RESET_ALL)
        elif agent == "Function":
            print(Fore.YELLOW + f"{agent}: <A>" + Style.RESET_ALL + Fore.LIGHTBLACK_EX + f" {message}" + Style.RESET_ALL)
    
    else:
        if agent == "PromptAI":
            print(Fore.RED + f"{agent}: <A>" + Style.RESET_ALL + Fore.LIGHTBLUE_EX + f" {message}" + Style.RESET_ALL)
        elif agent == "CodingAI":
            print(Fore.GREEN + f"{agent}: <A>" + Style.RESET_ALL + Fore.LIGHTBLUE_EX + f" {message}" + Style.RESET_ALL)
        elif agent == "Function":
            print(Fore.YELLOW + f"{agent}: <A>" + Style.RESET_ALL + Fore.LIGHTBLUE_EX + f" {message}" + Style.RESET_ALL)