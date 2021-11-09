import os
# enable tensorflow logging if LOG_LEVEL is DEBUG
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' if os.getenv("LOG_LEVEL", "INFO") == "DEBUG" else "2"
