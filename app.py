from flask import Flask, render_template, session, redirect,request,flash
from functools import wraps
from neuralintents import GenericAssistant
import pymongo
import speech_recognition as sr
import pyttsx3 as tts
#import pywhatkit
from datetime import datetime
import wikipedia
import pyjokes
from bson import ObjectId


app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc3'
# Database
client = pymongo.MongoClient('localhost', 27017)
db = client["python_EVA_DB"]
todos = db.todo # todo collection


#todolist


# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')

  return wrap

# login Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')

# speech_recognition route
@app.route('/assistantUI/')
def assistantUI():
        flash(" HELLO I AM EVA, YOUR VIRTUAL ASSISTANT, HOW CAN I HELP YOU")
        return render_template('assistantUI.html')

@app.route('/audio_to_text/')
def audio_to_text():
    flash(" Press Start to start recording audio and press Stop to end recording audio")
    return render_template('audio_to_text.html')

@app.route('/audio', methods=['POST'])
def audio():
    r = sr.Recognizer()
    with open('upload/audio.wav', 'wb') as f:
        f.write(request.data)

    with sr.AudioFile('upload/audio.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='en-IN', show_all=True)
        print(text)
        return_text = " Did you say : <br> "
        try:
            for num, texts in enumerate(text['alternative']):
                return_text += str(num+1) +") " + texts['transcript']  + " <br> "
        except:
            return_text = " Sorry!!!! Voice not Detected "

    return str(return_text)


#@app.route('/notes/', methods=["GET", "POST"])
#def notes():
#    return render_template('notes.html')
#Display the all Tasks
date_time= datetime.today().strftime('%Y-%m-%d')
def redirect_url():
    return request.args.get('next') or request.referrer or url_for('list')

@app.route("/list/")
def lists ():
	todos_l = todos.find()
	a1="active"
	return render_template('notes.html',a1=a1,todos=todos_l,date_time=date_time)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/list")

@app.route("/update")
def update ():
    id = request.values.get("_id")
    print(id)
    task=todos.find({"_id":ObjectId(id)})
    print(task)
    return render_template('update.html',tasks=task)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	# Re-directed URL i.e. PREVIOUS URL from where it came into this one

#	if(str(redir)=="http://localhost:5000/search"):
#		redir+="?key="+id+"&refer="+refer

	return redirect(redir)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
	return redirect("/list")
