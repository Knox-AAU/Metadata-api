""" Metadataapi entrance file """
import os
import sys
import json
from uuid import uuid4
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified

app = Flask(__name__)

# Configure the Flask app to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') # pylint: disable=C0301
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy database instance
db = SQLAlchemy(app)

# Define a simple model
class Metadata(db.Model):
    """ Metadata table model """
    uuid = db.Column(db.String(36), primary_key=True)
    mdata = db.Column(db.JSON, nullable=False) # mdata because metadata is reserved in declarative flask apis

class TripleUUID(db.Model):
    """ Triple UUID model """
    uuids = db.Column(db.ARRAY(db.String(36)))
    triple = db.Column(db.String(2000), primary_key=True)

# Create tables
with app.app_context():
    db.create_all()

# Define a simple route
@app.route('/')
def index():
    """ Acts as a health check """
    return jsonify({ "success": True, "message": "Metadata api is healthy" })

@app.route('/metadata', methods=['POST'])
def add_metadata():
    """ 
        @description: Method to take in metadata and bind it together with a UUID in the database 
        @body: {
            metadata: object
        }
        @returns: uuid matching the metadata
    """
    try:
        data = request.get_json()

        uuid = str(uuid4())
        metadata = data.get('metadata')

        new_metadata = Metadata(uuid=uuid, mdata=metadata)

        db.session.add(new_metadata)
        db.session.commit()

        return jsonify({ 'success': True, 'message': uuid })

    except Exception as e:
        return jsonify({ 'success': False, 'message': str(e) })

@app.route('/metadata', methods=['GET'])
def get_metadata():
    """ 
        @description Method to take in a triple and return the metadata connected to this triple
        @body: {
            triple: array
        }
        @returns: metadata connected to specified triple
    """
    try:
        data = request.get_json()

        triple_as_pk = data['triple'][0] + data['triple'][1] + data['triple'][2]

        uuid = db.session.execute(db.select(TripleUUID).filter_by(triple=triple_as_pk)).scalar()

        if uuid.uuids:
            metadata = Metadata.query.filter(Metadata.uuid.in_(uuid.uuids)).all()

            if metadata:
                res = []

                for data in metadata:
                    res.append(data.mdata[0])

                return jsonify({'success': True, 'message': res })

            return jsonify({'success': False, 'message': f'No metadata found connected to UUID: {uuid.uuids}'})

        return jsonify({'success': False, 'message': f'No UUID found connected to Triple: {triple_as_pk}'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e) })

@app.route('/triple', methods=['POST'])
def add_triple():
    """ 
        @description Method to take in a UUID and a triple and bind it together in a database 
        @body: {
            uuid: string,
            triple: array
        }
        @returns: triple in the format that was inserted as primary key
    """
    try:
        data = request.get_json()

        uuid = data.get('uuid')
        triple = data.get('triple')

        triple_as_pk = triple[0] + triple[1] + triple[2]

        uuid_array_from_pk = db.session.execute(db.select(TripleUUID).filter_by(triple=triple_as_pk)).scalar()

        if uuid_array_from_pk:
            # Add UUID to array of UUIDS
            if uuid_array_from_pk.uuids:
                if uuid in uuid_array_from_pk.uuids:
                    # If UUID is already in array of UUIDS
                    return jsonify({ 'success': False, 'message': f"UUID: {uuid} already exists!" })

                uuid_array_from_pk.uuids.append(uuid)
                flag_modified(uuid_array_from_pk, 'uuids')

        else:
            # Create new triple instance
            new_triple = TripleUUID(uuids=[uuid], triple=triple_as_pk)
            db.session.add(new_triple)

        db.session.commit()

        return jsonify({ 'success': True, 'message': triple_as_pk })

    except Exception as e:
        return jsonify({ 'success': False, 'message': str(e) })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('PYTHON_ENV', '').lower() == 'development')
