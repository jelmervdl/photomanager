class Photo extends Backbone.Model

class PhotoCollection extends Backbone.Collection
	model: Photo
	url: '../api/photos/all'

class PhotoListView extends Backbone.View
	tagName: 'ul'

	initialize: -> 
		@model.on 'reset', @render, this

	render: (eventName) ->
		for photo in @model.models
			view = new PhotoListItemView model:photo
			(jQuery @el).append view.render().el

		this

class PhotoListItemView extends Backbone.View
	tagName: 'li'

	render: (eventName) ->
		(jQuery @el).text @model.get 'path' 
		this

class PhotoView extends Backbone.View
	render: (eventName) ->
		(jQuery @el).text "Photo " + @model.get 'path'
		this

class AppRouter extends Backbone.Router
	routes:
		'': 'list'
		'photos/:id': 'photoDetails'

	list: ->
		@photoList = new PhotoCollection
		@photoListView = new PhotoListView model:@photoList
		@photoList.fetch success: =>
			(jQuery '#photo-list').html @photoListView.render().el

	photoDetails: (id) ->
		@photo = @photoList.get id
		@photoView = new PhotoView model:@photo
		(jQuery '#photo-details').html @photoView.render().el

app = new AppRouter
Backbone.history.start()
