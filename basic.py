# Basic opertaions with venv

# Create venv environment
python -m venv env

# Activate venv environment
source env/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the app
python3 app.py

# get the list of installed packages
pip list

# Create requirements.txt
pip freeze > requirements.txt


# Deactivate venv environment
deactivate