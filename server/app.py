from flask import Flask, jsonify, request,  make_response
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return 'This is an API for tracking heroes and their superpowers.'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.to_dict())

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.to_dict())

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    data = request.json
    if 'description' in data:
        description = data['description']
        if len(description) < 20:
            return jsonify({'errors': ['Description must be at least 20 characters long']}), 400
        power.description = description
    
    db.session.commit()
    return jsonify(power.to_dict())

@app.route('/hero_powers', methods=['POST'])
def add_hero_power():
    data = request.json
    try:
        hero_power = HeroPower(**data)
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 201
    except AssertionError as e:
        return jsonify({'errors': [str(e)]}), 400


if __name__ == '__main__':
    app.run(port=5000, debug=True)
