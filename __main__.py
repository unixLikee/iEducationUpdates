import json
from flask import Flask, Response
from Instagram import Instagram
import threading, time

#Constants
USERNAME = 'informatica.it'
HASHTAG = '#ied'
PORT = 80

#Flask init
app = Flask(__name__)

class updatePost(threading.Thread):
    def run(self):
        while (True):
            self.instagram = Instagram(USERNAME, HASHTAG)
            print('Updated')
            #Check for updates evert 30 secs
            time.sleep(30)

#Main route
@app.route("/")
def getPost():
    all = instaupdater.instagram.getAll()
    post = {
        'head': {
            'title': all[0],
            'timestamp': all[1],
            'image_link': all[2]
        },
        'body': {
            'text': all[3]
        }
    }

    response = Response(json.dumps(post))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Server'] = 'informatica.it'
    response.headers['Content-Type'] = 'application/json'
    return response

#getTitle's route
@app.route("/getTitle")
def getTitle():
    title = instaupdater.instagram.getAll()[0]
    post = {
        'head': {
            'title': title
        }
    }

    response = Response(json.dumps(post))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Server'] = 'informatica.it'
    response.headers['Content-Type'] = 'application/json'
    return response

#getTimestamp's route
@app.route("/getTimestamp")
def getTimestamp():
    timestamp = instaupdater.instagram.getAll()[1]
    post = {
        'head': {
            'timestamp': timestamp
        }
    }

    response = Response(json.dumps(post))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Server'] = 'informatica.it'
    response.headers['Content-Type'] = 'application/json'
    return response

#getImageLink's route
@app.route("/getImageLink")
def getImageLink():
    image_link = instaupdater.instagram.getAll()[2]
    post = {
        'head': {
            'image_link': image_link
        }
    }

    response = Response(json.dumps(post))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Server'] = 'informatica.it'
    response.headers['Content-Type'] = 'application/json'
    return response

#getText's post
@app.route("/getText")
def getText():
    text = instaupdater.instagram.getAll()[3]
    post = {
        'body': {
            'text': text
        }
    }

    response = Response(json.dumps(post))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Server'] = 'informatica.it'
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    #New thread
    instaupdater = updatePost()
    instaupdater.start()

    #Start flask's app
    app.run(debug = False, port = PORT)