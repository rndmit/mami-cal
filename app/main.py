from flask import (Blueprint, flash, g, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask import current_app as app

import app.parser as parser
import app.ical as ical

bp = Blueprint('main', __name__, url_prefix='/', static_folder='/static')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/request-ics', methods=['POST'])
def request_ics():
   if request.method == 'POST':
      target = request.form['group']
      result = parser.get_data(target)
      if result:
        ical.save_to_ics(ical.build(result), f'{target}.ics')
   return redirect(f'/download-ics/{target}.ics')

@bp.route('/download-ics/<path:filename>')
def download_ics(filename):
    return send_from_directory(app.config['ICS_STORAGE_FOLDER'], filename, as_attachment=True)
