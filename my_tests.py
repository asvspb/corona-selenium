from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
load_dotenv()

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
