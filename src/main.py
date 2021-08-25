# coding=utf-8

from .entities.entity import Session, engine, Base
from .entities.node import Node

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
nodes = session.query(Node).all()

if len(nodes) == 0:
    # create and persist mock exam
    python_node = Node("SQLAlchemy Node", "Test your knowledge about SQLAlchemy.", "script")
    session.add(python_node)
    session.commit()
    session.close()

    # reload exams
    nodes = session.query(Node).all()

# show existing exams
print('### nodes:')
for node in nodes:
    print(f'({node.id}) {node.title} - {node.description}')
