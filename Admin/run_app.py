import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

admin_file=os.getenv('ADMIN_FILE')
admin_address=os.getenv('ADMIN_ADDRESS')
admin_port=os.getenv('ADMIN_PORT')

# Install dependencies
# os.system("pip install -r requirements.txt")

if not all([admin_file, admin_address, admin_port]):
  print(f'Error: One or more required environment variables are not set')
  exit(1)

command = ["streamlit", "run", f"{admin_file}.py", f"--server.port={admin_port}", f"--server.address={admin_address}"]

try:
  subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
  print(f'Error running Streamlit: {e}')
except FileNotFoundError:
  print('Error Streamlit command not found. It is installed?')