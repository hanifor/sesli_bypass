import time
from selenium import webdriver
import speech_recognition as sr
from selenium.webdriver.common.by import By
import requests
from pydub import AudioSegment



driver = webdriver.Chrome()
driver.get("https://google.com/recaptcha/api2/demo")

recaptcha_box_iframe = driver.find_element(By.XPATH,'//*[@id="recaptcha-demo"]/div/div/iframe')
driver.switch_to.frame(recaptcha_box_iframe)
driver.find_element(By.XPATH,'//*[@id="recaptcha-anchor"]').click()

time.sleep(2)

driver.switch_to.default_content()

time.sleep(2)

listen_box_iframe = driver.find_element(By.XPATH,'/html/body/div[2]/div[4]/iframe')
time.sleep(1)
driver.switch_to.frame(listen_box_iframe)
driver.find_element(By.XPATH,'//*[@id="recaptcha-audio-button"]').click()

time.sleep(2)

sound_link = driver.find_element(By.XPATH,'//*[@id="rc-audio"]/div[7]/a').get_attribute("href")

r = requests.get(f"{sound_link}")

with open("sound.mp3","wb") as f:
    f.write(r.content)

sound = AudioSegment.from_mp3("sound.mp3")
sound.export("sound.wav",format = "wav")

time.sleep(2)

rr = sr.Recognizer()

captcha_audio = sr.AudioFile("sound.wav")

with captcha_audio as source:
    audio = rr.record(captcha_audio)
    result = rr.recognize_google(audio,language="en-US")

print(result)
driver.find_element(By.XPATH,'//*[@id="audio-response"]').send_keys(result)
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="recaptcha-verify-button"]').click()

time.sleep(1000)