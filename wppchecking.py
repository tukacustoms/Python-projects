from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import re

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\\Users\\operador.2207\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument("--profile-directory=Profile 11") #or Profile 11
#chrome_options.add_argument("--headless=new") #take off to use headless mode
service= Service(ChromeDriverManager().install())
driver= webdriver.Chrome(service=service,options=chrome_options)

contacts = [ "Grupo Rosângela", "Grupo Claudiney", "Grupo Thaís(Parceiro"]

def vd_info(contact_name):
    try:
        search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div/p')
        search_box.click()
        search_box.send_keys(contact_name)
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)
        search_box.clear()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE)
        return True
    
    except Exception as e:
        print(f"Error finding {contact_name}:{e}")
        return False
    
def extractdata(message):
    #print(message)
    if "RAZÃO SOCIAL" in message.upper():
        if message != last_message:
            return message
    else: 
        return None
    

def checknewmessage():
    driver.get("https://web.whatsapp.com/")
    time.sleep(10)
    while True:
        try:
            for contact in contacts:
                if vd_info(contact):
                    messages = driver.find_elements(By.XPATH,'//div[contains(@class,"message-in")]')
                    if messages:
                        last_message = messages [-1].text
                        extracteddata = extractdata(last_message)
                        print(f"{extracteddata}")
                      
                else:
                    return None
        except Exception as e:
            print(f"Error:", {e})

checknewmessage()
