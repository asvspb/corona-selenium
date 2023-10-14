# app require installed python3.10
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3-tk python3-pip pythonpy python3.10 wget unzip
pip3 install selenium python-dotenv

# install current stable Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# find current stable webdriver link
installed_chrome_version=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
url="https://googlechromelabs.github.io/chrome-for-testing/"
webdriver_version=$(curl -s "$url" | grep -Po 'https:\/\/edgedl\.me\.gvt1\.com\/edgedl\/chrome\/chrome-for-testing\/\K\d+\.\d+\.\d+\.\d+' | head -n 1)

echo "-------------------------------------"
echo "Проверка совпадения версий..."
webdriver_version_prefix=$(echo "$webdriver_version" | cut -d '.' -f 1)
webdriver_driver_url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$webdriver_version/linux64/chrome-linux64.zip"


if [ "$installed_chrome_version" == "$webdriver_version_prefix" ]; then
  echo "Версии совпадают, скачиваем webdriver:"
  echo "-------------------------------------"

  webdriver_driver_url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$webdriver_version/linux64/chrome-linux64.zip"

  wget "$webdriver_driver_url" -O chromedriver_linux64.zip
  unzip chromedriver_linux64.zip
  sudo mv chromedriver /usr/local/bin/chromedriver
  sudo chmod +x /usr/local/bin/chromedriver

  chmod +x ./selenium_script.sh
  python3 ./selenium_script.py
  tail ./selenium_logs.txt

else
  echo "Версия установленного хром - $installed_chrome_version"
  echo "Версия webdriver - $webdriver_version_prefix"
  echo "Не совпадают, пропускаем установку!"
  echo "-------------------------------------"
fi


