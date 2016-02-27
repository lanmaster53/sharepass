from flask import request, redirect, url_for, render_template, jsonify, abort, flash
from sharepass import app, db
from decorators import nocache
from models import Password
from utils import get_token, send_share
from datetime import datetime

# password validation

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/share', methods=['POST'])
@nocache
def share():
    if request.method == 'POST':
        pw = Password(
            hash=get_token(10),
            cipher=request.form.get('cipher'),
            comment=request.form.get('comment'),
        )
        db.session.add(pw)
        db.session.commit()
        msg = 'Send the following link to the recipient.'
        email = request.form.get('email')
        if email:
            send_share(email, pw)
            msg = 'The following link has been sent to the recipient.'
        flash('Password added.')
        return render_template('share.html', password=pw, message=msg)
    return redirect(url_for('index'))

@app.route('/password/<string:hash>')
@nocache
def password(hash):
    pw = Password.get_by_hash(hash)
    if pw:
        # remove the password on access
        db.session.delete(pw)
        db.session.commit()
        delta = datetime.now() - pw.created
        delta = delta.seconds + delta.days * 86400
        if delta < app.config['PASSWORD_TTL']:
            return render_template('password.html', password=pw)
    abort(404)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
