from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from bykr.auth import login_required
from bykr.db import get_db
import mysql.connector

#Jeeves related import
#import JeevesLib
#from sourcetrans.macro_module import macros, jeeves


bp = Blueprint('blog', __name__)

"""
# [START upload_image_file]
def upload_image_file(file):
        if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url
# [END upload_image_file]
"""
@bp.route('/')
def index():
    db = get_db()
    c = db.cursor()
    c.execute(
        'SELECT p.id, title, body, created, author_id, username, bike_used,'
        ' average_speed, max_speed'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' LEFT JOIN statistics s ON p.id = s.post_id'
        ' ORDER BY created DESC'
    )
    #pdb.set_trace()
    posts = c.fetchall()
    #fetchall() fetches all (or all remaining) rows of a query result set and returns a list of tuples.
    return render_template('blog/index.html', posts=posts)
#what would be the case when there is a lot of posts?

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
	bike = request.form['bike_used']
	miles_biked = request.form['miles_biked']
        average_speed = request.form['average_speed']
        max_speed = request.form['max_speed']
        calories_burned = request.form['calories_burned']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            #C db = get_db()
            cnx = mysql.connector.connect(host='127.0.0.1', user='root', passwd='hello1234', db='bblog')
	    #C c = db.cursor()
        c = cnx.cursor()
        c.execute(
                'INSERT INTO post (title, body, author_id, bike_used)'
                ' VALUES (%s, %s, %s, %s)',
                [title, body, g.user[0], bike]
            )
        pid = c.lastrowid
        c.execute(
                'INSERT INTO statistics (post_id, miles_biked, average_speed, max_speed, calories_burned)'
                ' VALUES (%s, %s, %s, %s, %s)',
                [pid, miles_biked, average_speed, max_speed, calories_burned])
        cnx.commit()

        c.close()
        cnx.close()
        return redirect(url_for('blog.index'))
# Following is to extract the list of this users bike on GET
    else:
	#pdb.set_trace()
        db = get_db()
        c = db.cursor()
	c.execute(
		'SELECT manufacturer from bike b JOIN user_bike ub ON b.id = ub.bike_id '
		'WHERE ub.user_id = %s', [g.user[0],]
	)
	bikes = c.fetchall()
    return render_template('blog/create.html', bikes=bikes)

def get_post(id, check_author=True):
    db = get_db()
    c = db.cursor()
    c.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        [id,]
    )
    #pdb.set_trace()
    post = c.fetchone()
    #post = list(post_1)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    #pdb.set_trace()
    if check_author and post[4] != g.user[0]:
        abort(403)

    return post

#def average_speed()

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
	    c = db.cursor()
            c.execute(
                'UPDATE post SET title = %s, body = %s'
                ' WHERE id = %s',
                [title, body, id]
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    c = db.cursor()
    c.execute('DELETE FROM post WHERE id = %s', [id,])
    db.commit()
    return redirect(url_for('blog.index'))
