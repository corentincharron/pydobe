import logging


_format = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

logger = logging.getLogger("pydobe")

# Stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(_format)
logger.addHandler(stream_handler)

# File handler
file_handler = logging.FileHandler('pydobe.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(_format)
logger.addHandler(file_handler)

