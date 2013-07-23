from flask import Flask
from fs.osfs import OSFS
import json

class Photo(object):
	def __init__(self, path):
		self.path = path

class PhotoEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__

def is_photo(path):
	return path[-3:].lower() == 'jpg'

app = Flask(__name__)

@app.route('/api/photos/all')
def list_photos():
	photo_fs = OSFS('~/Dropbox/Photos/2013')
	photos = []

	for photo in photo_fs.walkfiles():
		if is_photo(photo):
			photos.append(Photo(photo))

	return json.dumps(photos, indent=2, cls=PhotoEncoder)

if __name__ == '__main__':
	app.run(debug=True)