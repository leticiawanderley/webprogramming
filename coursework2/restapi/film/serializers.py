from film.models import Film, Actor, Director, Award
from rest_framework import serializers
from rest_framework.reverse import reverse

class ActorSerializer(serializers.ModelSerializer):
	films = serializers.SerializerMethodField()

	class Meta:
		model = Actor
		fields = ('id', 'url', 'name', 'nationality', 'films')
		read_only_fields = ('id', 'url', 'films') 

	def create(self, validated_data):
		view = self.context['view']
		actor = Actor.objects.get_or_create(**validated_data)[0]
		if 'pk' in view.kwargs:
			film_id = view.kwargs['pk']
			film = Film.objects.get(pk=film_id)
			film.actors.add(actor)
			film.save()
		return actor

	def get_films(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/?actor=" + str(obj.id)
  
class DirectorSerializer(serializers.ModelSerializer):
	films = serializers.SerializerMethodField()

	class Meta:
		model = Director
		fields = ('id', 'url', 'name', 'films')
		read_only_fields = ('id', 'url', 'films') 

	def create(self, validated_data):
		view = self.context['view']
		director = Director.objects.get_or_create(**validated_data)[0]
		if 'pk' in view.kwargs:
			film_id = view.kwargs['pk']
			film = Film.objects.get(pk=film_id)
			film.director = director
			film.save()
		return director

	def get_films(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/?director=" + str(obj.id)

class AwardSerializer(serializers.ModelSerializer):
	film = serializers.SerializerMethodField()

	class Meta:
		model = Award
		fields = ('id', 'url', 'name', 'category', 'film')
		read_only_fields = ('id', 'url', 'film')

	def create(self, validated_data):
		view = self.context['view']
		if 'pk' in view.kwargs:
			film_id = view.kwargs['pk']
			film = Film.objects.get(pk=film_id)
			validated_data['film'] = film
		return Award.objects.get_or_create(**validated_data)[0]

	def get_film(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/" + str(obj.film.id)

class FilmSerializer(serializers.ModelSerializer):
	actors = serializers.SerializerMethodField()
	director = serializers.SerializerMethodField()
	awards = serializers.SerializerMethodField()
	class Meta:
		model = Film
		fields = ('id', 'url', 'title', 'year', 'genre', 'director', 'actors', 'awards')
		read_only_fields = ('id', 'director', 'actors', 'awards')

	def create(self, validated_data):
		if 'actors' in validated_data:
			actors_data = validated_data.pop('actors')
		if 'director' in validated_data:
			director_data = validated_data.pop('director')
			if director_data and director_data.get('name'):
				validated_data['director'] = Director.objects.get_or_create(**director_data)[0]
		film = Film.objects.create(**validated_data)
		if actor_data:
			for actor_data in actors_data:
				actor = Actor.objects.get_or_create(**actor_data)[0]
				film.actors.add(actor)
		film.save()
		return film

	def update(self, instance, validated_data):
		self.validate_update(instance, validated_data)
		instance.title = validated_data.get('title', instance.title)
		instance.year = validated_data.get('year', instance.year)
		instance.genre = validated_data.get('genre', instance.genre)
		instance.save()
		return instance

	def validate_update(self, instance, validated_data):
		actors_data = validated_data.pop('actors')
		director_data = validated_data.pop('director')
		if len(actors_data) != len(instance.actors.all()):
			raise serializers.ValidationError("It's not possible to update actors in this state.")
		else:
			actors = instance.actors.all()
			for i in range(len(actors)):
				if actors[i].name != actors_data[i]['name'] or actors[i].nationality != actors_data[i]['nationality']:
					raise serializers.ValidationError("It's not possible to update actors in this state.")
		if director_data['name'] != instance.director.name:
			raise serializers.ValidationError("It's not possible to update the director in this state.")

	def get_actors(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/" + str(obj.id) + "/actor"

	def get_director(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/" + str(obj.id) + "/director"

	def get_awards(self, obj):
		self.request = self.context['request']
		return "http://" + self.request.META['HTTP_HOST'] + "/film/" + str(obj.id) + "/award"
