class Photo extends Backbone.Model

class PhotoCollection extends Backbone.Collection
	model: Photo

	initialize: (folder) ->
		@url = '../api/photos/' + folder

class PhotoListView extends Backbone.View
	tagName: 'ul'

	initialize: -> 
		@model.on 'reset', @render, this

	render: (eventName) ->
		for photo in @model.models
			view = new PhotoListItemView model:photo
			(jQuery @el).append view.render()

class PhotoListItemView extends Backbone.View
	tagName: 'li'

	template: _.template '<a href="#photos/<%= id %>"><%= path %></a>'

	render: (eventName) ->
		(jQuery @el).html @template @model.toJSON()

class PhotoView extends Backbone.View
	render: (eventName) ->
		(jQuery @el).text "Photo " + @model.get 'path'

class AppRouter extends Backbone.Router
	initialize: ->
		@route '', 'list'
		@route 'folders/*path', 'list'
		@route 'photos/:id', 'photoDetails'
	
	list: (folder) ->
		@photoList = new PhotoCollection folder ? '2013'
		@photoListView = new PhotoListView model:@photoList
		@photoList.fetch success: =>
			(jQuery '#photo-list').html @photoListView.render()

	photoDetails: (id) ->
		console.log "photoDetails", id
		@photo = @photoList.get id
		@photoView = new PhotoView model:@photo
		(jQuery '#photo-details').html @photoView.render()

app = new AppRouter
Backbone.history.start()
