from film.models import Film, Actor, Director, Award
from rest_framework import serializers
from rest_framework.reverse import reverse

"""Serializer of Actor model
"""
class ActorSerializer(serializers.ModelSerializer):
	films = serializers.SerializerMethodField()

	class Meta:
		model = Actor
		fields = ('id', 'url', 'name', 'nationality', 'films')
		read_only_fields = ('id', 'url', 'films') 
	
	"""Function create overriden to include actor in film's cast
	if the request was made inside the film's actors list
	"""
	def create(self, validated_data):
		view = self.context['view']
		actor = Actor.objects.get_or_create(**validated_data)[0]
		if 'pk' in view.kwargs:
			film_id = view.kwargs['pk']
			film = Film.objects.get(pk=film_id)
			film.actors.add(actor)
			film.save()
		return actor
	
	"""Creates a link to actor's film list
	"""
	def get_films(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/?actor=" + str(obj.id)

"""Serializer of Director model
"""
class DirectorSerializer(serializers.ModelSerializer):
	films = serializers.SerializerMethodField()

	class Meta:
		model = Director
		fields = ('id', 'url', 'name', 'films')
		read_only_fields = ('id', 'url', 'films') 

	"""Function create overriden to include director in film
	if the request was made inside the film's director list
	"""
	def create(self, validated_data):
		view = self.context['view']
		director = Director.objects.get_or_create(**validated_data)[0]
		if 'pk' in view.kwargs:
			film_id = view.kwargs['pk']
			film = Film.objects.get(pk=film_id)
			film.director = director
			film.save()
		return director

	"""Creates a link to director's film list
	"""
	def get_films(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/?director=" + str(obj.id)

"""Serializer of Award model
"""
class AwardSerializer(serializers.ModelSerializer):
	film = serializers.SerializerMethodField()

	class Meta:
		model = Award
		fields = ('id', 'url', 'name', 'category', 'film')
		read_only_fields = ('id', 'url', 'film')

	"""Function create overriden to include award in film's award list
	if the request was made inside the film's award list
	"""
	def create(self, validated_data):
		view = self.context['view']
		if 'pk' in view.kwargs:
			film_id = view.kwargs['pk']
			film = Film.objects.get(pk=film_id)
			validated_data['film'] = film
		return Award.objects.get_or_create(**validated_data)[0]

	"""Creates a link to award's film winner
	"""
	def get_film(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/" + str(obj.film.id)

"""Serializer of Film model
"""
class FilmSerializer(serializers.ModelSerializer):
	actors = serializers.SerializerMethodField()
	director = serializers.SerializerMethodField()
	awards = serializers.SerializerMethodField()
	class Meta:
		model = Film
		fields = ('id', 'url', 'title', 'year', 'genre', 'director', 'actors', 'awards')
		read_only_fields = ('id', 'director', 'actors' 'awards')

	"""Creates a link to film's actors
	"""
	def get_actors(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/" + str(obj.id) + "/actor"

	"""Creates a link to film's director
	"""
	def get_director(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/" + str(obj.id) + "/director"

	"""Creates a link to film's awards
	"""
	def get_awards(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/" + str(obj.id) + "/award"
