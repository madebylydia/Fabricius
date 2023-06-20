import logging

# These logs are not available in the terminal but rather in the HTML output.
logging.root.setLevel(0)
logging.root.addHandler(logging.StreamHandler())
