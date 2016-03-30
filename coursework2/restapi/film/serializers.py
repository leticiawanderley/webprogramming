from film.models import Film, Actor, Director, Award
from rest_framework import serializers

class ActorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Actor
		fields = ('id','name', 'nationality')

	def create(self, validated_data):
		view = self.context['view']
		film_id = view.kwargs['pk']
		film = Film.objects.get(pk=film_id)
		actor = Actor.objects.get_or_create(**validated_data)[0]
		film.actors.add(actor)
		film.save()
		return actor
  
class DirectorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Director
		fields = ('id', 'name')

class AwardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Award
		fields = ('id', 'name', 'film')

class FilmSerializer(serializers.ModelSerializer):
	actors = ActorSerializer(many=True)
	director = DirectorSerializer(many=False)
	class Meta:
		model = Film
		fields = ('id', 'title', 'year', 'genre', 'director', 'actors')

	def create(self, validated_data):
		actors_data = validated_data.pop('actors')
		director_data = validated_data.pop('director')
		if director_data and director_data.get('name'):
			validated_data['director'] = Director.objects.get_or_create(**director_data)[0]
		film = Film.objects.create(**validated_data)
		for actor_data in actors_data:
			actor = Actor.objects.get_or_create(**actor_data)[0]
			film.actors.add(actor)
		film.save()
		return film
