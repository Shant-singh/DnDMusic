from flask import render_template

from app import app

# Error handlers
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def permission_error(error):
    return render_template('errors/403.html', error=error.description), 403