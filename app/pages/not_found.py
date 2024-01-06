from flask import render_template

def not_found_page(e):
    return render_template('404.html', e=e), 404