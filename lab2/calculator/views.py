import datetime 
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from calculator.models import Saving
from django.views import generic

class IndexView(generic.ListView):

	template_name = 'calculator/index.html'
	context_object_name = 'queries_list'

	def get_queryset(self):
		return Saving.objects.all()[:10]

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		c = super(IndexView, self).get_context_data(**kwargs)
		# add the request to the context
		c.update({ 'request': self.request })
		# add session variables to the context
		c.update(self.request.session)
		if 'rate' in self.request.COOKIES:
			rate = self.request.COOKIES['rate']
			c.update({'rate': float(rate)})
		return c

def result(request):
	initial_capital = request.POST['initial']
	final_capital = request.POST['final']
	years = float(request.POST['years'])
	rate = float(request.POST['rate'])
	if initial_capital:
		initial_capital = float(initial_capital)
		final_capital = None
	elif final_capital:
		final_capital = float(final_capital)
		initial_capital = None
	saving = Saving(initial_capital=initial_capital, final_capital=final_capital, years=years, rate=rate)
	saving.calculate()
	saving.save()
	response = HttpResponseRedirect(reverse('calculator:saving', args=(saving.id,)))
	response.set_cookie('rate', str(rate), expires=calculate_exp())
	request.session['initial_capital'] = saving.initial_capital
	request.session['final_capital'] = saving.final_capital
	request.session['years'] = saving.years
	return response

def calculate_exp():
	now = datetime.datetime.utcnow()
	max_time = 7 * 24 * 60 * 60
	exp = now + datetime.timedelta(seconds=max_time)
	format = "%a, %d-%b-%Y %H:%M%S GMT"
	exp_str = datetime.datetime.strftime(exp, format)
	return exp_str

class DetailView(generic.DetailView):
    model = Saving
    template_name = 'calculator/saving.html'