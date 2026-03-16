#  checks If api is running 
from flask import Flask


#  creating a flask application instance 
# flask is the web framework that will run the backend server 
app= Flask(__name__)

# define a route for the home page 
# when someone visits http:127.0.0.1:5000/ 
# tis function will run 
@app.route("/")
def home():
    #  returning a message to confirmm API is running 
    return"Lung cancer detection API running"

#  This ensures the Flask server runs only when this file is exacuted directly 
#  and not when it is imported by any other file 

if __name__ =="__main__":
    #  start the Flask server 
    #  debug=True automatically reloads the server when the code changes 
    app.run(debug=True)
