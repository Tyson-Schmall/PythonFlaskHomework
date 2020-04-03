from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Entertainment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(144), unique=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description


class EntertainmentSchema(ma.Schema):
    class Meta:
        fields = ('title', 'description')


entertainment_schema = EntertainmentSchema()
entertainments_schema = EntertainmentSchema(many=True)

# Endpoint to add new entertainment recommendations.
@app.route('/add_content', methods=["POST"])
def add_entertainment():
    title = request.json['title']
    description = request.json['description']

    new_entertainment = Entertainment(title, description)

    db.session.add(new_entertainment)
    db.session.commit()

    entertainment = Entertainment.query.get(new_entertainment.id)

    return entertainment_schema.jsonify(entertainment)


# Endpoint to query all entertainment recommendations.
@app.route("/display_all", methods=["GET"])
def get_entertainment():
    all_entertainment = Entertainment.query.all()
    result = entertainments_schema.dump(all_entertainment)
    return jsonify(result)


# Endpoint for querying a single entertaining show.
@app.route("/display_one/<id>", methods=["GET"])
def get_guide(id):
    entertainment = Entertainment.query.get(id)
    return entertainment_schema.jsonify(entertainment)


# Endpoint for updating an entertainment file
@app.route("/entertainment/<id>", methods=["PUT"])
def entertainment_update(id):
    entertainment = Entertainment.query.get(id)
    title = request.json['title']
    description = request.json['description']

    entertainment.title = title
    entertainment.description = description
    
    db.session.commit()
    return entertainment_schema.jsonify(entertainment)

# Endpoin for deleting a record
@app.route("/entertainment/<id>", methods=["DELETE"])
def entertainment_delete(id):
    entertainment = Entertainment.query.get(id)
    db.session.delete(entertainment)
    db.session.commit()

    return entertainment_schema.jsonify(entertainment)

if __name__ == '__main__':
    app.run(debug=True)