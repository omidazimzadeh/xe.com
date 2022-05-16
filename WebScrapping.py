import os
import time
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options as options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import mysql.connector as myssql


def startdb():
    global mydb, mycursor
    try:
        mydb = myssql.connect(
            host="localhost",
            user="root",
            password="admin",
            database="tradingview"
        )

        # buffer is true nabashe misheUnread result found
        mycursor = mydb.cursor(buffered=True)

    except (myssql.Error, myssql.Warning) as e:
        print(e)
        return None


def closedb():
    # 4. Commit changes
    mydb.commit()
    # 5. Close connections
    mycursor.close()


def insert(listed):
    try:
        startdb()
        val = tuple(listed)
        if len(val) == 4:
            mycursor.execute(
                "INSERT INTO omidd (euro,gbp,cad,aud)  VALUES (%s,%s,%s,%s)", val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        pass
    except (myssql.Error, myssql.Warning) as e:
        print(e)
        return None
    closedb()


def main():

    FireFoxDriverPath = Service(os.path.join(
        os.getcwd(), 'Driver', 'geckodriver.exe'))
    browser = webdriver.Firefox(service=FireFoxDriverPath)
    browser.implicitly_wait(7)

    url = "https://www.xe.com/"
    browser.get(url)

    browser.find_element(
        By.XPATH, '//*[@id="__next"]/div[2]/div[4]/section/div[1]/div[1]/div[1]/div/div').click()

    keys = browser.find_element(By.XPATH, '//*[@id="dashboard-top-row"]')
    keys.send_keys("aed")
    keys.send_keys(Keys.ENTER)
    keys = browser.find_element(By.XPATH, '//*[@id="pugsnax"]')
    keys.send_keys("aud")
    keys.send_keys(Keys.ENTER)
    finds_before = []
    finds = []
    while(True):

        find_euro = browser.find_element(By.XPATH,
                                         '/html/body/div[1]/div[2]/div[4]/section/div[1]/div[3]/div/div[1]/div/div').text
        splited_euro = find_euro.split(" ")
        finds.append(splited_euro[0])

        find_gbp = browser.find_element(By.XPATH,
                                        '/html/body/div[1]/div[2]/div[4]/section/div[1]/div[4]/div/div[1]/div/div').text
        splited_gbp = find_gbp.split(" ")
        finds.append(splited_gbp[0])

        find_cad = browser.find_element(By.XPATH,
                                        '/html/body/div[1]/div[2]/div[4]/section/div[1]/div[6]/div/div[1]/div/div').text
        splited_cad = find_cad.split(" ")
        finds.append(splited_cad[0])

        find_aud = browser.find_element(By.XPATH,
                                        '/html/body/div[1]/div[2]/div[4]/section/div[1]/div[7]/div/div[1]/div/div').text
        splited_aud = find_aud.split(" ")
        finds.append(splited_aud[0])

        if finds == finds_before:

            finds_before = finds.copy()
            finds.clear()
            continue
        elif finds != finds_before:
            print("mosavi nistan")
            finds_before = finds.copy()
            insert(finds)
            time.sleep(3)
            finds.clear()


if __name__ == '__main__':
    main()
