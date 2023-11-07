import os

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
    return "Website created successfully!"