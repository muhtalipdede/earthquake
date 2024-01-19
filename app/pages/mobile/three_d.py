from flask import render_template

from app.api.get_three_d_map import get_three_d_map

def three_d_mobile_page():
    _three_d_map = get_three_d_map()
    return render_template('mobile/three_d.html', three_d_map=_three_d_map)