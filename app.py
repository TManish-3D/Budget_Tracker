from main import app, db
import os

if __name__ == '__main__':
    if not os.path.exists('budget.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)