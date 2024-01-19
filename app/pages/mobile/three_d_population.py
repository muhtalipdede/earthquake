from flask import render_template


def three_d_population_mobile_page():
    _three_d_map = get_three_d_population_map()
    return render_template('mobile/three_d.html', three_d_map=_three_d_map)