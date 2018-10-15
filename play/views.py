from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from play.models import *
import os
from .forms import TrickForm

def viewGame(request, id):
	g = get_object_or_404(Game, id=id)
	
	tricks = Trick.objects.filter(game = g)
	# teams = Team.objects.filter(game = g)
	
	score_ns_complete = {'score': g.getScoreNS(), 'belote': g.getBeloteNS(), 'valat':g.getValatNS(), 'taken': g.getTakenNS(), 'failed': g.getFailedNS()}
	score_ew_complete = {'score': g.getScoreEW(), 'belote': g.getBeloteEW(), 'valat':g.getValatEW(), 'taken': g.getTakenEW(), 'failed': g.getFailedEW()}
	
	player_n_complete = {'player' : g.getPlayerN(), 'score' : g.getScoreN(),  'valat' : g.getValatN(), 'taken' : g.getTakenN(), 'failed': g.getFailedN(), 'done': g.getTakenN()-g.getFailedN()}
	player_s_complete = {'player' : g.getPlayerS(), 'score' : g.getScoreS(),  'valat' : g.getValatS(), 'taken' : g.getTakenS(), 'failed': g.getFailedS(), 'done': g.getTakenS()-g.getFailedS()}
	player_e_complete = {'player' : g.getPlayerE(), 'score' : g.getScoreE(),  'valat' : g.getValatE(), 'taken' : g.getTakenE(), 'failed': g.getFailedE(), 'done': g.getTakenE()-g.getFailedE()}
	player_w_complete = {'player' : g.getPlayerW(), 'score' : g.getScoreW(),  'valat' : g.getValatW(), 'taken' : g.getTakenW(), 'failed': g.getFailedW(), 'done': g.getTakenW()-g.getFailedW()}
	
	return render(request, 'play/viewGame.html', {
		'g':g,
		'tricks':tricks,
		'scores':{'ns' : score_ns_complete, 'ew':score_ew_complete},
		'players':{'player_n': player_n_complete, 'player_s': player_s_complete, 'player_e': player_e_complete, 'player_w': player_w_complete}
		})
		
def viewPlayer(request, id) :
	p = get_object_or_404(Player, id=id)
	
	gs = Game.objects.filter(players = p)
	
	return render(request, 'play/viewPlayer.html', {'p':p})
		
def newTrick(request, id):
	g = get_object_or_404(Game, id=id)

	form = TrickForm(request.POST or None)
	form.fields['taker'].queryset = g.players.all()
	if form.is_valid():
		t = Trick(number = g.getTrickNumber(),
			score_ns = form.cleaned_data['score_ns'],
			score_ew = form.cleaned_data['score_ew'],
			belote_ns = form.cleaned_data['belote_ns'],
			belote_ew = form.cleaned_data['belote_ew'],
			taker = form.cleaned_data['taker'],
			round_taken = form.cleaned_data['round_taken'],
			card = form.cleaned_data['card'],
			suit = form.cleaned_data['suit'],
			game = g)
		
		#t.save()
		return redirect('play/viewGame.html/'+str(g.id))
		
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
	return render(request, 'play/newTrick.html', locals())

def populateDatabase(request):
	location_file = open(os.path.dirname(__file__) + '/db_archive/lieu.csv', 'r')
	player_file = open(os.path.dirname(__file__) + '/db_archive/joueurs.csv', 'r')
	trick_file = open(os.path.dirname(__file__) + '/db_archive/round.csv', 'r')
	game_file = open(os.path.dirname(__file__) + '/db_archive/belote.csv', 'r')
	
	eqs = {'0' : 'Carreau', '1' : 'Coeur', '2' : 'Pique', '3' : 'Trefle'}
	eqc = {'0' : 'Sept', '1': 'Huit', '10' : 'Dix', '3' : 'Dame', '4' : 'Roi', '11' : 'As', '14' : 'Neuf', '20' : 'Valet'}
	l = {}
	p = {}
	
	for line in location_file :
		line = line.replace('\n','')
		l[line.split(',')[0]] = line.split(',')[1]
		lo = Location(name=line.split(',')[1])
		lo.save()
		
	for line in player_file :
		line = line.replace('\n','')
		p[line.split(',')[0]] = [line.split(',')[1].title(), line.split(',')[2].upper()]
		pl = Player(name = line.split(',')[1].title(), surname = line.split(',')[2].upper())
		pl.save()
	
	for line in game_file :
		line = line.replace('\n','')
		date = line.split(',')[2]
		if date == '00-00-0000' or date == '0000-00-00':
			date='1970-01-01'
		if line.split(',')[17] == '' :
			if line.split(',')[1] == '' :
				loc = Location.objects.filter(name = 'Unknown Location')[0]
				g = Game(location = loc, date = date)
			else :
				if line.split(',')[1] in l.keys() :
					g = Game(location = Location.objects.filter(name = l[line.split(',')[1]])[0], date = date)
				else :
					g = Game(location = Location.objects.filter(name = 'Unknown Location')[0], date = date)
			g.save()
			i = 0
			for line2 in trick_file :
				line2 = line2.replace('\n','')
				if line2.split(',')[1] == line.split(',')[0] :
					tr = Trick(score_ns=line2.split(',')[6],
						game = g,
						score_ew=line2.split(',')[7],
						belote_ns = line2.split(',')[8],
						belote_ew = line2.split(',')[9],
						suit = eqs[line2.split(',')[5]],
						card = eqc[line2.split(',')[4]],
						taker = Player.objects.filter(name=p[line2.split(',')[2]][0], surname=p[line2.split(',')[2]][1])[0],
						round_taken = line2.split(',')[3],
						number = i)
					i = i + 1
					tr.save()
			trick_file.seek(0)
		else :
			ls = line.split(',')
			if line.split(',')[1] in l.keys() :
				location = Location.objects.filter(name = l[line.split(',')[1]])[0]
			else :
				location = Location.objects.filter(name = 'Unknown Location')[0]
			g = Game(location = location,
				date = date,
				score_ns = int(ls[7]),
				score_ew = int(ls[8]),
				belote_ns = int(ls[13]),
				belote_ew = int(ls[14]),
				valat_ns = int(ls[15]),
				valat_ew = int(ls[16]),
				failed_n = int(ls[9]),
				failed_s = int(ls[10]),
				failed_e = int(ls[11]),
				failed_w = int(ls[12]),
				taken_n = int(ls[24]),
				taken_s = int(ls[25]),
				taken_e = int(ls[26]),
				taken_w = int(ls[27]),
				first_taken = int(ls[21]),
				second_taken = int(ls[22]),
				not_taken = int(ls[23]),
				taken_diamond = int(ls[17]),
				taken_heart = int(ls[18]),
				taken_spade = int(ls[19]),
				taken_club = int(ls[20]),
				version = 1
				)
		g.save()
		
		if line.split(',')[3] in p.keys():
			player = Player.objects.filter(name=p[line.split(',')[3]][0], surname=p[line.split(',')[3]][1])[0]
			t = Team(side='n', player = player, game = g)
			t.save()
		else :
			raise ValueError('A very specific bad thing happened')
		if line.split(',')[4] in p.keys():
			player = Player.objects.filter(name=p[line.split(',')[4]][0], surname=p[line.split(',')[4]][1])[0]
			t = Team(side='s', player = player, game = g)
			t.save()
		else :
			raise ValueError('A very specific bad thing happened')
		if line.split(',')[5] in p.keys():
			player = Player.objects.filter(name=p[line.split(',')[5]][0], surname=p[line.split(',')[5]][1])[0]
			t = Team(side='e', player = player, game = g)
			t.save()
		else :
			raise ValueError('A very specific bad thing happened')
		if line.split(',')[6] in p.keys():
			player = Player.objects.filter(name=p[line.split(',')[6]][0], surname=p[line.split(',')[6]][1])[0]
			t = Team(side='w', player = player, game = g)
			t.save()
		else :
			raise ValueError('A very specific bad thing happened')
		
		
	
	location_file.close()
	player_file.close()
	trick_file.close()
	game_file.close()
	
	return HttpResponse(' ')
