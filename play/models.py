from django.db import models
from django.utils import timezone
from django.db.models import Sum

# Create your models here.

class Game(models.Model):
	players = models.ManyToManyField('Player', through='Team')
	location = models.ForeignKey('Location', on_delete=models.PROTECT)
	date = models.DateField(default=timezone.now, verbose_name="Game day")
	score_ns = models.IntegerField(default=0)
	score_ew = models.IntegerField(default=0)
	belote_ns = models.IntegerField(default=0)
	belote_ew = models.IntegerField(default=0)
	valat_ns = models.IntegerField(default=0)
	valat_ew = models.IntegerField(default=0)
	taken_n = models.IntegerField(default=0)
	taken_s = models.IntegerField(default=0)
	taken_e = models.IntegerField(default=0)
	taken_w = models.IntegerField(default=0)
	failed_n = models.IntegerField(default=0)
	failed_s = models.IntegerField(default=0)
	failed_e = models.IntegerField(default=0)
	failed_w = models.IntegerField(default=0)
	taken_heart = models.IntegerField(default=0)
	taken_diamond = models.IntegerField(default=0)
	taken_club = models.IntegerField(default=0)
	taken_spade = models.IntegerField(default=0)
	first_taken = models.IntegerField(default=0)
	second_taken = models.IntegerField(default=0)
	not_taken = models.IntegerField(default=0)
	version = models.IntegerField(default=2)
   
	class Meta:
		verbose_name = "Belote Game"
		ordering = ['date']
    
	def __str__(self):
		s=""
		for p in self.players.all():
			s=s+p.name+','
		s=s+'@'+self.location.name
		return s
	
	def isNorthOrSouth(self, p):
		if p == self.getPlayerN() or p == self.getPlayerS():
			return True
		else :
			return False
	
	
	def getPlayerN(self):
		return self.players.get(team__side = 'n')
		
	def getPlayerS(self):
		return self.players.get(team__side = 's')

	def getPlayerE(self):
		return self.players.get(team__side = 'e')
		
	def getPlayerW(self):
		return self.players.get(team__side = 'w')

	
	def getScoreNS(self):
		if self.version == 1 :
			return self.score_ns
		else :
			return Trick.objects.filter(game=self).aggregate(Sum('score_ns'))['score_ns__sum']
	
	def getScoreEW(self):
		
		if self.version == 1 :
			return self.score_ew
		else :
			return Trick.objects.filter(game=self).aggregate(Sum('score_ew'))['score_ew__sum']

	def getScoreN(self):
		if self.version == 1 :
			return "N/A"
		else :
			return Trick.objects.filter(game = self, taker = self.getPlayerN()).aggregate(Sum('score_ns'))['score_ns__sum']
	
	def getScoreS(self):
		if self.version == 1 :
			return "N/A"
		else :
			return Trick.objects.filter(game = self, taker = self.getPlayerS()).aggregate(Sum('score_ns'))['score_ns__sum']

	def getScoreE(self):
		if self.version == 1 :
			return "N/A"
		else :
			return Trick.objects.filter(game = self, taker = self.getPlayerE()).aggregate(Sum('score_ew'))['score_ew__sum']
	
	def getScoreW(self):
		if self.version == 1 :
			return "N/A"
		else :
			return Trick.objects.filter(game = self, taker = self.getPlayerW()).aggregate(Sum('score_ew'))['score_ew__sum']
			
	
	def getBeloteNS(self):
		if self.version == 1 :
			return self.belote_ns
		else :
			return Trick.objects.filter(game=self).aggregate(Sum('belote_ns'))['belote_ns__sum']
	
	def getBeloteEW(self):
		if self.version == 1 :
			return self.belote_ew
		else :
			return Trick.objects.filter(game=self).aggregate(Sum('belote_ew'))['belote_ew__sum']
	
	
	def getValatNS(self):
		if self.version == 1 :
			return self.valat_ns
		else :
			return (self.getValatN() + self.getValatS())
	
	def getValatEW(self):
		if self.version == 1 :
			return self.valat_ew
		else :
			return (self.getValatE() + self.getValatW())  
	
	def getValatN(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len(Trick.objects.filter(game = self, taker = self.getPlayerN(), score_ns__gte = 250))
	
	def getValatS(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len(Trick.objects.filter(game = self, taker = self.getPlayerS(), score_ns__gte = 250))

	def getValatE(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len(Trick.objects.filter(game = self, taker = self.getPlayerE(), score_ew__gte = 250))
	
	def getValatW(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len(Trick.objects.filter(game = self, taker = self.getPlayerW(), score_ew__gte = 250))
	
	
	def getTakenNS(self):
		if self.version == 1 :
			return "N/A"
		else :
			return (self.getTakenN() + self.getTakenS())

	def getTakenEW(self):
		if self.version == 1 :
			return "N/A"
		else :
			return (self.getTakenE() + self.getTakenW())
	
	def getTakenN(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len(Trick.objects.filter(game = self, taker = self.getPlayerN()))
	
	def getTakenS(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len(Trick.objects.filter(game = self, taker = self.getPlayerS()))

	def getTakenE(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len(Trick.objects.filter(game = self, taker = self.getPlayerE()))
	
	def getTakenW(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len(Trick.objects.filter(game = self, taker = self.getPlayerW()))
	
	def getFailedNS(self):
		if self.version == 1 :
			return "N/A"
		else :
			return (self.getFailedN()+self.getFailedS())

	def getFailedEW(self):
		if self.version == 1 :
			return "N/A"
		else :
			return (self.getFailedE()+self.getFailedW())
	
	def getFailedN(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len([t for t in Trick.objects.filter(game = self, taker = self.getPlayerN()) if t.score_ns < t.score_ew])

	def getFailedS(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len([t for t in Trick.objects.filter(game = self, taker = self.getPlayerS()) if t.score_ns < t.score_ew])

	def getFailedE(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len([t for t in Trick.objects.filter(game = self, taker = self.getPlayerE()) if t.score_ns > t.score_ew])

	def getFailedW(self):
		if self.version == 1 :
			return "N/A"
		else :
			return len([t for t in Trick.objects.filter(game = self, taker = self.getPlayerW()) if t.score_ns > t.score_ew])
	
	def hasWon(self, p):
		if isNorthOrSouth(p) == (self.getScoreNS > self.getScoreEW) :
			return True
		else :
			return False
			
	def getTrickNumber(self):
		return len(Trick.objects.filter(game = self))
        
class Team(models.Model):
	side = models.CharField(max_length=2)
	player = models.ForeignKey('Player', on_delete=models.PROTECT)
	game = models.ForeignKey('Game', on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Belote Team"
		ordering = ['game']

	def __str__(self):
		return self.side

class Player(models.Model):
	surname = models.CharField(max_length=25)
	name = models.CharField(max_length=25)
	nickname = models.CharField(max_length=25)
	
	class Meta:
		verbose_name = "Player"
		ordering = ['name']
	
	def __str__(self):
		return self.name + " " + self.surname
	
class Trick(models.Model):
	number = models.IntegerField(default=-1)
	score_ns = models.IntegerField(default=0)
	score_ew = models.IntegerField(default=0)
	belote_ns = models.IntegerField(default=0)
	belote_ew = models.IntegerField(default=0)
	taker = models.ForeignKey('Player', on_delete=models.PROTECT)
	round_taken = models.IntegerField()
	card = models.CharField(max_length=10)
	suit = models.CharField(max_length=10)
	game = models.ForeignKey('Game', on_delete=models.CASCADE)
	
	class Meta:
		verbose_name = "Belote Trick"
		ordering = ['number']

	def __str__(self):
		return str(self.score_ns) + '/' + str(self.score_ew)
		
class Location(models.Model):
	name = models.CharField(max_length=20)

	class Meta:
		verbose_name = "Location"
		ordering = ['name']

	def __str__(self):
		return self.name
