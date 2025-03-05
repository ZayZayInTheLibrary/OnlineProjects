from flask import Flask, render_template, request, jsonify, url_for, redirect

app = Flask(__name__)


guild_id = "1341546870740095006"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bot')
def send_text():
    text = request.args.get('text')
    print("Flask received text:", text)
    return redirect(url_for('trigger', text=text, guild_id=guild_id))

@app.route('/dreamer_bot')
def send_dreamer_text():
    text = request.args.get('text')
    print("Flask received text:", text)
    return redirect(url_for('trigger_dream', text=text, guild_id="1324513122698133565"))    



def run_flask(port="5001"):
    # Running with use_reloader=False prevents spawning multiple threads.
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

if __name__ == "__main__":
    run_flask()
