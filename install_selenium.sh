sudo apt update
sudo apt install -y python3 python3-pip wget unzip
pip3 install selenium logging python-dotenv

# install Chrome && Chrome WebDriver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
chrome_version=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
chrome_driver_url="https://chromedriver.storage.googleapis.com/$chrome_version/chromedriver_linux64.zip"
wget "$chrome_driver_url" -O chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver

# run selenium script
chmod +x selenium_script.sh
python3 selenium_script.py
tail selenium_logs.txt
