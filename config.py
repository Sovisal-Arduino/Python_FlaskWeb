import os
# Correct import statement (fixing the typo)
from dotenv import load_dotenv  # Correct import statement

load_dotenv()

class Config:  # Class name should be capitalized by convention
    SECRET_KEY = os.getenv("SECRET_KEY") or "your-secret-key-here"  # Fixed typo in variable name