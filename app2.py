from flask import Flask, jsonify, make_response, request
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'This is an API for tracking heroes and their superpowers.'

@app.route('/heroes', methods=['GET'])
def heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        heroes.append(hero_dict)
    response = make_response(
        jsonify(heroes),
        200
    )
    return response

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    hero_dict = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': []
    }
    for hero_power in hero.hero_powers:
        power_dict = {
            'id': hero_power.power.id,
            'name': hero_power.power.name,
            'description': hero_power.power.description
        }
        hero_dict['powers'].append(power_dict)

    return jsonify(hero_dict)

@app.route('/powers', methods=['GET'])
def powers():
    powers_list = []
    for power in Power.query.all():
        power_dict = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        powers_list.append(power_dict)

    response = make_response(
        jsonify(powers_list),
        200
    )
    return response

@app.route('/powers/<int:id>', methods=['GET'])
def fetch_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    power_dict = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }

    return jsonify(power_dict)

@app.route('/heroes/<int:id>', methods=['PATCH'])
def update_hero(id):
    data = request.get_json()
    hero = Hero.query.get(id)

    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    if 'name' in data:
        new_name = data['name']
        if not new_name:
            return jsonify({'error': 'Name cannot be empty'}), 400
        hero.name = new_name

    if 'super_name' in data:
        new_super_name = data['super_name']
        if not new_super_name:
            return jsonify({'error': 'Super name cannot be empty'}), 400
        hero.super_name = new_super_name

    db.session.commit()

    return jsonify({'message': 'Hero updated successfully'}), 200

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)

    if power is None:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    if "description" not in data:
        return jsonify({"errors": ["description field is required"]}), 400

    new_description = data["description"]

    # Update the power's description
    power.description = new_description

    try:
        db.session.commit()
        return jsonify({"id": power.id, "name": power.name, "description": power.description})
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    # Validate the required fields
    if "strength" not in data or "power_id" not in data or "hero_id" not in data:
        return jsonify({"errors": ["strength, power_id, and hero_id fields are required"]}), 400

    strength = data["strength"]
    power_id = data["power_id"]
    hero_id = data["hero_id"]

    # Check if the Power and Hero exist
    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)

    if power is None or hero is None:
        return jsonify({"errors": ["Power or Hero not found"]}), 404

    # Create a new HeroPower
    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    try:
        db.session.add(hero_power)
        db.session.commit()
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        response = make_response(
            jsonify(hero_data),
            200
        )
        return response
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555)
