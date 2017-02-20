import sys
import operator
import string

#open the file contains words and word counts
file = open ("wc05.txt")
d = {}
#store words and their frequency in a dictionary
for line in file:
	entry = line.split()
	word = entry[0]
	count = float(entry[1])
	d[word] = count
#close file	
file.close

#fuction to calculate prior probability(non-zero)
def priorProb(word):
	totalCount = sum(d.values())
	p = (d[word])/totalCount
	return p
denominator_value = None


def denominator(evidence):
	#denominator
	prob_denominator_sum = 0
	
	for words in d:
		prob_evid_given_word_denom = None
		for letter, position_list in evidence.items():
			for i in range(5):
				if((words[i] == letter )and (i in position_list)):
					continue
				elif((words[i] != letter )and (i not in position_list)):
					continue
				else:
					prob_evid_given_word_denom = 0.0
					break
		if(prob_evid_given_word_denom == None):
			prob_evid_given_word_denom = 1.0
		prob_denominator_sum += prob_evid_given_word_denom * priorProb(words)
	return prob_denominator_sum
	
#function to calculate posterior probability
def postProb(evidence, word):
	#numerator
	prob_evid_given_word = None
	for letter, position_list in evidence.items():
		for i in range(5):
			if((word[i] == letter) and (i in position_list)):
				continue
			elif((word[i]!= letter) and (i not in position_list)):
				continue
			else:
				prob_evid_given_word = 0.0
				break
	if(prob_evid_given_word == None):
		prob_evid_given_word = 1.0
	prob_numerator = prob_evid_given_word * priorProb(word)
	return prob_numerator/denominator_value

#calculate predictive probability
def predictProb(letter, evidence,position_set):
	#build a set of all letters to check
	alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	letters_to_check = alphabet - set(evidence.keys())
	if letter not in letters_to_check:
		print("This letter ", letter," has already been guessed. Try another.")
		return 0.0
	positions_to_fill = set([0,1,2,3,4]) - position_set
	prob_letter_in_word = None
	prob_predictive = 0
	for word in d:
		prob_letter_in_word = None
		for position in positions_to_fill:
			if (word[position] == letter):
				prob_letter_in_word = 1
			else:
				continue
		if (prob_letter_in_word != 1): #caution: silent error 
			prob_letter_in_word = 0
		prob_predictive += prob_letter_in_word * postProb(evidence,word)

	return prob_predictive

def game(correctly_guessed, incorrectly_guessed):
	 
	#build evidence from input
	position_set = set()
	evidence = {}
	for i in range(5):
		if (correctly_guessed[i] != '-'):
			if correctly_guessed[i] not in evidence:
				evidence[correctly_guessed[i]] = [i]
			else:
				evidence[correctly_guessed[i]].append(i)
			#add to position set
			position_set.add(i)
		else:
			continue
	for j in range(len(incorrectly_guessed)):
		if incorrectly_guessed[j] in evidence:
			continue
		else:
			evidence[incorrectly_guessed[j]] = []
	print (evidence)
	global denominator_value
	denominator_value = denominator(evidence)
	print(denominator_value)
	#calculate predictive probability for every letter
	dict_predict_prob = dict.fromkeys(string.ascii_uppercase, None)
	for letter in dict_predict_prob.keys():
		dict_predict_prob[letter] = predictProb(letter,evidence,position_set)
	print (dict_predict_prob)

	ordered_predict_prob = sorted(dict_predict_prob.items(), key = operator.itemgetter(1))
	letter_to_guess = ordered_predict_prob[-1]
	print(letter_to_guess)


if __name__ == '__main__':
	correctly_guessed = "--H--"
	incorrectly_guessed = ['E','I','M','N','T']
	game(correctly_guessed, incorrectly_guessed)
