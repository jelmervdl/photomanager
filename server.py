from flask import Flask
from fs.osfs import OSFS, ResourceNotFoundError
from hashlib import md5
from pexif import JpegFile
from datetime import datetime
import json

TIME_FORMAT = '%Y:%m:%d %H:%M:%S'

class Photo(object):
	def __init__(self, path, photo_fs):
		self.id = md5(path.encode('utf-8')).hexdigest()
		self.path = path

		with photo_fs.open(path, 'r') as fd:
			try:
				image = JpegFile.fromFd(fd)
				self.timestamp = datetime.strptime(image.exif.primary.DateTime, TIME_FORMAT)
				self.location = image.get_geo()
			except:
				pass


class PhotoEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.isoformat()
		elif isinstance(obj, Photo):
			return obj.__dict__


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
		photo_fs = OSFS('~/Pictures/Playground/' + folder)
		photos = []

		for photo in photo_fs.walkfiles():
			if is_photo(photo):
				photos.append(Photo(photo, photo_fs))

		return jsonify(photos)
	except ResourceNotFoundError as err:
		return jsonify({'error': unicode(err)})

if __name__ == '__main__':
	app.run(debug=True)