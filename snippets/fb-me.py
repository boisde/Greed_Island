from flask import Flask, redirect, url_for,jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.secret_key = "e4d12595a78cd5c79fac4e75c7660138" #Just your personal App key.

blueprint = make_facebook_blueprint(
    client_id="471544776657489", #Put Your App ID 
    client_secret="e4d12595a78cd5c79fac4e75c7660138", #Put Your App Secret
    scope=['user_birthday'] #Define the list you want to access of user's info they will be prompted to allow. Get the list from fb developer's page
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/signup/fb")
def fbSignup():
   if not facebook.authorized:
      return redirect(url_for("facebook.login"))
   else:
      return "<h2>logged in to fb</h2>" 

      
@app.route('/',methods=['GET'])
def getUserNameOfGithub():
   if facebook.authorized:
      resp = facebook.get("/me?fields=gender,birthday")
      id = resp.json()["id"]
      return resp.json()["birthday"]
   else:
      return "<h1> you are not logged in</h1>"
      
@app.after_request
def after(response):
   print(response.get_data())
   return response
        
if __name__ == "__main__":
   app.run(debug=True,ssl_context='adhoc') #Enabling ssl mode for testing as FB doesn't allow http url callbacks.