from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    # Itt kezelheted a játék logikáját
    return jsonify(status="game running")

if __name__ == '__main__':
    app.run(debug=True)

