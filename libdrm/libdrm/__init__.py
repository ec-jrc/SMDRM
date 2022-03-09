from .__version__ import __version__

# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
import logging

logging.getLogger("libdrm").addHandler(logging.NullHandler())
