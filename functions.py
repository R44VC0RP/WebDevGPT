import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



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

    # Open your local HTML file
    browser.get("file://website/index.html")

    # Give the page some time to render JavaScript, if needed
    browser.implicitly_wait(2)  # waits for 10 seconds

    # Take a screenshot
    browser.save_screenshot('websiteSaved.png')

    # Close the browser
    browser.quit()

    return "Image saved successfully!, file is, (websiteSaved.png) "