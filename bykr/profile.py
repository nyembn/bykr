from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import pdb
from bykr.auth import login_required
from bykr.db import get_db
import pdb

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
    c.execute(
        'SELECT s.average_speed from statistics s JOIN post p ON s.post_id = p.id WHERE p.author_id=%s',
        [g.user[0],])
    average_speed_series = c.fetchall()

    c.execute(
        'SELECT p.created from post p JOIN statistics s ON p.id = s.post_id WHERE p.author_id = %s',
        [g.user[0],])
    timeData = c.fetchall()

    c.execute(
        'SELECT s.max_speed from statistics s JOIN post p ON s.post_id =p.id WHERE p.author_id=%s',
        [g.user[0],])
    max_speed_series = c.fetchall()

    return render_template('profile/ride_stats.html', average_speed_series=average_speed_series,
    max_speed_series = max_speed_series, timeData = timeData)
