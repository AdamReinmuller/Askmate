from flask import Flask, request, render_template,

app = Flask(__name__)

app.run(debug=True, port=5000, host='0.0.0.0')