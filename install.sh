# create python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install python packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# install youtube-dl
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
