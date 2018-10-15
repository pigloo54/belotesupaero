from django import forms
from .models import Trick, Player

class TrickForm(forms.Form):
	taker = forms.ModelChoiceField(widget=forms.Select(), queryset=Player.objects.none())
	round_taken = forms.ChoiceField(choices=(
		(1, 'One'),
		(2, 'Two')
		))
	card = forms.ChoiceField(choices=(
		('Jack', 'Jack'),
		('Nine', 'Nine'),
		('As', 'As'),
		('Ten', 'Ten'),
		('King', 'King'),
		('Queen', 'Queen'),
		('Eight', 'Eight'),
		('Seven', 'Seven'),
		))
	suit = forms.ChoiceField(choices=(
		('Diamond', 'Diamond'),
		('Heart', 'Heart'),
		('Spade', 'Spade'),
		('Club', 'Club')
		))
	score_ns = forms.IntegerField(widget = forms.NumberInput(attrs={'class' : 'fit'}))
	score_ew = forms.IntegerField(widget = forms.NumberInput(attrs={'class' : 'fit'}))
	belote_ns = forms.BooleanField(label = 'Belote', widget=forms.CheckboxInput(), required=False)
	belote_ew = forms.BooleanField(label = 'Belote', widget=forms.CheckboxInput(), required=False)
	valat = forms.BooleanField(label = 'Valat', widget=forms.CheckboxInput(), required=False)
	failed = forms.BooleanField(label = 'Failed', widget=forms.CheckboxInput(), required=False)

	def clean(self):
		cleaned_data = super(TrickForm, self).clean()
		taker = cleaned_data.get('taker')
		valat = cleaned_data.get('valat')
		round_taken = cleaned_data.get('round_taken')
		card = cleaned_data.get('card')
		suit = cleaned_data.get('suit')
		score_ns = cleaned_data.get('score_ns')
		score_ew = cleaned_data.get('score_ew')
		belote_ns = cleaned_data.get('belote_ns')
		belote_ew = cleaned_data.get('belote_ew')

		if ((belote_ns and belote_ew) or
						((valat == False) and (score_ns - belote_ns*20 +score_ew - belote_ew) != 162) or
						(valat == True and not (score_ns - belote_ns*20 == 252 and score_ew -belote_ew*20 == 0 or score_ew - belote_ew*20 == 252 and score_ns - belote_ns*20 == 0)) or
						(not(round_taken == '1' or round_taken == '2'))) :
			raise forms.ValidationError("Data isn't consistent" +  
			'taker:' + str(taker.id) + 
			'valat:' + str(valat)  + 
			'round_taken:' + str(round_taken) + 
			'card:' + str(card) + 
			'suit:' + str(suit) + 
			'score_ns:' + str(score_ns) + 
			'score_ew:' + str(score_ew) +
			'belote_ns:' + str(belote_ns) + 
			'belote_ew:' + str(belote_ew) 
			)
		else :
			return cleaned_data

