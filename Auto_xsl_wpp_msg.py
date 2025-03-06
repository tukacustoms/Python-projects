from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\\Users\\operador.2207\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument("--profile-directory=Profile 11") #or Profile 11
#chrome_options.add_argument("--headless=new") #take off to use headless mode
service= Service(ChromeDriverManager().install())
driver= webdriver.Chrome(service=service,options=chrome_options)

df = pd.read_excel(r"C:\Users\operador.2207\OneDrive\Programs\Test Sync.xlsx")
contacts = df['NUMERO']
message = "Ola! Sou Arthur do Setor de Qualidade da Vivo Empresas! Vim aqui lembrar sobre os aceites digitais que estão em seu e-mail! Realizando logo entrarei contato para realizarmos sua Auditoria"

def reply():
    msg_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p')
    msg_box.click()
    msg_box.send_keys(message)

def vd_info(contact_name):
    try:
        search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div/div/div/p')
        #search_box = driver.find_element(By.XPATH,'//span[@title="{contact_name}"]') # use this code to automate existing contacts
        search_box.click()
        search_box.send_keys(contact_name)
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)
        driver.find_element(By.XPATH,'//*[@id="pane-side"]/div[1]/div/div/div[2]/div/div')
        search_box.click()
        search_box.clear()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE)
        return True
    
    except Exception as e:
        print(f"Error finding {contact_name}:{e}")
        return False
    
def run():
    #driver.get("https://app.neocrm.com.br/painel-producao/pedido")
    #driver.execute_script("window.open('https://web.whatsapp.com/', '_blank')")
    #driver.execute_script("window.open('https://web.whatsapp.com/')")
    #driver.switch_to.window(driver.window_handles[1])
    driver.get("https://web.whatsapp.com/")

    time.sleep(10) 

def checknewmessage():
    run()
    df = pd.read_excel(r"C:\Users\operador.2207\OneDrive\Programs\Test Sync.xlsx")
    while True:
        try:
            for index, row in df.iterrows():
                contact = row["NUMERO"]
                vd_info(str(contact))
                if (vd_info(contact)==True):
                    reply()
                    df.at[index, "STATUS"] = "True"
                    df.to_excel(r"C:\Users\operador.2207\OneDrive\Programs\Test Sync.xlsx", index=False)
                else:
                    df.at[index, "STATUS"] = "False"
                    df.to_excel(r"C:\Users\operador.2207\OneDrive\Programs\Test Sync.xlsx", index=False)
        except Exception as e:
            print(f"Error sending messages{e}")
        return False

checknewmessage()

driver.quit()
