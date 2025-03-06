import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('SECRET_KEY'))  # .env に設定した SECRET_KEY が表示されるはず
print(os.getenv('DATABASE_URI')) 