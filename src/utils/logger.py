import logging

# basic logger config
logging.basicConfig(level=logging.INFO)

# make logger so we can use it in other files
logger = logging.getLogger("app")
