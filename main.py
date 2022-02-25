#importing required libraries
import os
import random
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import speech_recognition as sr #pip install SpeechRecognition
#pip install PyAudio #speechrecoginition library use it
from playsound import playsound #pip install playsound==1.2.2 #importing function name playsound from module playsound.
from gtts import gTTS  # pip install gTTS
import pickle #pip install pickle
import csv 


#to get current file path
dir_path = os.path.dirname(os.path.realpath(__file__))



#defining some phrases in the dictionary for the program to speak
PHRASES = {
's_ggl':['OKay! I am searching.','Hang On! Searching on google.'],
's_amzn':['Let me find your deals.','Got it, Searching on amazon.','Just wait for a second.'],
's_wiki':['Searching it.','Hold On! I am searching','Just wait for a second.'],
's_ytb':['Hang On! Searching on youtube.','Wait! I got the videos.'],
'hi':['Hey! Good to see you','Hello! I am here to help you, Like a Genie!','Hello! I am here to help you.'],
'bye':['Bye! See You Again.','Feeling bad to see you going.','I had a very good time with you, Bye!'],
'err':['Sorry! But I did\'nt get it.','My bad, I wasn\'t hearing.','Oh! My bad I missed your words.','I did\'nt get that!','Have you said something?'],
's_info':['I am Aine an AI based computer program.','My name is Aine, And I am a computer program made by bunch of students.','I am an AI program, Created to intract with humans.','I am Aine, I made up of magical codes.'],
}



#common urls
URLS = {
'insta':'https://www.instagram.com/',
'fb':'https://www.facebook.com/',
'ggl':'https://www.google.com/search?q=',
'amzn':'https://www.amazon.in/s?k=',
'insta_inbx':'https://www.instagram.com/direct/inbox/',
'wtsapp':'https://web.whatsapp.com/',
'gmail':'https://mail.google.com/',
'ytb':'https://www.youtube.com/results?search_query='
}



#creators Info
creator_d = '''
            Project Details_________
            School        : Ayesha Tarin Modern Public School
            Project Name  : Project Aine-SP

            Project Partners________
            Shibli Mueed  : 12th-PCM
            Fatima Zainab : 12th-PCM
            Daud Khan     : 12th-PCB
            '''



intro='''
        I am here to help you by simplifying your tasks.
        If you want to search anything, you can say like \'What is Malaria\' or \'Who is president of USA\'.
        And I can find you good deals on Amazon, Just say like \'Find me shoes on amazon\'.
        You can ask me to \'Search cats on youtube\' or to \'Write down my facebook password\'.
        And I can calculate for you, just say like : What is 998 divide by 79.'''

    



#user name code
#it only take input when you run the code first time
try:
    with open(f'{dir_path}\\data\\user_name.dat', 'rb') as file: # using 'with' to make sure that file close
        user_name = pickle.load(file).capitalize()
        print("\nWelcome back "+user_name)
except:
    os.mkdir(f'{dir_path}\\data')
    os.mkdir(f'{dir_path}\\notes')
    text = input("\nEnter Your Name: ").lower()
    with open(f'{dir_path}\\data\\user_name.dat', 'wb') as file:
        pickle.dump(text,file)

    with open(f'{dir_path}\\data\\spdb.csv','w') as csvf:  #spdb searched parameters database
        data_fields=( 'Time','Loop Count','User','Query','Keyboard Input')
        csv.DictWriter(csvf, fieldnames=data_fields, lineterminator = '\n').writeheader()
    
    with open(f'{dir_path}\\data\\user_name.dat', 'rb') as file:
        user_name = pickle.load(file).capitalize()

    print('\nInitializing! Might take some time.')
    intro_aud = gTTS(text=intro,lang='en')
    intro_aud.save(f'{dir_path}\\data\\intro.mp3')
    print("\nHello! "+user_name+' your journey starts here!')

finally:
    pref_input = input('\nDo you want to use keyboard instead of voice input? y/n : ') or 'n'
    if pref_input != 'y':
        pref_input=False
        print('\nVoice Input SELECTED')
    else:
        pref_input=True
        print('\nKeyboard Input SELECTED')



#defining some functions below
def speak(text):  #defining speak function
    try:
        text_ts = gTTS(text=text,lang='en')
        text_ts.save(f'{dir_path}\\temp.mp3')
        print('\nAine : '+text)
        playsound(f'{dir_path}\\temp.mp3')
        os.remove(f'{dir_path}\\temp.mp3')
    except Exception as e:
        print(e)



def err():
    speak(random.choice(PHRASES['err']))



def get_input(): #defining a listening function
    
    if pref_input != True:
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source) #this line is for noise cancelation according to linrary manual
                r.pause_threshold = 1 #user max pause time
                print('\nListning...')
                audio = r.listen(source)
                said=''
        except:
            print('\nNo Microphone Found!')
        try:    #using try and except to avoid any error
            print('\nRecognizing...')
            said = r.recognize_google(audio, language='en')
            print(f'\n{user_name} : {said}')
            #inserting queries in csv file
            mk_record = True
        except:
            mk_record = False
            err()

    else:
        try:
            said = input(f'\n{user_name} : ')
            mk_record = True
        except:
            mk_record = False
            err()

    if mk_record == True:
        with open(f'{dir_path}\\data\\spdb.csv','a') as csvf:
                write_csv=csv.writer(csvf,delimiter=',',lineterminator = '\n')
                date = datetime.datetime.now().strftime("%c").replace(' ','-')
                write_csv.writerow([date,loopcount,user_name,said,pref_input])

    return said.lower()




def make_note(text):
    date = datetime.datetime.now().strftime("%x").replace('/','-') #fetching current date and time
    file_name = f'note-{text[:5]}-{date}.txt'  #naming file as current date and time with '-note.txt'
    with open(f'{dir_path}\\notes\\{file_name}', 'w') as f:
        f.write(text)



def cmd():
    print('''
    -i     to change input method
    -h     for help
    -s     for creator information
    -c     to change user name
    -spdb  to see user searched parameter database
    ===    to exit commands
    ''')

    while True:
        cmd = input('\nCommand: ')
        if cmd == '-h':
            print('='*25)
            print('''
            UI of the program is very simple, features are given below.

            1. Ask anything. Voice command search.
            2. Open diffrent websites.
            3. Calculate just by voice command.
            4. It will make text notes for you.
            5. Findproducts on amazon.
            6. Find videos on youtube.
            ''')
            print(creator_d)
            
        elif cmd == '-s':
            print(creator_d)

        elif cmd == '-c':
            global user_name
            text = input("\nEnter Your Name: ").lower()
            with open(f'{dir_path}\\data\\user_name.dat', 'wb') as file:
                pickle.dump(text,file)
            with open(f'{dir_path}\\data\\user_name.dat', 'rb') as file:
                user_name = pickle.load(file).capitalize()
            print(f"\nName change to \'{user_name}\'.")

        elif cmd == '-spdb':
            with open(f'{dir_path}\\data\\spdb.csv','r') as fo:
                readed_data=csv.reader(fo,delimiter=',')
                print(readed_data)
                for k in readed_data:
                    print(' | '.join(k))

        elif cmd == '===':
            print('\nEXITED COMMANDS!')
            break
        
        elif cmd == '-i':
            global pref_input
            pref_input = input('\nDo you want to use keyboard instead of voice input? y/n : ') or 'n'
            if pref_input != 'y':
                print('\nVoice Input SELECTED')
            else:
                print('\nKeyboard Input SELECTED')
            

        else:
            print('\nPlease enter correct command!')




#program loop start here
print('\nSay \'cmd\' to enter commands.\n\nSTARTED')



loopcount = 1 #using this variable for debugging purposes and to store data
while True:

    #opening csv file to store querirs searches by user
    query = get_input()



    #using try and exeption to handle errors
    try:
        if query != '':
            GRTNGS = ['hello','hey',]
            for j in GRTNGS: #identifing the words in string to perform tasks
                if j in query:
                    speak(random.choice(PHRASES['hi']))


            SINFO = ['who are you','introduce yourself','your intro','your name']
            for j in SINFO: #identifing the words in string to perform tasks
                if j in query:
                    if 'your name' in query:
                        speak(random.choice(PHRASES['s_info']))

                    else:
                        speak(random.choice(PHRASES['s_info']))
                        print(intro)
                        playsound(f'{dir_path}\\data\\intro.mp3')
                    


            LNCH_STRS = ['open','launch']
            for j in LNCH_STRS: #identifing the words in string to perform tasks
                if j in query:
                    if "facebook" in query:
                        webbrowser.open(URLS['fb'])
                        speak('Opening Facebook.')
                        
                    elif 'instagram' in query:
                        webbrowser.open(URLS['insta'])
                        speak('Opening Instagram.')
                        
                    elif 'inbox' in query:
                        webbrowser.open(URLS['insta_inbx'])
                        speak('Opening Instagram Inbox.')

                    elif 'mail' in query:
                        webbrowser.open(URLS['gmail'])
                        speak('Opening Gmail.')

                    elif 'whatsapp' in query:
                        webbrowser.open(URLS['wtsapp'])
                        speak('Opening WhatsApp.')

                    elif 'facebook' in query:
                        webbrowser.open(URLS['fb'])
                        speak('Opening Facebook.')

                    elif 'youtube' in query:
                        webbrowser.open(URLS['ytb'])
                        speak('Opening Youtube.')

                    else: #it will try to guess and open the websites which are not listed above
                        temp=query.replace('launch ','').replace('open ','').replace('.com','').replace('.in','').replace(' ', '')
                        webbrowser.open('http://'+temp+'.com')
                        speak("Opening "+temp)
                        
                
            
            NOTE_STRS = ['make a note', 'remember','write down']
            for j in NOTE_STRS:
                if j in query:
                    temp_query = query.replace('remember','').replace('write down','').replace('make a note','')
                    if  temp_query != '':
                        temp_query = query.replace('remember ','').replace('write down ','')
                        make_note(temp_query)
                        speak('Okay, I\'ve written it.')

                    else:
                        speak('What do you want me to write down?')
                        what = get_input()
                        make_note(what)
                        speak('Done!')
                

            QUES_STRS = ['search','find','what ','who','which','wiki','on internet','google','how','why']
            for j in QUES_STRS: #identifing the words in string to perform tasks
                if j in query:
                    temp_query = query.replace('search ','').replace('find me ','').replace('find ','').replace(' on internet','')
                    
                    SRCH_ENG =['google','on amazon','on youtube','why']
                    for k in SRCH_ENG: #identifing the words in string to perform tasks
                        if k in temp_query:
                            if 'on amazon' in temp_query:
                                temp_query = temp_query.replace('on amazon','').replace(' ','+')    
                                speak(random.choice(PHRASES['s_amzn']))
                                webbrowser.open(URLS['amzn']+temp_query)
                                
                            elif 'on youtube' in temp_query:
                                temp_query = temp_query.replace('on youtube','').replace(' ','+')    
                                speak(random.choice(PHRASES['s_ytb']))
                                webbrowser.open(URLS['ytb']+temp_query)
                                
                            else:
                                temp_query = temp_query.replace('on google','').replace('google','').replace(' ','+')
                                speak(random.choice(PHRASES['s_ggl']))
                                webbrowser.open(URLS['ggl']+temp_query)
                                
                    SRCH =['what','who','which','on internet','wiki','how']
                    for l in SRCH: #identifing the words in string to perform tasks
                        if l in temp_query:
                            temp_query = temp_query.replace('on wiki','').replace('pedia', '').replace('who ','').replace('what ','').replace('which ','').replace('how','').replace('is','').replace('are','')

                            if '' or ' ' == temp_query:
                                err()

                            elif ' + 'or' - 'or' x 'or' / ' in temp_query:
                                temp_query = temp_query.replace('what ','').replace('is ','').replace('are ','')

                                if '+' in temp_query:
                                    temp_prob = temp_query.replace(' ', '')
                                    num1,num2 = temp_prob.split('+')
                                    num1=float(num1)
                                    num2=float(num2)
                                    sol = str(num1+num2)
                                    speak('it\'s '+sol)

                                elif '-' in temp_query:
                                    temp_prob = temp_query.replace(' ', '')
                                    num1,num2 = temp_prob.split('-')
                                    num1=float(num1)
                                    num2=float(num2)
                                    sol = str(num1-num2)
                                    speak('it\'s '+sol)

                                elif 'x' in temp_query:
                                    temp_prob = temp_query.replace(' ', '')
                                    num1,num2 = temp_prob.split('x')
                                    num1=float(num1)
                                    num2=float(num2)
                                    sol = str(num1*num2)
                                    speak('it\'s '+sol)

                                elif '/' in temp_query:
                                    temp_prob = temp_query.replace(' ', '')
                                    num1,num2 = temp_prob.split('/')
                                    num1=float(num1)
                                    num2=float(num2)
                                    sol = str(num1/num2)
                                    speak('it\'s '+sol)

                                elif temp_query.find('you') == -1:
                                    try:
                                        print('\n'+random.choice(PHRASES['s_wiki']))
                                        results = wikipedia.summary(temp_query,sentences=2)
                                        speak(results)
                                    except Exception as e:
                                        print(e)
                                        speak('\nI am sorry! something was wrong with wikipedia!')
                                    

            EXT_STRS = ['quit','bye','abort','exit']
            for j in EXT_STRS:#identifing the words in string to perform tasks
                if j in query:
                    speak(random.choice(PHRASES['bye']))
                    print("\n\nPROGRAM ENDED")
                    exit()


            if 'cmd' == query:
                cmd()

    except Exception as e:
        print(e)
        err()
    loopcount+=1
