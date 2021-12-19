import math
from flask import render_template,request, redirect, url_for, session, jsonify
from PhongKhamTu import app
import utils
from PhongKhamTu.admin import *
from flask_login import login_user, logout_user, login_required

@app.route("/")
def index():
    return render_template('index1.html')


if __name__ == "__main__":
    app.run(debug=True)