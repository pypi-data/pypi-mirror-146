from email import header
from sre_parse import State
from time import sleep
from urllib import response
from urllib.request import Request
from anyio import sleep_until
from requests.auth import HTTPBasicAuth
import requests
from requests_oauthlib import OAuth2Session, OAuth2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import jsonpath

def Get_AccessToken():
    #region Declaring the data
    client_id = "PVTbheUVdporlUwUybYEu6LtNECZQ3uV"
    client_secret = "1Kt1T5MQRQ47ACdM68u9xza0jgbo4dxXoAJAuXHK6fP0terKXk89a4VfsLxObkUO"
    redirect_uri = "https://crs-qa.kroll.com"
    scope = "openid"
    #endregion

    #region getting the authorizing URL
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,scope=scope)
    authorization_url = oauth.authorization_url("https://researchclarity-dev-beta.eu.auth0.com/authorize?audience=7c3b6a5b-3d5d-4fa6-ba95-e66ad6197d77")
    print(authorization_url)
    #endregion

    #region Selenium code to get the callbackURL 
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=capa)
    driver.get(authorization_url[0])
    driver.implicitly_wait(5000)
    user = driver.find_element_by_xpath("//input[@type='email']")
    user.send_keys("Service-ServiceQAAcc@duffandphelps.com")
    submitbutton = driver.find_element_by_xpath("//span[contains(text(),'Submit')]")
    submitbutton.click()
    sleep(2)
    passcode = driver.find_element_by_xpath("//input[@type = 'password']")
    passcode.send_keys("Automation@1234567")
    sleep(2)
    signin = driver.find_element_by_id("idSIButton9")
    signin.click()
    sleep(2)
    driver.execute_script("window.stop();")
    callbackurl = driver.current_url
    print(callbackurl)
    #endregion

    #region Getting the token
    authorization_response = callbackurl
    token = oauth.fetch_token("https://researchclarity-dev-beta.eu.auth0.com/oauth/token", authorization_response=authorization_response,client_secret=client_secret, verify=False)
    print(token)
    # json_token = json.loads(token.text)
    # print(json_token)
    processed_token = jsonpath.jsonpath(token,'id_token')
    processed_token = "Bearer" + " " + processed_token[0]
    print(processed_token)
    #endregion

    #region Return processed token and oauth
    return processed_token,oauth
    #endregion