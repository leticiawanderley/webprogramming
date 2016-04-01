from film.models import Film, Actor, Award, Director
from film.serializers import FilmSerializer, ActorSerializer, AwardSerializer, DirectorSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'film': reverse('film-list', request=request, format=format),
        'actor': reverse('actor-list', request=request, format=format),
        'director': reverse('director-list', request=request, format=format),
        'award': reverse('award-list', request=request, format=format)
    })

class FilmList(generics.ListCreateAPIView):
    serializer_class = FilmSerializer
    def get_queryset(self):
    	actor = self.request.query_params.get('actor', None)
    	director = self.request.query_params.get('director', None)
    	queryset = Film.objects.all()
    	if actor is not None:
    		queryset = queryset.filter(actors__id=actor)
    	elif director is not None:
    		queryset = queryset.filter(director__id=director)
    	return queryset

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Film.objects.all()
	serializer_class = FilmSerializer
	def get_object(self):
		pk = self.kwargs['pk']
		try:
			return Film.objects.get(pk=pk)
		except Film.DoesNotExist:
			raise Http404

class ActorList(generics.ListCreateAPIView):
    serializer_class = ActorSerializer
    def get_queryset(self):
    	if 'pk' in self.kwargs:
    		film_id = self.kwargs['pk']
    		return Actor.objects.filter(film=film_id)
    	else:
    		return Actor.objects.filter()

class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ActorSerializer
	def get_queryset(self):
		return Actor.objects.filter()
	def get_object(self):
		pk = self.kwargs['pk']
		try:
			return self.get_queryset().get(pk=pk)
		except Actor.DoesNotExist:
			raise Http404

class AwardList(generics.ListCreateAPIView):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    def get_queryset(self):
    	queryset = Award.objects.all()
    	if 'pk' in self.kwargs:
    		film_id = self.kwargs['pk']
    		queryset.filter(film__id=film_id)
    	return queryset

class AwardDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Award.objects.all()
	serializer_class = AwardSerializer
	def get_object(self):
		pk = self.kwargs['pk']
		try:
			return Award.objects.get(pk=pk)
		except Award.DoesNotExist:
			raise Http404

class DirectorList(generics.ListCreateAPIView):
    serializer_class = DirectorSerializer
    def get_queryset(self):
    	if 'pk' in self.kwargs:
    		film_id = self.kwargs['pk']
    		return Director.objects.filter(film=film_id)
    	else:
    		return Director.objects.filter()

class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = DirectorSerializer
	def get_queryset(self):
		return Director.objects.filter()
	def get_object(self):
		pk = self.kwargs['pk']
		try:
			return self.get_queryset().get(pk=pk)
		except Director.DoesNotExist:
			raise Http404
		
