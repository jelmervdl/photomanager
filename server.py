from flask import Flask
from fs.osfs import OSFS, ResourceNotFoundError
from hashlib import md5
import json

class Photo(object):
	def __init__(self, path):
		self.id = md5(path).hexdigest()
		self.path = path

class PhotoEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__

def is_photo(path):
	return path[-3:].lower() == 'jpg'

app = Flask(__name__)

@app.route('/api/photos/<path:folder>')
def list_photos(folder):
	try:
		photo_fs = OSFS('~/Dropbox/Photos/' + folder)
		photos = []

		for photo in photo_fs.walkfiles():
			if is_photo(photo):
				photos.append(Photo(photo))

		return json.dumps(photos, indent=2, cls=PhotoEncoder)
	except ResourceNotFoundError as err:
		return json.dumps({'error': str(err)})

if __name__ == '__main__':
	app.run(debug=True)