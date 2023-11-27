# pylint: skip-file 

""" Metadataapi entrance file """

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the Flask app to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@metadataapi_database:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy database instance
db = SQLAlchemy(app)

# Define a simple model
class Metadata(db.Model):
    """ Metadata table model """
    uuid = db.Column(db.String(40), primary_key=True)
    mdata = db.Column(db.JSON, nullable=False) # mdata because metadata is reserved in declarative flask apis

class TripleUUID(db.Model):
    """ Triple UUID model """
    uuid = db.Column(db.String(40))
    triple = db.Column(db.String(2000), primary_key=True)

# Create tables
with app.app_context():
    db.create_all()

# Define a simple route
@app.route('/')
def index():
    """ Acts as a health check """
    return jsonify({ "success": True, "message": os.environ['PYTHON_ENV']})

@app.route('/binduuid', methods=['POST'])
def binduuid():
    try:
        # Takes json input
        data = request.get_json()
        
        uuid = data.get('uuid')
        # [{ "author": "John Snut", "pages": 420 },{ "author": "Snut John" },{ "pages": 69 }]
        metadata = data.get('metadata')
        
        new_metadata = Metadata(uuid=uuid, mdata=metadata)
        
        db.session.add(new_metadata)
        db.session.commit()

        return jsonify({'success': True, 'message': f'Saved metadata to database under UUID {uuid}'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/bindtriple', methods=['POST'])
def bindtriple():
    try:
        data = request.get_json()
        
        uuid = data.get('uuid')
        triple = data.get('triple')
        
        triple_as_pk = triple[0] + triple[1] + triple[2]
        
        new_triple = TripleUUID(uuid=uuid, triple=triple_as_pk)
        
        db.session.add(new_triple)
        db.session.commit()

        return jsonify({'success': True, 'message': f'Saved data to database under triple {triple_as_pk}'})

        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/getMetadata')
def getMetadata():
    try:
        data = request.get_json()
                
        triple_as_pk = data['triple'][0] + data['triple'][1] + data['triple'][2]
        
        uuid = db.session.execute(db.select(TripleUUID).filter_by(triple=triple_as_pk)).scalar()        
        
        if uuid.uuid:
            metadata = db.session.execute(db.select(Metadata).filter_by(uuid=uuid.uuid)).scalar()
            # metadata = Metadata.query.get(uuid)
                        
            if metadata.mdata:
                return jsonify({'success': True, 'message': metadata.mdata})
            
            else:
                return jsonify({'success': False, 'message': f'No metadata found connected to UUID: {uuid.uuid}'})
        
        else:
            return jsonify({'success': False, 'message': f'No UUID found connected to Triple: {triple_as_pk}'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': e})

# TESTING ROUTES - REMOVE BITTE #
@app.route('/getuuids')
def getuuids():
    try:
        
        mdata = Metadata.query.all()
        uuidList = [{'uuid': d.uuid, 'metadata': d.mdata} for d in mdata]
        
        return {'success': True, 'message': uuidList}
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/gettriples')
def gettriples():
    try:
        
        triples = TripleUUID.query.all()
        triplesList = [{'uuid': d.uuid, 'triple': d.triple} for d in triples]
        
        return {'success': True, 'message': triplesList}
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/test')
def test():
    return {"snut": "bas"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('PYTHON_ENV', '').lower() == 'true')