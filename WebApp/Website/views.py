from flask import Blueprint, render_template, request
from flask.helpers import flash
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Note

views = Blueprint('views',__name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        time = request.args.get('time')
        print("hello from views.py")
        if len(note) <2:
            flash('Too small to be a note','error')
        else:
            new_note = Note(data = note, user_id = current_user.id)
            flash('Note Added')
    return render_template("home.html", User= current_user)