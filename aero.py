from flask import Flask,render_template,url_for,request
import mysql.connector
from mysql.connector.errors import Error



conn=mysql.connector.connect(host="localhost",user="root",password="root",db="aero") #connecting to database
cursor = conn.cursor() #assigning cursor function
print(conn)

global bok
bok =[]
global mk
mk=[]
global seat
seat=0
global ticketid
ticketid=0
global name
name= None

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():                                     #index function
    return render_template('index.html')
@app.route('/indexa',methods=['GET','POST'])
def indexa():
    global name
    return render_template('indexa.html',value=name)

@app.route('/booking' ,methods=['GET','POST'])
def booking():
    #booking function comes here                                #booking function
    return render_template('booking.html')

@app.route('/details' ,methods=['GET','POST'])
def details():
    global bok
    #ava_seat = 100                                            #booking function redirect
    a =  request.form.get("fromm")
    des = request.form.get("to")
    date = request.form.get("sdate")
    end = request.form.get("edate")
    print(end)
    #total_seat = ava_seat-seat
    cursor.execute("SELECT * FROM plane WHERE plane_current_locatio ='%s' AND plane_destination='%s' AND start_date='%s' AND end_date='%s'" %(a,des,date,end))
    bok=cursor.fetchall()
    print(bok)
    if(bok == []):
        return render_template('booking.html')
    else:
        return render_template('details.html',value=bok)

@app.route('/private_booking' ,methods=['GET','POST'])
def private_booking():
    return render_template('private.html')

@app.route('/priprocess' ,methods=['GET','POST'])
def priprocess():
    dep = request.form.get("deparure")
    ret = request.form.get("return")

    print(ret)
    cursor.execute("SELECT * FROM plane WHERE start_date='%s' AND end_date='%s'" %(dep,ret))
    pridata = cursor.fetchall()
    print(pridata)
    if(pridata == []):
        return render_template('private.html')
    else:
        return render_template('list.html',value=pridata)

@app.route('/tracking' ,methods=['GET','POST'])
def tracking():                                   #tracking function
    return render_template('tracking.html')

@app.route('/result' ,methods=['GET','POST'])
def result():                                #result of tracking
    search = request.form.get("plane_search")
    t = search
    print (t)
    cursor.execute("SELECT * FROM plane WHERE plane_id = '%s'" % t)
    data = cursor.fetchall()
    cursor.execute("SELECT * FROM ticket WHERE user_mailid = '%s'" % t)
    data1 = cursor.fetchall()
    print(data1)
    if(data != []  ):
        #---------------------------------#
        return render_template("result.html",value=data)
    elif(data1 !=[]):
        return render_template('result1.html',value=data1)
    elif(data1 == []):
        return render_template("tracking.html")
    else:
        print(t)
        return render_template('tracking.html')
@app.route('/login' ,methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/loginpro',methods=['GET','POST'])
def loginpro():
    st="no user!"
    id = request.form.get("user_id")
    passw = request.form.get("pass")
    print(id)
    print(passw)
    cursor.execute("SELECT user_name,user_password FROM user WHERE user_name = '%s' and user_password='%s'" % (id,passw))
    userid = cursor.fetchall()
    #for i in userid:
    #    print(i)
    #print(i)
    #cursor.execute("SELECT user_password FROM user ")
    #passwd = cursor.fetchall()
    #print(passwd)
    #for i in passwd:

    #if((userid == []) & (passwd == [])):
        #print("hdugfjdnfd")
        #return render_template('signup.html')
    #elif(passw == passwd[0]):
        #print("dbfdjsf")
    if(userid == []):
        return render_template("signup.html",value=st)
    else:

        return render_template('indexa.html',value=id)
    #else:
        print("kk")
    #else
       #return render_template('signup.html')

@app.route('/signup' ,methods=['GET','POST'])
def signup():
    return render_template("signup.html")

@app.route('/signuppro',methods=['GET','POST'])
def signuppro():
    global phno
    global name
    global stri
    print("fne")
    name = request.form.get("user_name")
    addr = request.form.get("address")
    mail = request.form.get("mail")
    cursor.execute("select user_mailid from user where user_mailid='%s'" %mail)
    m=cursor.fetchall()
    stri="user exist!"
    if(m==[]):
        phno = request.form.get("phoneno")
        passw = request.form.get("pass")
        print(passw)
        cursor.execute("INSERT INTO user(user_name,user_address,user_mailid,user_phone_no,user_password) VALUES ('%s' ,'%s' , '%s' , '%s' ,'%s')" %(name,addr,mail,phno,passw))
        conn.commit()
        det=cursor.fetchall()
        print(det)
        return render_template('login.html',value=det)
    else:
        print(stri)
        return render_template('login.html',value=stri)

@app.route('/payment', methods=['GET','POST'])
def payment():
    planeid = request.form.get("ticket_id")
    cursor.execute("select plane_id from plane where plane_id=%s" %planeid)
    ii = cursor.fetchall()
    print(ii)
    if(ii == []):
        return render_template('private.html')
    else:
        return render_template('pay.html',value=ii)
@app.route('/done' ,methods=['GET','POST'])
def done():
    global ticketid
    ctype= request.form.get("card_type")
    hname= request.form.get("holder_name")
    cnumber= request.form.get("card_number")
    ccv= request.form.get("ccv")
    pno = request.form.get("phno")
    print(pno)
    cursor.execute("select * from user where user_phone_no=%s" %pno)
    ee=cursor.fetchall()
    print(ee)
    print(mk)
    print(ticketid)
    print(seat)
    cursor.execute("SELECT * FROM plane WHERE plane_id = '%s'" % ticketid)
    k=cursor.fetchall()
    print(k)
    for i in ee[0]:
        print(i)
    if(ee == []):
        return render_template('login.html')
    else:

        #k=['plane_name,plane_current_location,plane_destinatio,plane_sdate,plane_edate]
        a=ee[0][0]
        b=ee[0][1]
        c=ee[0][2]
        d=ee[0][3]
        e=k[0][1]
        f=k[0][2]
        g=k[0][3]
        h=k[0][4]
        im=k[0][5]
        cursor.execute("INSERT INTO ticket(user_name,user_address,user_mailid,plane_name,plane_current_location,plane_destinatio,plane_sdate,plane_edate,seat) VALUES ('%s' ,'%s' , '%s' ,'%s', '%s', '%s', '%s', '%s', %s) " %(a,b,c,e,f,g,h,im,seat))
        conn.commit()
        cursor.execute("select * from ticket where user_name='%s'" % a)
        qq=cursor.fetchall()
        print(qq)
    return render_template('ticket.html',value=qq)
@app.route('/final' , methods=['POST','GET'])
def final():
    global bok
    global seat
    global mk
    global ticketid
    ticketid = request.form.get("ticket_id")
    print (ticketid)
    cursor.execute("select available_seat from plane where plane_id='%s'" %ticketid)
    tid=cursor.fetchall()
    print(tid)
    print(tid[0][0])
    seat = request.form.get("seat")
    print(seat)
    se=tid[0][0]-int(seat)
    print(se)
    cursor.execute("update plane set available_seat='%s' where plane_id='%s'" %(se,ticketid) )
    conn.commit()
    print(ticketid)
    cursor.execute("SELECT * FROM plane WHERE plane_id = '%s'" % ticketid)
    mk=cursor.fetchall()
    print(mk)
    if( mk == []):
        return render_template('details.html',value=bok)
    else:
        return render_template("pay.html",value=mk)
