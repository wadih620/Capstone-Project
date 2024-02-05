from flask import Flask, render_template
from training_level1 import setup1, level1
from training_level2 import setup2, level2
from training_level3 import setup3, level3
from voiceRec_mode import setupV, voice

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


@app.get('/auto')
def level1_get():
    print("level1 MODE - GET")
    return render_template('main.html')


# IS CALLED WHEN level1 BUTTON IS PRESSED
@app.post('/level1')
def level1_post():
    print("level1 MODE - POST")
    setup1()
    level1()
    return render_template('main.html')


# IS CALLED WHEN STOP level1 BUTTON IS PRESSED
@app.post('/stop-level1')
def stop_level1():
    print("STOPPING level1 MODE")
    return render_template('main.html')

@app.get('/level2')
def level2_get():
    print("level2 MODE - GET")
    return render_template('main.html')


# IS CALLED WHEN level2 BUTTON IS PRESSED
@app.post('/level2')
def level2_post():
    print("level2 MODE - POST")
    setup2()
    level2()
    return render_template('main.html')


# IS CALLED WHEN STOP level2 BUTTON IS PRESSED
@app.post('/stop-level2')
def stop_level2():
    print("STOPPING level2 MODE")
    return render_template('main.html')

@app.get('/level3')
def level3_get():
    print("level3 MODE - GET")
    return render_template('main.html')


# IS CALLED WHEN level3 BUTTON IS PRESSED
@app.post('/level3')
def level3_post():
    print("level3 MODE - POST")
    setup3()
    level3()
    return render_template('main.html')


# IS CALLED WHEN STOP level3 BUTTON IS PRESSED
@app.post('/stop-level3')
def stop_level3():
    print("STOPPING level3 MODE")
    return render_template('main.html')


@app.get('/voice')
def voice_rec_get():
    print("VOICE RECOGNITION MODE - GET")
    return render_template('main.html')


# IS CALLED WHEN VOICE REC BUTTON IS PRESSED
@app.post('/voice')
def voice_rec_post():
    print("VOICE RECOGNITION MODE - POST")
    setupV()
    voice()
    return render_template('main.html')


# IS CALLED WHEN STOP VOICE REC BUTTON IS PRESSED
@app.post('/stop-voice')
def stop_voice():
    print("STOPPING VOICE RECOGNITION MODE")
    return render_template('main.html')


if __name__ == "__main__":
    print("Server Starting ...")
    app.run(host="0.0.0.0")

    # For PyCharm
    #app.run()
