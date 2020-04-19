from django.shortcuts import render
import pyrebase
from django.contrib import auth
config = {
    'apiKey': "AIzaSyAP5OhqpTQ_khPNQ5W8tfQYWy8WJ9mxqBE",
    'authDomain': "easyfiles1-71702.firebaseapp.com",
    'databaseURL': "https://easyfiles1-71702.firebaseio.com",
    'projectId': "easyfiles1-71702",
    'storageBucket': "easyfiles1-71702.appspot.com",
    'messagingSenderId': "742424831590",
    'appId': "1:742424831590:web:63ecf439b0978bcf3d2fa7",
    'measurementId': "G-D2R6Q5YHCW"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

def signIn(request):
    return render(request, "signIn.html")
def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"signIn.html",{"msg":message})

    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "welcome.html",{"e":email})
def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')
def signUp(request):
    return render(request,"signup.html")
def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passw)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"msg":message})
    uid = user['localId']
    data={"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")
def create(request):
    return render(request,'create.html')
def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    Name_of_Folder = request.POST.get('Name_of_Folder')
    Reason_to_create_folder =request.POST.get('Reason_to_create_folder')
    url = request.POST.get('url')
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        "Name_of_Folder":Name_of_Folder,
        "Reason_to_create_folder":Reason_to_create_folder,
        "url":url
}
    database.child('users').child(a).child('reports').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})
def check(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    timestamps = database.child('users').child(a).child('reports').shallow().get().val()
    lis_time=[]
    for i in timestamps:

        lis_time.append(i)

    lis_time.sort(reverse=True)

    print(lis_time)
    Name_of_Folder = []

    for i in lis_time:

        wor=database.child('users').child(a).child('reports').child(i).child('Name_of_Folder').get().val()
        Name_of_Folder.append(wor)
    print(Name_of_Folder)

    date=[]
    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    print(date)

    comb_lis = zip(lis_time,date,Name_of_Folder)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'check.html',{'comb_lis':comb_lis,'e':name})

def post_check(request):

    import datetime

    time = request.GET.get('z')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    Name_of_Folder =database.child('users').child(a).child('reports').child(time).child('Name_of_Folder').get().val()
    Reason_to_create_folder =database.child('users').child(a).child('reports').child(time).child('Reason_to_create_folder').get().val()
    url=database.child('users').child(a).child('reports').child(time).child('url').get().val()
    print(url)
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    name = database.child('users').child(a).child('details').child('name').get().val()

    #return render(request,'post_check.html',{'w':Name_of_Folder,'p':Reason_to_create_folder,'d':dat,'e':name})

    return render(request,'post_check.html',{'w':Name_of_Folder,'p':Reason_to_create_folder,'d':dat,'e':name,'i':url})
