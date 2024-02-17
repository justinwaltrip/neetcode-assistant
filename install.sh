# create python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install python packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
