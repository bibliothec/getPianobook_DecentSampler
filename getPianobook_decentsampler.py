import os
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# script to get pianobook for decent sampler
# download items in current directory
# setting
downloaddir = os.getcwd()
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": downloaddir
})
driver = webdriver.Chrome(options=options)
# login
loginurl = "https://www.pianobook.co.uk/members/login/?redirect_url=https://www.pianobook.co.uk/"
myemail = ""  # input your resisterd email addr
mypasswd = ""  # input your resisterd password
driver.get(loginurl)
email = driver.find_element(By.ID, "user_login")
passwd = driver.find_element(By.ID, "user_pass")
email.clear()
passwd.clear()
email.send_keys(myemail)
passwd.send_keys(mypasswd)
email.submit()
time.sleep(1)
print("Successfully login")
# move main content
mainurl = "https://www.pianobook.co.uk/packs/"
driver.get(mainurl)
print("Successfully load page")
time.sleep(3)
driver.find_element(By.CLASS_NAME, "moove-gdpr-infobar-allow-all").click()
print("Accept cookies")
getDSxpath = ("/html/body/div[1]/div/div[3]/div/div[1]/div[2]/ul/li[1]/button")
driver.find_element(By.XPATH, getDSxpath).click()
print("Successfully getDSxpath")
time.sleep(1)
# expansion all contents
while True:
    try:
        loadmore = driver.find_element(By.CLASS_NAME, "button--loadmore")
    except:
        break
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    loadmore.click()
    time.sleep(1)
print("Successfully load all content")
# download items
item = driver.find_elements(By.CLASS_NAME, "cardinfo")
itemnum = len(item)
for num in range(itemnum):
    driver.switch_to.window(driver.window_handles[0])
    tmpsiteurl = item[num].get_attribute("href")
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(tmpsiteurl)
    time.sleep(2)
    tmpitemtag = driver.find_element(By.CLASS_NAME, "download")
    tmpitemurl = tmpitemtag.get_attribute("href")
    tmpfilename = urllib.parse.unquote(os.path.basename(tmpitemurl))
    tmpfilepath = os.path.join(downloaddir, tmpfilename)
    if os.path.exists(tmpfilepath):
        print(str(tmpfilename)+" was downloaded. Skip it.")
        time.sleep(2)
        if(num<itemnum-1):
            driver.close()
        continue
    tmpitemtag.click()
    print("Download "+str(tmpfilename))
    time.sleep(3)
    driver.close()
time.sleep(10)
print("Successfully download")
driver.close()
driver.quit()
