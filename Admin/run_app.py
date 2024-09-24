import os
import subprocess

# Install dependencies
# os.system("pip install -r requirements.txt")

# Run the Streamlit app
subprocess.run(["streamlit", "run", "admin.py", "--server.port=8083", "--server.address=localhost"])