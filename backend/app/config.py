import os

MODEL_NAME = os.getenv("MODEL_NAME", "mistral:7b-instruct")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))