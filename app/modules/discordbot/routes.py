from flask import render_template
from app.modules.discordbot import discordbot_bp


@discordbot_bp.route('/discordbot', methods=['GET'])
def index():
    return render_template('discordbot/index.html')
