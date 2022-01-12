tilt=False
page="blank"
acc=0

import telebot
from telebot.types import Message
from PIL import Image
import random
from os import mkdir
import shutil

bot = telebot.TeleBot("5053392872:AAEEZFlnhRX16MViU94eUSq_ACczPGxHkyc")
myChatID=1639318508

pageW=0  
pageH=0
Hmax=0
fromleft=0
charspacing=0  
Pwidth=0
Pheight=0
lineWidth=0
nof=0
lof=0
noData=False
config=False
id='tapish' 

leftmargin=False  #true when '^' is passes to textTOimg()
pageNo=1     #sarting page no.

#opens the blank ruled A4 paper image
image=Image.open("source/ruled.jpeg")
send=False
width=pageW 
height=pageH
margin=0


#these variable are to be changes accordingly
def clear():
    global pageW,pageH,Hmax,fromleft,charspacing,Pwidth,Pheight,noData,lineWidth,send,nof,lof,config,leftmargin,pageNo,image,width,height,margin

    #no. of pixels from left and right respectively on page from where words starts to paste
    pageW=267  
    pageH=249
    #max height before automatically jumping to new page
    Hmax=2000
    #no. of pixels as space for writing on left margin like Que or Ans
    fromleft=130
    #the space b/w each characters
    charspacing=2  
    #height and width to write the page number
    Pwidth=1430
    Pheight=2055
    #pixel diff b/w consecutive lines
    lineWidth=56
    #no of folsers to choose from
    nof=5
    #max writable pixel length on a line
    lof=1720

                  #till here

    config=False 
    leftmargin=False  #true when '^' is passes to textTOimg()
    pageNo=1     #sarting page no.

    #opens the blank ruled A4 paper image
    image=Image.open('source/'+page+'.jpeg')
    noData=False
    send=False
    width=pageW 
    height=pageH
    margin=fromleft+random.randint(0,13)


clear()


#responsible to write on left to margin
def writeonleft(t,msg):
    global leftmargin,margin
    if t=="space":
        leftmargin=False
        margin=fromleft
    elif t=='slant':
        leftmargin=False
        margin=fromleft
        newpage(msg)
    else:
        rand=random.randint(0,nof-1)
        img=Image.open('source/'+id+'/data'+str(rand)+'/'+t+'.png')
        if tilt:
            size=list(img.size)
            scl=random.uniform(-0.1,0.1)
            size[0]=round(size[0]+size[0]*scl)
            size[1]=round(size[1]+size[1]*scl)
            ang=random.uniform(-10,10)
            img=img.rotate(ang)
            if size[0]!=0 and size[1]!=0:
                img=img.resize(size)
            
        image.paste(img,(margin,height),img)
        margin=margin+img.size[0]


#calls pagenum() and then saves the written image in output folder
#and if end is false (i.e the saved page not last page) opens the black page again to write
def newpage(msg,end=False):
    global image,height,width,pageNo,noData
    pagenum(pageNo)
    try:
        image.save('output/'+str(msg.chat.id)+'/page'+str(pageNo)+'.jpeg')
    except FileNotFoundError:
        bot.send_message(msg.chat.id,"It seems like your data is lost.\n\nType /start to reinitiate")
        noData=True
    if not end:
        image=Image.open('source/'+page+'.jpeg')
        #set default staring point
        width=pageW
        height=pageH
        pageNo=pageNo+1
    


#moves the cursor to next line and it lines are ended calls newpage()
def nextline(message):
    global height,width
    height=height+lineWidth
    width=pageW
    if(height>Hmax):
        newpage(message)

#write page number to page 
def pagenum(x):
    wid=Pwidth

    for y in str(x):
        #randomly select each character from diff data folder
        rand=random.randint(0,nof-1)
        img=Image.open('source/'+id+'/data'+str(rand)+'/'+y+'.png')
        image.paste(img,(wid,Pheight),img)
        wid=wid+img.size[0]+charspacing

        
        

# takes the whole text at ones and iterate over it to pass each char to paste on background page image
def txtTOimg(txt,message):
    global width,leftmargin
    for i in txt:

        if i=='^':
            leftmargin=True
            continue
        elif i==' ':
            i='space'
            if(width>1700-267-50):
                nextline(message)
                continue
        elif i=='\n':
            nextline(message)
            continue
        elif i=='&':
            i='and'
        elif i=='*':
            i='astric'
        elif i==',':
            i='comma'
        elif i=='$':
            i='dollar'
        elif i=='"':
            i='dquote'
        elif i=='!':
            i='exclam'
        elif i=='/':
            i='f_slash'
        elif i=='#':
            i='hash'
        elif i=='-':
            i='minus'
        elif i=='%':
            i='percent'
        elif i=='+':
            i='plus'
        elif i=="'":
            i='quote'
        elif i=='_':
            i='uscore'
        elif i=='(':
            i='sbracket_l'
        elif i==')':
            i='sbracket_r'
        elif i=='.':
            i='stop'
        elif i.isalpha():
            i=str(i)
        elif i=='`':
            i='ajeeb' 
        elif i=='@':
            i='at'
        elif i=='[':
            i='bbracket_l'
        elif i==']':
            i='bbracket_r'
        elif i==":":
            i='colon'
        elif i=='{':
            i='curly_l'
        elif i=='}':
            i='curly_r'
        elif i=='|':
            i='danda'
        elif i=='=':
            i='equal'
        elif i=='>':
            i='greaterthan'
        elif i=='<':
            i='lessthan'
        elif i=='?':
            i='que'
        elif i==';':
            i='semicolon'
        elif i=="~":
            i='slant'
        elif i=='\t':
            i='tab'
        

        if(leftmargin):
            writeonleft(i,message)
        else:
            rand=random.randint(0,4)
            try:
                img=Image.open('source/'+id+'/data'+str(rand)+'/'+i+'.png')
            except FileNotFoundError:
                bot.send_message(message.chat.id,"Character '"+i+"' not found, so omitted")
            if tilt:
                size=list(img.size)
                scl=random.uniform(-0.1,0.1)
                size[0]=round(size[0]+size[0]*scl)
                size[1]=round(size[1]+size[1]*scl)
                ang=random.uniform(-10,10)
                img=img.rotate(ang)
                if size[0]!=0 and size[1]!=0:
                    img=img.resize(size)
            image.paste(img,(width,height),img)
            width=width+img.size[0]+charspacing


def setup(message):
    try:
        mkdir("output/"+str(message.chat.id))
        with open("output/"+str(message.chat.id)+"/log.txt","w") as l:
            l.write(str(message))
    except FileExistsError:
        pass
    except Exception:
        print("something went wrong in setup()")



@bot.message_handler(commands='start')
def send_welcome(message):
    if  message.chat.id==myChatID or message.chat.id==acc:
        bot.send_message(message.chat.id,"Okk. Start sending me text.")
        setup(message)
        clear()
    else:
        bot.send_message(message.chat.id,"Dear "+message.chat.first_name+" you don't have access to this bot.\nContact @tapish101 for permission.")


@bot.message_handler(commands='config')
def configure(message):
    global config
    bot.send_message(message.chat.id,"These perameters are canfigurable right now\n\nPage - options are 'Ruled' and 'Blank'\nTilt - with option 'True' or 'False'.\n\nDefault Page is 'Blank' and Tilt is 'False'\n\nTo change first write variable name <space> your option\nFor example  Tilt True\n\nWrite 'Exit' to exit config menu.\n\nAfter config all your pages will be lost.")
    config=True


def con(message):
    return config



@bot.message_handler(func=con)
def set(message):
    global config,page,tilt

    if message.text.lower()=="exit":
        config=False
        bot.send_message(message.chat.id,"Config exited.\nData cleared.")
        clear()
        exit()

    word=message.text.split()
    if len(word)<2 or word[0].lower() not in ['tilt','page'] or word[1].lower() not in ['true','false','ruled','blank']:
        bot.send_message(message.chat.id,"Invalid selection. Try again")
    else:
        if word[0].lower()=='tilt' and word[1].lower() in ['ruled','blank'] or word[0].lower()=='page' and word[1].lower() in ['true','false']:
             bot.send_message(message.chat.id,"Use correct Parameter")
        else:
            bot.send_message(message.chat.id,word[0]+" set to "+word[1])
            if word[0].lower()=='page':
                page=word[1].lower()
            elif word[0].lower()=='tilt' and word[1]=='true':
                tilt=True
            else:
                tilt=False



@bot.message_handler(commands='clear')
def send_welcome(message):
    bot.send_message(message.chat.id,"All pages cleared.")
    clear()


@bot.message_handler(commands=['pages','page'])
def send_welcome(message):
    global send
    bot.send_message(message.chat.id,"Compressed images or not??\n\nReply 'Yes' to compress images and\n'No' for uncompressed version")
    send=True


def sendType(message):
    return send

@bot.message_handler(func=sendType)
def sendVer(message):
    global send
    if message.text.lower()=='yes':
        bot.send_message(message.chat.id,"Hold on")
        try:
            for i in range(pageNo):
                photo = open('output/'+str(message.chat.id)+'/page'+str(i+1)+'.jpeg', 'rb')
                bot.send_photo(message.chat.id, photo)
        except Exception:
            bot.send_message(message.chat.id,"Something went wrong. Try again /pages")
        finally:
            send=False
    elif message.text.lower()=='no':
        bot.send_message(message.chat.id,"Hold on")
        try:
            for i in range(pageNo):
                doc = open('output/'+str(message.chat.id)+'/page'+str(i+1)+'.jpeg', 'rb')
                bot.send_document(message.chat.id, doc)
        except Exception:
            bot.send_message(message.chat.id,"Something went wrong. Try again /pages")
        finally:
            send=False
    else:
        bot.send_message(message.chat.id,"Unrecognized Command. Try again  /pages")

    

@bot.message_handler(commands='del')
def delete(message):
    try:
        shutil.rmtree(r'output/'+str(message.chat.id))
        bot.send_message(message.chat.id,"All Your Data Cleared.\nTo start using again use command /start")
    except FileNotFoundError:
        bot.send_message(message.chat.id,"No data found.\nTo use the bot type command /start")


@bot.message_handler(commands='adduser')
def send_welcome(message):
    global acc
    try:
        usr=message.text.split()
        bot.send_message(message.chat.id,"User Added "+usr[1])
        acc=int(usr[1])
    except IndexError:
        bot.send_message(message.chat.id,"Use /addUser followed by chat id\n(ex /addUser 8765667786)")
    except Exception:
        bot.send_message(message.chat.id,"Something went wrong")

@bot.message_handler(commands='remuser')
def send_welcome(message):
    global acc
    try:
        shutil.move(str(acc), 'deleted '+str(acc))
    except Exception:
        pass
    
    bot.send_message(message.chat.id,"User removed.")
    acc=0
    


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    txtTOimg(" "+message.text,message)
    #saves the latest open page img and program ends here
    newpage(message,end=True)
    if not noData:
        bot.send_message(message.chat.id, "Written successfully.\n(Total "+str(pageNo)+" pages)")
        


bot.infinity_polling()
