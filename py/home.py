from flask import Blueprint, render_template, flash, url_for, redirect, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .create import db
#pagina iniziale prima del login
home = Blueprint('home', __name__)

@home.route('/')
def prova():
	return render_template("index.html")
