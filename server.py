from flask import Flask
from fs.osfs import OSFS, ResourceNotFoundError
from hashlib import md5
import json

class Photo(object):
	def __init__(self, path):
		self.id = md5(path.encode('utf-8')).hexdigest()
		self.path = path

class PhotoEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__

def is_photo(path):
	return path[-3:].lower() == 'jpg'

def jsonify(data):
	return json.dumps(data, indent=2, cls=PhotoEncoder, ensure_ascii=False).encode('utf-8')

app = Flask(__name__)

@app.route('/api/photos/')
def list_all_photos():
	return list_photos('')

@app.route('/api/photos/<path:folder>')
def list_photos(folder):
	try:
		photo_fs = OSFS('~/Dropbox/Photos/Organized/' + folder)
		photos = []

		for photo in photo_fs.walkfiles():
			if is_photo(photo):
				photos.append(Photo(photo))

		return jsonify(photos)
	except ResourceNotFoundError as err:
		return jsonify({'error': unicode(err)})

if __name__ == '__main__':
	app.run(debug=True)