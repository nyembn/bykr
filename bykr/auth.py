import functools
import pdb
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bykr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        c = db.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        c.execute(
            'SELECT id FROM user WHERE username = %s', [username,]
        )
        ur = c.fetchone()
        if ur is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            c.execute(
                'INSERT INTO user (username, password) VALUES (%s, %s)',
                [username, generate_password_hash(password)]
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        c= db.cursor()
        c.execute(
            'SELECT * FROM user WHERE username = %s', [username,]
        )
        user = c.fetchone()
        if user is None:
            error = 'Incorrect username'
        if not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[1]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login_ti.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        c = db.cursor()
        c.execute(
            'SELECT * FROM user WHERE username = %s', [user_id,]
        )
	#pdb.set_trace()
        g.user = c.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
