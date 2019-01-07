from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import copy

chrome_options = Options()
#chrome_options.add_argument("--headless")##no browser opens!!
WINDOW_Size="1920,1080"
chrome_options.add_argument("--window-size=%s" % WINDOW_Size)
driver = webdriver.Chrome(chrome_options=chrome_options)

dankstuff = "dankstuff"
username = "xxx"
password = "xx"
driver.get("https://pks.dk/login/")

# assert "Python" in driver.title
# elem = driver.find_element_by_name("ctl00$ctl00$ctl00$ContentPlaceHolderDefault$BoligExtra_container$PKSLoginByInteressentNo_1$txt_username")

usernameholder = driver.find_element_by_class_name('login-username')
passwordholder = driver.find_element_by_class_name('login-password')
usrpaslist = [usernameholder, passwordholder]

for info in usrpaslist:
    info.clear()  # we clear already set input on both username and password just in case #yaneverknow, - honestly the for loop is a bit overkill, but in case we have more in the future

usernameholder.send_keys(username)
passwordholder.send_keys(password)
passwordholder.send_keys(Keys.RETURN) #af en eller anden årsag, så skal både denne her med OG .click(), tror måske det er fordi PKS siden er lidt bøvlet idk

log_in_button_name = "ContentPlaceHolderDefault_BoligExtra_container_PKSLoginByInteressentNo_1_lb_login"
log_in_button = driver.find_element_by_id(log_in_button_name)

#clickbuttonwait = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.ID,log_in_button_name)))

log_in_button.click()

if EC.title_contains("Min side"): #tjekker lige om vi rent faktisk er kommet ind
    print("We have succesfully logged in, jubii")
else:
    exit()

#else:
  #  WebDriverWait(driver, 5).until(EC.title_contains("Min side"))

driver.get("https://pks.dk/min-side/boligoensker-placering/")
#a =[]
#a = driver.find_element_by_xpath('//p[@class="head"]')

#a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//* [@id="WishList"]/div[4]/div/p[1]')))
DormList= []
DormList.append(WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//p[contains(@class, "head")]'))))
DormList = np.array(DormList).flatten()
DormList = [j.text for j in DormList]


#q=[]
#q.append(driver.find_elements_by_xpath("//span[@class='tab-box']")) #ONLY gets text within the tab-box spawn tags.
#q=np.array(q).flatten()
#for item in q:
#    print(item.text)

xx = []

xx.append(driver.find_elements_by_xpath('//li[6][//span[@class="tab-box"]]')) #Li is parent, gets values outside <span class/tag and inside.
#we take index list [6] (remember counting starts from 1 in xpath) because that is where the number value is located.
xx = np.array(xx).flatten()
finalvaluelist = [i.text for i in xx] #first 4 values needs to be deleted
del finalvaluelist[0:4]

#just the integer values
poslist = [int(item.split()[1]) for item in finalvaluelist] #does not check if value is actually a digit
#print(DormList)
#print(poslist)

combinedlist = [final for x in zip(DormList,poslist) for final in x]
print(combinedlist)
#driver.refresh()


driver.get("https://www.findbolig.nu/logind.aspx")
findboligusername = driver.find_element_by_id('ctl00_placeholdercontent_1_txt_UserName')
findboligpassword = driver.find_element_by_id('ctl00_placeholdercontent_1_txt_Password')
findboligusername.send_keys(username)
findboligpassword.send_keys(password)
findboligpassword.send_keys(Keys.RETURN)

driver.get("https://www.findbolig.nu/Findbolig-nu/Min-side/ventelisteboliger/opskrivninger")

urls_hrefs = driver.find_elements_by_class_name('bulletLink')#.get_attribute("href")
#print(url)

OpskrivningsHREFlist = []

for item in urls_hrefs:
    OpskrivningsHREFlist.append(item.get_attribute("href"))

xop = copy.deepcopy(OpskrivningsHREFlist)
del OpskrivningsHREFlist[0:5]
del OpskrivningsHREFlist[-3:-1] #these three lines could be muuch more elegant, but this is a quick fix.
del OpskrivningsHREFlist[-1]

#print(OpskrivningsHREFlist)

#driver.get(OpskrivningsHREFlist[0])
listOfNames = []
listOfPositions = []

##findbolig er legit den langsommeste responding server jeg nogensinde har set, derfor tager det her over flere minutter hvis der er mange opskrivninger
for hreflink in OpskrivningsHREFlist:
    driver.get(hreflink)
    listOfNames.append(driver.find_element_by_id('ctl00_placeholdercontent_0_LabelBuildingNameTop').text)
    driver.find_element_by_link_text("Min placering på ventelisten").click()
    #listOfPositions.append(driver.find_elements_by_xpath('//*[@id="popupWaitlistRankText"]/p[1]/strong'))

    listOfPositions.append(WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="popupWaitlistRankText"]/p[1]/strong'))).text)




#print(listOfNames)

combinedlistfindbolig = [final for x in zip(listOfNames,listOfPositions) for final in x]
print(combinedlistfindbolig)

thefile = open('test.txt','w')
for item in combinedlistfindbolig:
    thefile.write("%s\n" % item)

thefile.close()

#driver.close()
