from sqlalchemy import true
import undetected_chromedriver as uc
import pandas as pd
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
from time import sleep

class GoogleReviewBot:
    
    def __init__(self,mailaddress,password,comment):
        self.mailaddress = mailaddress
        self.password = password
        self.comment = comment
        self.completedAccounts = open("./data/completedAccounts.csv","a")
        self.waitDuration = [3,4,5]
        self.initialize()

    def initialize(self):
        self.i = 0
        PlaceURL = "https://www.google.com/search?q=tnl+cafe&sca_esv=17318cc11200120d&biw=1879&bih=969&tbm=lcl&sxsrf=ADLYWIIblDYcRUOd_MtwrkzptGt2NA3Lzw%3A1735212656488&ei=cD5tZ4a4HZ2sseMP_-6poAg&oq=tnl+ca&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIgZ0bmwgY2EqAggAMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEjsIFCpDFj7EnAAeACQAQCYAZkBoAHoBaoBAzMuNLgBA8gBAPgBAZgCB6ACgQbCAgQQIxgnwgIKEAAYgAQYQxiKBcICEBAAGIAEGLEDGEMYgwEYigXCAgsQABiABBixAxiDAZgDAIgGAZIHAzIuNaAH1ik&sclient=gws-wiz-local#rlfi=hd:;si:3281324097293305655,l,Cgh0bmwgY2FmZUiMg5Czs6-AgAhaFBAAEAEYASIIdG5sIGNhZmUyAm1zkgEEY2FmZZoBI0NoWkRTVWhOTUc5blMwVkpRMEZuU1VNdE1VcExlVWxCRUFFqgE_EAEqDCIIdG5sIGNhZmUoKDIfEAEiG_tP5qC1qpf9PJN2i93QkruLP9FBpsCI25Q6uTIMEAIiCHRubCBjYWZl-gEECCcQQw,y,hzEty7yUZVQ;mv:[[3.04728807731903,101.64586343213718],[3.0469281226809706,101.64550296786285]]" #ENTER YOUR LINK HERE
        self.driver = uc.Chrome()
        self.driver.delete_all_cookies()
        self.urls = ["https://accounts.google.com/signin/v2/identifier?hl=tr&passive=true&continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dgoogle%26oq%3Dgoogle%26aqs%3Dchrome.0.69i59l3j0i271l2j69i60j69i65j69i60.706j0j1%26sourceid%3Dchrome%26ie%3DUTF-8&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin",PlaceURL]
        self.driver.get(self.urls[self.i])
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,("identifierNext"))))
        
    def _login(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,("identifierNext"))))
            login=self.driver.find_element(By.ID,"identifierId")
            login.send_keys(self.mailaddress)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,("identifierNext")))).click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"passwordNext")))
            password=self.driver.find_element(By.NAME,("password")) 
            password.send_keys(self.password)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"passwordNext"))).click()
            sleep(random.choice(self.waitDuration))
        except:
            print("There is a problem 1.")
            pass
         
    def _comment(self):
        try:
            self.i +=1
            self.driver.get(self.urls[self.i]) 
            sleep(random.choice(self.waitDuration))   
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[18]/iframe")))
            self.driver.find_element(By.XPATH,("/html/body/div[1]/c-wiz/div/div/div/div/div[1]/div[3]/div[2]/div[3]/div[1]/textarea")).send_keys("Comment")
            elem=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#yDmH0d > c-wiz > div > div > div > div > div.O51MUd > div.l5dc7b > div.DTDhxc.eqAW0b > div.euWHWd.aUVumf > div > div:nth-child(5)")))
            self.driver.execute_script("arguments[0].click();", elem)
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#ZRGZAf > span"))).click()
            sleep(random.choice(self.waitDuration))
            self.completedAccounts.write(self.mailaddress + "-" + self.password + "\n")
            self.driver.close()
        except:
            print("There is a problem in Comment.")
            pass

    @staticmethod
    def GetUserInfo(mailaddressFile,passwordsFile,commentsFile):
        get_MailAdresses=pd.read_csv(mailaddressFile).sample(frac=1,random_state=0)
        get_Passwords=pd.read_csv(passwordsFile).sample(frac=1,random_state=0)
        get_Comments=pd.read_csv(commentsFile).sample(frac=1,random_state=0)
        num = min(len(get_MailAdresses),len(get_Passwords),len(get_Comments))
        UserInfo= get_MailAdresses
        UserInfo["mailaddress"] = get_MailAdresses.values
        UserInfo["password"] = get_Passwords.values
        UserInfo["comment"] = get_Comments.values
        UserInfo.index = range(num)
        return UserInfo
    
    
if __name__ == "__main__":
    mailaddressFile = "./data/mailaddresses.csv"
    passwordsFile = "./data/passwords.csv"
    commentsFile = "./data/comments.csv"
    UserInfoDF = GoogleReviewBot.GetUserInfo(mailaddressFile, passwordsFile,commentsFile)
    for num in range(len(UserInfoDF)):
        UserInfoSeries = UserInfoDF.loc[num]
        GRB = GoogleReviewBot(*UserInfoSeries)
        try:
            GRB._login()
            GRB._comment()
        except:
            print("There is a problem.")
            pass
