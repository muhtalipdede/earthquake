from datetime import datetime
from flask import render_template
from app.api.get_fault_line import get_fault_line
from app.api.get_last_earthquake import get_last_earthquake
from app.api.get_magnitude_map import get_magnitude_map
from app.helpers.datetime_helper import DatetimeHelper

def index_mobile_page():
    df = get_last_earthquake()
    fault_line = get_fault_line()
    _magnitude_map = get_magnitude_map(df=df, fault_line=fault_line)

    date_str = df['date'][0]
    date = DatetimeHelper.format_datetime_str(date_str)
    address = df['address'][0]
    magnitude = df['magnitude'][0]
    dept = df['dept'][0]

    return render_template('mobile/index.html', magnitude_map=_magnitude_map, date=date, address=address, magnitude=magnitude, dept=dept)