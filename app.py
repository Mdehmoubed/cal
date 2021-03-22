from flask import Flask, render_template, request, session ,url_for,redirect,flash ,logging ,jsonify,json

import sqlite3 as sql
from functools import wraps
import time

#from passlib.hash import sha256_crypt

app = Flask(__name__)
DATABASE ='/mdn1.db'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('home1.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash( Please login')
            return redirect(url_for('login'))
    return wrap



@app.route('/register')
def ne():
    return render_template('register.html',msg='')#chang with flash 
@app.route('/aduser', methods=['POST','GET'])
def adduser():
    if request.method =='POST':
        try:
            uname=request.form['uname']
            psw=request.form['psw']
            iemail=request.form['iemail']
            lname=request.form['lname']
            fname=request.form['fname']
            print(uname +","+ psw +","+ fname +","+lname+","+iemail)
            with sql.connect("mdn1.db") as con:
                cur=con.cursor()
                cur.execute('INSERT INTO users(username,password,email,lname,fname) VALUES (?,?,?,?,?)', (uname,psw,iemail,lname,fname))
                con.commit()
                msg=''
        except:
            con.rollback()
            msg = 'error in insertion'
        finally:
            con.close()
            if msg=='' :
                #return render_template('account.html',username =uname)
                return redirect('/')
            else:
                print(msg)
                return render_template('register.html',msg = msg)
    else:
        return       



@app.route('/login')
def no():
    return render_template('login.html',msg='')#chang with flash 
@app.route('/login1', methods=['POST','GET'])
def logi():
    if request.method =='POST':
        uname=request.form['uname']
        psw=request.form['psw']
        con=sql.connect("mdn1.db")
        cur=con.cursor()
        cur.execute("select password from users where username = ?",(uname,))
        retrive=cur.fetchall()
        con.close()
        if len(retrive)>0 :
           if retrive[0][0]== psw :
               session['logged_in'] = True
               session['username'] = uname 
               print("ok")
               return redirect(url_for('dashboard')) 
           else :
                error ='invalid login'
                print(error)                
                return render_template('register.html',msg = error)
        else :
            error ='username not found'
            return render_template('register.html',msg = error)
    else :
        return                


##account
@app.route('/account')
@is_logged_in
def dashboard():   
    con=sql.connect("mdn1.db")
    cur=con.cursor()
    cur.execute("select * from users where username = ?",(session['username'],))
    user=cur.fetchall()
    cur.execute("select * from event where username = ?",(session['username'],))
    events =cur.fetchall()
    con.close()
    #print(events)
    return render_template('account.html',user = user,events=events)



##logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    #flash
    return redirect('/login')



##reciver for del and edit and add events

@app.route('/postmethod1', methods = ['POST'])
@is_logged_in
def gda():
    jsd = json.loads(request.form['id'])
    con=sql.connect("mdn1.db")
    cur=con.cursor()
    if(jsd['st'] =='edit' or jsd['st'] =='add'):
        name=jsd['name']
        address=jsd['address']
        uname=session['username']
        date=jsd['date']
        start=jsd['start']
        end=jsd['end']
    
    if (jsd['st'] =='edit'):
        event_id=int(jsd['ido'])
        cur.execute('UPDATE event SET eventname=?,address=?,username=?,date=?,start=?,end=? WHERE eventID=?',(name,address,uname,date,start,end,event_id))
     
    if (jsd['st']=='add'):
        cur.execute('INSERT INTO event(eventname,address,username,date,start,end) VALUES (?,?,?,?,?,?)',(name,address,uname,date,start,end))
    
    if (jsd['st']=='del'):
        a=int(jsd['ido'])
        cur.execute('DELETE FROM event WHERE eventID = ?;',(a,))
     
    con.commit()
    con.close()
    return jsd


if '__name__'=='__main__':
    
    app.run(debug=True)