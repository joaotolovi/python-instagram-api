import time
import os, random, json
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time,threading
import os, random, json, datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_stealth import stealth
from selenium.webdriver.support.wait import WebDriverWait
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import websocket
from threading import Thread
import datetime, time,requests


class Instagram:
    def __init__(self, user, password, url="https://www.instagram.com/"):
        self.options = webdriver.ChromeOptions() 
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.binary_location = "chrome-win\chrome_original.exe"
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--window-size=1280,800")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument(f'user-data-dir={os.path.realpath("./chrome-win")}') 
        self.capabilities = DesiredCapabilities.CHROME
        self.capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        chrome_service = Service("./chromedriver.exe")
        chrome_service.creationflags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(service=chrome_service,options=self.options,desired_capabilities=self.capabilities)
        self.people = []
        self.palavras=['imports','multimarcas','griff','loja','roupa','roupas','masculina','marcas','modas']
        self.url=url

    def login_verify(self):
        for x in range(6):
            try:
                self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div')
                print('Login')
                self.findAppId()
                return True
            except:
                time.sleep(0.5)
            return False

    def login(self):
        print('foi')
        self.session = requests.Session()
        self.driver.get(self.url)
        time.sleep(3)
        if self.login_verify()==False:
            try:
                username = self.driver.find_element(By.NAME,"username")
                password = self.driver.find_element(By.NAME,"password")
                username.send_keys(USERNAME)
                password.send_keys(PASSWORD)
                password.send_keys(Keys.ENTER)
            except:pass
            self.login_verify()
        
    def verifica(self, texto, palavras):
        for palavra in palavras:
            if palavra.lower() in texto.lower():
                return True
        return False

    def findAppId(self):
        while True:
            self.log=self.get_browser_log()
            if 'x-ig-app-id' in str(self.log):
                print(55)
                self.find_app_id=self.find_in_array(self.log,'x-ig-app-id')
                self.app_id=self.find_value_by_key(self.find_app_id,'x-ig-app-id')
                print('app id')
                break
        self.session.headers.update({'authority': 'i.instagram.com',
                                    'sec-ch-ua': '"Chromium";v="91", " Not;A Brand";v="99"',
                                    'x-ig-www-claim': 'hmac.AR1lvB8BpVZOkcStf7WaDJKfKwKPPTff3XRrxqZrMLufKDG1',
                                    'sec-ch-ua-mobile': '?0',
                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4463.0 Safari/537.36',
                                    'accept': '*/*',
                                    'x-asbd-id': '198387',
                                    'x-csrftoken': self.find_cookie('csrftoken'),
                                    'x-ig-app-id': self.app_id,
                                    'origin': 'https://www.instagram.com',
                                    'sec-fetch-site': 'same-site',
                                    'sec-fetch-mode': 'cors',
                                    'sec-fetch-dest': 'empty',
                                    'referer': 'https://www.instagram.com/',
                                    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                                    'cookie': f'sessionid={self.find_cookie("sessionid")};',
                                    })
        

    def get_folowers_by_id(self,user):
        params = {
            'count': '100',
            'search_surface': 'follow_list_page',
            #'max_id':0,
        }

        self.users=[]
        while True:
            self.response = self.session.get(f'https://i.instagram.com/api/v1/friendships/{user}/followers/', params=params)
            self.response=self.response.json()
            for user_ in self.response['users']:
                self.users.append(user_)
            if self.response['big_list']==True:
                if 'next_max_id' in self.response:
                    params.update({'max_id':self.response['next_max_id']})
                else:
                    if 'max_id' not in params:
                        params['max_id']=0
                    params['max_id']+=100
            else:return self.users
            time.sleep(3)


    def get_folowers_by_username(self,user):
        user=self.get_user_by_username(user)
        user=user['id']
        return self.get_folowers_by_id(user)

    def get_following_by_id(self,user,size=10000):
        params = {
            'count': '100',
            'search_surface': 'follow_list_page',
            'max_id':0,
        }

        self.users=[]

        while True:
            self.response = self.session.get(f'https://i.instagram.com/api/v1/friendships/{user}/following/', params=params)
            self.response=self.response.json()
            for user_ in self.response['users']:
                self.users.append(user_)
                if len(self.users) >=size:return self.users

            if self.response['big_list']==True:
                if 'next_max_id' in self.response:
                    params.update({'max_id':self.response['next_max_id']})
                else:
                    if 'max_id' not in params:
                        params['max_id']=0
                    params['max_id']+=100
                    
            else:return self.users
            time.sleep(3)

    def get_following_by_username(self,user,size=10000):
        user=self.get_user_by_username(user)
        user=user['id']
        return self.get_following_by_id(user,size)

    def get_user_by_username(self,username):
        params = {
            'username': username,
            }

        self.response = self.session.get('https://i.instagram.com/api/v1/users/web_profile_info/', params=params)
        return self.response.json()['data']['user']

    def get_timeline(self, size=1000):
        data = {}
        self.timeline=[]
        for x in range(size):
            response = self.session.post('https://i.instagram.com/api/v1/feed/timeline/', data=data)

            response=response.json()
            if "next_max_id" in response:data["max_id"]=response["next_max_id"]
            for x in response["feed_items"]:
                self.timeline.append(x)
                if len(self.timeline) >=size:return self.timeline
        return self.timeline
            
        
    def like_post_by_id(self, id_):
        response = self.session.post(f'https://www.instagram.com/web/likes/{id_}/like/')

    def follow_user_by_id(self, id_):
        response = self.session.post(f'https://www.instagram.com/web/friendships/{id_}/follow/')        

    def unfollow_user_by_id(self, id_):
        response = self.session.post(f'https://www.instagram.com/web/friendships/{id_}/unfollow/')        
       
    def find_followers(self):
        self.driver.get(f'{self.url}/{self.user_scrap}')
        time.sleep(3)
        followers = self.driver.find_element(By.CSS_SELECTOR,"ul li a")
        followers.click()
        time.sleep(5)
        down = self.driver.find_element_by_class_name('_aano')
        person = self.driver.find_elements_by_css_selector("_acan _acap _acas")
        

        while True:
            for i in range(5):
                        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", down)
                        time.sleep(2)
            if person != self.driver.find_elements_by_css_selector("li button"):
                person = self.driver.find_elements_by_css_selector("li button")
                for i in range(10):
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", down)
                    time.sleep(2)
            break
        self.users=[]
        self.people_names = self.driver.find_element(By.CLASS_NAME,"_aaep")
        for x in self.people_names:
            self.users.append(x.text)

        a=open('users.txt', 'w')
        a.write(str(self.users))
        a.close()


    def follow(self):
        self.driver.get(f'{self.url}/{self.user_scrap}')
        time.sleep(3)
        followers = self.driver.find_element(By.CSS_SELECTOR,"ul li a")
        followers.click()
        time.sleep(5)
        down = self.driver.find_element(By.CLASS_NAME,'_aano')
        
        while True:
            self.people = self.driver.find_element(By.CSS_SELECTOR,"_acan _acap _acas")
            qt=0
            self.non_follow=False
            for person in self.people:
                try:
                    if person.text=='Follow' or person.text=='Seguir':
                        self.non_follow=True
                        print(person.text)
                        qt+=1
                        if qt==40:
                            qt=0
                            time.sleep(900)
                        person.click()
                        time.sleep(random.randint(30,40)/random.randint(1,3))
                except:print('err')
                # self.driver.quit()
            while True:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", down)


    def process_browser_log_entry(self,entry):
        response = json.loads(entry['message'])['message']
        return response

    def get_browser_log(self):
        self.browser_log = self.driver.get_log('performance') 
        self.events = [self.process_browser_log_entry(entry) for entry in self.browser_log]
        
        return self.events

    def find_in_array(self,array, value):
        for x in array:
            if value in str(x):
                return x

    def find_value_by_key(self,dic,value):
        for x in dic:
            if isinstance(dic,dict):
                if value in dic[x]:
                    print(2)
                    return dic[x][value]
                if value in dic.values():
                    return dic
                elif value in str(dic[x]):
                    return self.find_value_by_key(dic[x], value)

            if isinstance(dic,list):
                if value in dic:
                    return x
                elif value in str(x):
                    return self.find_value_by_key(x, value)


    def get_cookies(self):
        self.cookies=self.driver.execute_cdp_cmd('Network.getAllCookies',{})['cookies']

    def find_cookie(self, cookie):
        self.get_cookies()
        return self.find_value_by_key(self.cookies, cookie)['value']
                
