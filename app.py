#!/usr/bin/env python

from flask import Flask, request, jsonify
from seiren.services.ranked_items import add_item, find_items, find_item, remove_item, update_item_rank, find_due_items
from flask_migrate import Migrate
from seiren.database import db
import json

app = Flask("seiren")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app, db)

with app.app_context():
    # db.drop_all()
    db.create_all()

@app.route('/ranked_items', methods=['GET'])
def get_items():
    items = find_items()
    message = f"Item: {items}"
    return jsonify({"message": message})

@app.route('/ranked_items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item(item_id)
    message = f"Item: {item}"
    return jsonify({"message": message})

@app.route('/ranked_items/due/<int:limit>', methods=['GET'])
def get_due_items(limit):
    items = find_due_items(10)
    message = f"Item: {items}"
    return jsonify({"message": message})

@app.route('/ranked_items', methods=['POST'])
def create_item():
    item = request.json['item']
    item = add_item(item)
    return jsonify({"message": f"Item created successfully. ${item}"})

@app.route('/ranked_items/review', methods=['POST'])
def review_item():
    item_id = request.json['item_id']
    quality = request.json['quality']
    item = update_item_rank(item_id, quality)
    return jsonify({"message": f"Item reviewed successfully. ${item.serialize()}"})

@app.route('/ranked_items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    remove_item(item_id)
    return jsonify({"message": f"Item deleted successfully. ${item_id}"})

if __name__ == '__main__':
    app.run(debug=True)
