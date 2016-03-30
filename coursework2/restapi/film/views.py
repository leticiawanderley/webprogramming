from film.models import Film, Actor, Award, Director
from film.serializers import FilmSerializer, ActorSerializer, AwardSerializer, DirectorSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'film': reverse('film-list', request=request, format=format)
    })

class FilmList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Film.objects.all()
	serializer_class = FilmSerializer

class ActorList(generics.ListCreateAPIView):
    serializer_class = ActorSerializer
    def get_queryset(self):
    	film_id = self.kwargs['pk']
    	return Actor.objects.filter(film=film_id)

class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ActorSerializer
	def get_queryset(self):
		film_id = self.kwargs['pk']
		return Actor.objects.filter(film=film_id)
	def get_object(self):
		id = self.kwargs['id']
		return self.get_queryset().get(id=id)

class AwardList(generics.ListCreateAPIView):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

class AwardDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Award.objects.all()
	serializer_class = AwardSerializer

class DirectorList(generics.ListCreateAPIView):
    serializer_class = DirectorSerializer
    def get_queryset(self):
    	film_id = self.kwargs['pk']
    	return Director.objects.filter(film=film_id)

class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = DirectorSerializer
	def get_queryset(self):
		film_id = self.kwargs['pk']
		id = self.kwargs['id']
		return Director.objects.filter(film=film_id)
	def get_object(self):
		id = self.kwargs['id']
		return self.get_queryset().get(pk=id)
