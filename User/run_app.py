import os
import subprocess

# Install dependencies
# os.system("pip install -r requirements.txt")

# Run the Streamlit app
subprocess.run(["streamlit", "run", "app.py", "--server.port=8084", "--server.address=localhost"])