# coding=utf-8

from flask import Flask, jsonify, request

from .entities.entity import Session, engine, Base
from .entities.node import Node, NodeSchema

# creating the Flask application
app = Flask(__name__)

# if needed, generate database schema
Base.metadata.create_all(engine)


@app.route('/nodes')
def get_nodes():
    # fetching from the database
    session = Session()
    node_objects = session.query(Node).all()

    # transforming into JSON-serializable objects
    schema = NodeSchema(many=True)
    nodes = schema.dump(node_objects)

    # serializing as JSON
    session.close()
    return jsonify(nodes)


@app.route('/nodes', methods=['POST'])
def add_node():
    # mount node object
    posted_node = NodeSchema(only=('title', 'description')).load(request.get_json())

    node = Node(**posted_node, created_by="HTTP post request")

    # persist node
    session = Session()
    session.add(node)
    session.commit()

    # return created node
    new_node = NodeSchema().dump(node)
    session.close()
    return jsonify(new_node), 201
