from flask import render_template
from app.api.get_earthquake import get_earthquake
from app.api.get_fault_line import get_fault_line
from app.api.get_magnitude_map import get_magnitude_map

def earthquake_mobile_page(last_day):
    df = get_earthquake(last_day=last_day)
    fault_line = get_fault_line()
    _magnitude_map = get_magnitude_map(df=df, fault_line=fault_line)
    return render_template("mobile/earthquake.html", magnitude_map=_magnitude_map, last_day=last_day)