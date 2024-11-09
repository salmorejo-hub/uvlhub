from flask import render_template
from app.modules.api import api_bp
from flask_login import login_required, current_user

'''
@api_bp.route('/api', methods=['GET'])
def index():
    return render_template('api/index.html')


@api_bp.route('/api/configuration')
@login_required
def generate():
    print('Generating token')
    return render_template('api/index.html')
'''


@api_bp.route('/api/configuration')
@login_required
def index():
    return render_template('api/index.html')
