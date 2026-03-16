#  checks If api is running 
from flask import Flask

app= Flask(__name__)
@app.route("/")
def home():
    return"Lung cancer detection API running"

if __name__ =="__main__":
    app.run(debug=True)
