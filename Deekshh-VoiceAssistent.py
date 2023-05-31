#!/usr/bin/env python
# coding: utf-8

# In[17]:


pip install gobject


# In[18]:


import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import pyaudio
import yfinance as yf
import wolframalpha as wfa
import translators as ts
import requests
import time
import wikipedia
import datetime


# # coding

# In[22]:


#wolfram alpha API - key --https://products.wolframalpha.com/api
wolfram_api = 'UUVYKY-XPHG6U3UWW'

#chuck norris API --https://api.chucknorris.io/
chuck_norris_api = "https://api.chucknorris.io/jokes/random"

#news API key -- newsapi.org
news_api_key = "81c87f0f0c6b436687bc24a24185d879"

#weather API hey -- whetherbit.io
whether_api_key = "a3a80d246cdf436f80ba57db30e1d8a4"

#distance API key --  mapquestai.com -- https://developer.mapquest.com/documentation/directions-api/route/get
distance_api_key = "4jaYMXPcgRXZQT1DofjmdL6julCBpHo7"


#function to get capital of country -- wfa
def wolfram_alpha_capital(text):
    client = wfa.Client(wolfram_api)
    result = client.query(text)        #we can write aur text here
    answer = next(result.results).text
    ans = answer.split()
    deekshh_speak('The capital of ' + ans[-1] + ' is ' + ans[0])
    
 
#function to calculate -- wfa
def wolfram_alpha_calculator(text):
    client = wfa.Client(wolfram_api)
    result = client.query(text)
    answer = next(result.results).text
    deekshh_speak('The answer is ' + answer)
    
    
#function to get the president -- wfa
def wolfram_alpha_president(text):
    client = wfa.Client(wolfram_api)
    result = client.query(text)
    ans = next(result.results).text
    deekshh_speak('The President is' + ans)
    
    
#translator 
def translator(text):
    deekshh_speak_german(ts.google(text, from_language = 'en', to_language = 'de'))
    
    
#jokes
def chuck_norris():
    ck = chuck_norris_api   #link to random jokes
    cn_data = requests.get(ck)
    cn_json = cn_data.json()
    deekshh_speak(cn_json['value'])

    
#news
def get_news():
    news_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + news_api_key
    news = requests.get(news_url).json()
    articles = news["articles"]
    # print(len(articles))

    news_headlines = []
    for art in articles:
        news_headlines.append(art['title'])

    #first five headlines only
    for i in range(3):
        deekshh_speak(news_headlines[i])
 

#whether information
def get_whether():
    deekshh_speak("No problem, i will look it up for you. What city are you interested in?")
    whether_city = deekshh_listen()
    whether_url = "https://api.weatherbit.io/v2.0/current?city=" + whether_city + "&key=" + whether_api_key
    whether = requests.get(whether_url).json()
    temp = whether["data"][0]["temp"]
    description = whether["data"][0]["weather"]["description"]
    deekshh_speak("The temperature in " + whether_city + " is " + str(temp) + "degrees and you can experiance " + description + " whether")

    
#distance information 
def get_distance():
    deekshh_speak("Sure, please name the two cities: The first city is")
    from_city = deekshh_listen()
    time.sleep(2)
    deekshh_speak("And the second city is")
    to_city = deekshh_listen()
    deekshh_speak("Just a minute")
    distance_url = "https://www.mapquestapi.com/directions/v2/route?key=" + distance_api_key + "&from=" + from_city + "&to=" + to_city + "&unit=k"
    dis_req = requests.get(distance_url).json()
    # print(dis_req)
    dis = round(dis_req["route"]["distance"], 2)
    deekshh_speak("The distance between " + from_city + " to " + to_city +" is " + str(dis) + "kilometers")

    
#wikipedia
def get_info():
    deekshh_speak("Sure, Let me know what i can search for you on wikipedia?")
    val = deekshh_listen()
    wiki_result = wikipedia.summary(val, sentences=1)
    deekshh_speak(wiki_result)
   

#time 
def get_time_now():
    x = datetime.datetime.now()
    hour = x.strftime("%I")
    minute = x.strftime("%M")
    meridiem = x.strftime("%p")
    weekday = x.strftime("%A")
    time = "It is " + hour + ':' + minute + ' ' +meridiem
    deekshh_speak(time)

    
#day
def get_weekday():
    x = datetime.datetime.now()
    weekday = x.strftime("%A")
    deekshh_speak(time)
  




#convert what we speak(speech) to text!
def deekshh_listen():
    r = sr.Recognizer()
    mic_index = sr.Microphone().list_microphone_names().index('default')

    # Configure the microphone audio source using pyaudio
    p = pyaudio.PyAudio()
    mic = sr.Microphone(device_index=mic_index)
    try:
        with mic as source:
            #use listen fun to catch source(mic) by recognizer
            audio = r.listen(source)
            text = ''
        
        
            #using google api to convert speach to text
            text = r.recognize_google(audio)

    except sr.RequestError as re:
                print(re)

    except sr.UnknownValueError as uve:
                print(uve)

    except sr.WaitTimeoutError as wte:
                print(wte)

    text = text.lower()
    return text

    
#converting text generated to speech to give response in speech
def deekshh_speak(text):
    #creating audio data
    fn = 'audio_data.mp3'
    #converting text to speech using google api
    ts = gTTS(text=text, lang='en')
    ts.save(fn) #saving that file
    playsound.playsound(fn) #play
    os.remove(fn) #delete that file
 

#converting text generated to speech to give response in speech --german --done for german accent -- other it reads with english pronounciation
def deekshh_speak_german(text):
    #creating audio data
    fn = 'audio_data.mp3'
    #converting text to speech using google api
    ts = gTTS(text=text, lang='de')
    ts.save(fn) #saving that file
    playsound.playsound(fn) #play
    os.remove(fn) #delete that file    -- similarly we can do for other languages as well
    
    
#reply based on the input text
def deekshh_reply(text):
    
    #what is ur name
    if 'what' in text and 'name' in text:
        deekshh_speak('Hi, My name is Deekshh and I am your personal assistent')
        
    #why do u exist
    elif 'why' in text and 'exist' in text:
        deekshh_speak("i exist to help you 24/7")
        
    #when do you sleep
    elif 'when' in text and 'sleep' in text:
        deekshh_speak("I never sleep. I was created to support you 24 hours")
        
    ##favourite movie
    elif 'favourite' in text or 'favorite' in text and 'movie' in text:
        deekshh_speak("my favourite movie is titanic. I watch it with my friends")
        
    #stocks - apple
    elif 'apple' in text:
        apple = yf.Ticker("AAPL")
        deekshh_speak('At this moment you can purchase one apple share for ' + str(apple.info['regularMarketPrice']) + ' US Dollars')
        
    #stocks - Facebook
    elif 'facebook' in text:
        facebook = yf.Ticker("FB")
        deekshh_speak('At this moment you can purchase one apple share for ' + str(facebook.info['regularMarketPrice']) + ' US Dollars')
                    
    #stocks - tesla   -- can add more stocks from yfinance.com
    elif 'tesla' in text:
        tesla = yf.Ticker("TSLA")
        deekshh_speak('At this moment you can purchase one apple share for ' + str(tesla.info['regularMarketPrice']) + ' US Dollars')
                      
    #wolfram_alpha -- capital of country
    elif 'capital of' in text:
        wolfram_alpha_capital(text)
        
    #wolfram_alpha -- calculator
    elif 'add' in text or 'subtracted by' in text or 'multiply' in text or 'multiplied' in text or 'divide' in text or 'divided by' in text or 'root' in text:
        wolfram_alpha_calculator(text)
     
    #wolfram_alpha -- president
    elif 'who' in text and 'president of' in text:
        wolfram_alpha_president(text)
       
    #translator -- one language to another
    elif 'translate' in text:
        deekshh_speak("Sure, what do you want me to translate")
        while True:
            textToTrans = deekshh_listen()
            if textToTrans != 'Turn Of Translator':
                translator(textToTranslate)
            else:
                deekshh_speak("The translator will be turned off")
                break
    
    #chuck norris jokes
    elif 'chuck norris jokes' in text:
        chuck_norris()
     
    
    #news api --top 3 news headlines
    elif 'news' in text:
        deekshh_speak("The first 3 headlines are: ")
        get_news()
    
    
    #whether info
    elif 'whether' in text:
        get_whether()
     
    
    #distance between two citites
    elif 'distance' in text:
        get_distance()
      
    
    #information from wikipedia
    elif 'information' in text or 'wikipedia' in text:
        get_info()
    
    #time
    elif 'time' in text:
        get_time_now()
        
    #day
    elif 'weekday' in text or 'day' in text:
        get_weekday()
    
    
    
    elif 'Bye' or 'Bubyee' in text:
        deekshh_speak("Bubbye, hope i was helpful!, Have a good day")
        
    else:
        deekshh_speak("sorry i didn't get that, Can you please repeat?")
        
    

    
 


# ## execute section

# In[1]:


#execute this assistent!
def execute_assist():
    
    #asking details
    deekshh_speak('Hi, I am here to support you. Can you please tell me your name?')
    name = deekshh_listen()
    deekshh_speak('Hi,' + name + 'what can i do for you')
    
    while True:
        #in order to intercept what we say we will store, what deekshh will listen to a var listen_dee 
        #and from based on what we say reply will be given from deekshh_reply
        listened_by_dee = deekshh_listen() #what we say(our voice) is listened by deekshh_listen fuc
        print(listened_by_dee)
        deekshh_reply(listened_by_dee)
        
        #to end the while loop
        if "bye" in listened_by_dee:
            break
            
        
execute_assist()


# In[ ]:


# wolfram alpha api
# generate this api --UUVYKY-XPHG6U3UWW from the website

#for capital
# client = wfa.Client(wolfram_api)
# result = client.query('what is the capital of russia?')
# answer = next(result.results).text
# ans = answer.split()
# print('The capital of ' + ans[-1] + ' is ' + ans[0])

#for maths
# client = wfa.Client(wolfram_api)
# result = client.query('1+1')
# answer = next(result.results).text
# deekshh_speak('The answer is ' + answer)

#for president
# client = wfa.Client(wolfram_api)
# result = client.query('who is the president of india?')
# ans = next(result.results).text
# deekshh_speak('The President is' + ans)


# In[ ]:


# translator api -- download tanslator package!


# ts.google('i live in india and today i eat something', from_language = 'en', to_language = 'de')


# In[ ]:


# chuck norris api

# chuck_norris_api = "https://api.chucknorris.io/jokes/random"   #link to random jokes
# cn_data = requests.get(chuck_norris_api)
# cn_json = cn_data.json()
# deekshh_speak(cn_json['value'])


# In[ ]:


#news 

# news_api_key = "81c87f0f0c6b436687bc24a24185d879"

# news_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + news_api_key
# news = requests.get(news_url).json()
# # print(news)
# articles = news["articles"]
# # print(len(articles))


# news_headlines = []

# for art in articles:
#     news_headlines.append(art['title'])
    
# # print(news_headlines)

# #first five headlines only
# for i in range(5):
#     print(str(i+1) + ") " + news_headlines[i])


# In[ ]:


#whether 

# whether_api_key = "a3a80d246cdf436f80ba57db30e1d8a4"
# whether_city = "Delhi"
# whether_url = "https://api.weatherbit.io/v2.0/current?city=" + whether_city + "&key=" + whether_api_key
# whether = requests.get(whether_url).json()
# # print(whether)
# temp = whether["data"][0]["temp"]
# description = whether["data"][0]["weather"]["description"]
# deekshh_speak("The temperature in " + whether_city + " is " + str(temp) + "degrees and you can experiance " + description + " whether")


# In[ ]:


#distance between two citites -- mapquestapi.com

# distance_api_key = "4jaYMXPcgRXZQT1DofjmdL6julCBpHo7"
# from_city = "Delhi"
# to_city = "Jabalpur"
# distance_url = "https://www.mapquestapi.com/directions/v2/route?key=" + distance_api_key + "&from=" + from_city + "&to=" + to_city + "&unit=k"
# dis_req = requests.get(distance_url).json()
# # print(dis_req)
# dis = round(dis_req["route"]["distance"], 2)
# deekshh_speak("The distance between " + from_city + " to " + to_city +" is " + str(dis) + "kilometers")


# In[ ]:


#wikipedia -- download pip install wikipedia

# wiki_result = wikipedia.summary('Donald Trump', sentences=1)
# deekshh_speak(wiki_result)


# In[ ]:


#date and time module -- import datetime

#return year and name of weekday

# x = datetime.datetime.now()
# hour = x.strftime("%I")
# minute = x.strftime("%M")
# meridiem = x.strftime("%p")
# weekday = x.strftime("%A")
# time = "It is " + hour + ':' + minute + ' ' +meridiem
# print(time, weekday)


# In[ ]:




