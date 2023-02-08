import os
import sqlalchemy as db

from dotenv import load_dotenv

from flask import Flask
from flask import render_template

from sqlalchemy import MetaData
from sqlalchemy import text

load_dotenv()

meta = MetaData()
engine = db.create_engine(os.getenv('DATABASE_URI'))

def create_app():
    app = Flask(__name__)
    return app


app = create_app()

@app.route('/')
def index():

    with engine.connect() as con:
        query = "SELECT * FROM student"
        rs = con.execute(text(query))
    return render_template('index.html', students_list = rs)


app.run(debug=True)
