from django.db import models

class Saving(models.Model):
    initial_capital = models.FloatField(null=True)
    final_capital = models.FloatField(null=True)
    years = models.IntegerField(default=5)
    rate = models.FloatField(default=3.5)

    def calculate(self):
    	factor = (1 + (self.rate/100)/12) ** (12 * self.years)
    	if not self.initial_capital:
    		self.initial_capital = self.final_capital / factor
    	elif not self.final_capital:
    		self.final_capital = self.initial_capital * factor

    def __str__(self):
    	return "Initial Capital: " + str(self.initial_capital) + "\nYears: " + str(self.years) + "\nInterest Rate: " + str(self.rate)

