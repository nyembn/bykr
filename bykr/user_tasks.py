from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import pdb


bp = Blueprint('user_tasks', __name__, url_prefix='/user_tasks')

@bp.route('/add_bike_db', methods=('GET', 'POST'))
@login_required
def add_bike_db():
    if request.method == 'POST':
        #pdb.set_trace()
        manufacturer = request.form['manufacturer']
        error = None


        if not manufacturer:
            error = 'Manufacturer is required.'

        ##if error is not None:
        ##flash(error)
        else:
            db = get_db()
            c = db.cursor()
	    c.execute(
                'INSERT INTO bike (manufacturer)'
                ' VALUES (%s)',
                [manufacturer,]
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('user_tasks/add_bike_db.html')

@bp.route('/add_bike_to_profile', methods=('GET', 'POST'))
@login_required
def add_bike_profile():
    if request.method == 'GET':
        db = get_db()
	c = db.cursor()
        c.execute(
            'SELECT id, manufacturer'
            ' FROM bike'
        )
	bikes = c.fetchall()
	#bikes = list(bikes_1)
        return render_template('user_tasks/add_bike_profile.html', bikes=bikes)
    else: 
        user_bike = request.form['bikes']
        db = get_db()
	c = db.cursor()
	error = None
	c.execute(
            'SELECT user_id, bike_id FROM user_bike WHERE user_id = %s AND bike_id = %s', [g.user[0], user_bike])
	ub = c.fetchone()
	#pdb.set_trace()

	if ub is not None:
	    error = 'Bike {} is already added.'.format(user_bike)
	    flash(error)
	if error is None:
		c.execute('INSERT INTO user_bike (user_id, bike_id) VALUES (%s, %s)', [g.user[0], user_bike])
        	db.commit()
		success_message = 'Bike {} added to your profile'.format(user_bike)
		flash(success_message)
		#return redirect('user_tasks/add_bike_profile.html')
    c.execute(
        'SELECT id, manufacturer'
        ' FROM bike'
    )
    bikes = c.fetchall()
    #bikes = list(bikes_1)
    return render_template('user_tasks/add_bike_profile.html', bikes=bikes)
