from flask import Flask
from Routes import initialise_routes

app = Flask(__name__)
app.secret_key = 'ahndffhioafhaoiaiojdf'

initialise_routes(app)

if __name__ == "__main__":
    app.run(debug=True)