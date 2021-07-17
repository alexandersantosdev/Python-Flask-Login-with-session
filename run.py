from app import app, db

def init():
    db.create_all()
    app.run(debug=True)