from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import pdb
from bykr.auth import login_required
from bykr.db import get_db

bp = Blueprint('profile', __name__)

@bp.route('/profile')
@login_required
def profile():
	db = get_db()
	c = db.cursor()
	c.execute(
		'SELECT manufacturer from bike b JOIN user_bike ub ON b.id = ub.bike_id '
		'WHERE ub.user_id = %s', [g.user[0],]
	)
	
	bikes = c.fetchall()
	return render_template('profile/profile.html', bikes = bikes)

@bp.route('/profile/ride_stats')
@login_required
def ride_stats():
	db = get_db()
	c = db.cursor()
	c.execute('SELECT average_speed from post WHERE author_id=%s',
		  [g.user[0],])
	series = c.fetchall()
	
	return render_template('profile/ride_stats.html', series=series)
