import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Install dependencies - install once, do not need to run after first time
# os.system("pip install -r requirements.txt")

user_file=os.getenv('USER_FILE')
user_address=os.getenv('USER_ADDRESS')
user_port=os.getenv('USER_PORT')

if not all([user_file, user_address, user_port]):
  print('Error: One or more required environment variables are not set')
  exit(1)

command = ["streamlit", "run", f"{user_file}.py", f"--server.port={user_port}", f"--server.address={user_address}"]
# Run the Streamlit app
try:
  subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
  print(f'Error running Streamlit: {e}')
except FileNotFoundError:
  print('Error: Streamlit command not found. It is installed?')