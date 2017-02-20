import itertools
import operator
import math

# find total counts of all words
#build a list of unigram counts
file = open("unigram.txt")
uni_list = []
total_count = 0
for line in file:
	uni_list += line.splitlines()
	total_count += int(line.splitlines()[0])
file.close

#build a list of voabulary
file = open("vocab.txt")
vocab_list = []
for line in file:
	vocab_list += line.splitlines()
file.close

#calculate max likelihood estimate of unigram distribution  
uni_dict = {}
count = None
for w,c in zip(vocab_list, uni_list):
	count = int(c)
	uni_dict[w] = float(count)/total_count

#write to file: unigram porbabilies of all words start with A 
with open('answer_a.txt', 'w') as f:
	for word in uni_dict.keys():
		if word[0] == 'A':
			f.write((word + ', ' + str(uni_dict[word]) + '\n'))

#bigram 
file = open("bigram_the.txt")
bi_dict = {}
for line in file:
	newline = line.split()
	word_idx_followed = int(newline[1])
	bi_count = int(newline[2])
	bi_dict[vocab_list[word_idx_followed - 1]] = float(bi_count)/ int(uni_list[3])
file.close
bigram_result = sorted(bi_dict.items(), key = operator.itemgetter(1), reverse = True)[:10]
with open('answer_b.txt', 'w') as f:
	f.write('Word follows \'THE\': ' + 'Bigram probability' + '\n')
	for bigram_count in bigram_result: 
		f.write((bigram_count[0] + ': ' + str(bigram_count[1])))
		f.write('\n')
#build a dictionary using 'hw4_bigram.txt'to record likelihood of each given pair
file = open("bigram.txt")
bi_full_dict = {}
for line in file:
	the_line = line.split()
	idx_word = int(the_line[0])
	idx_word_followed = int(the_line[1])
	count_bi = int(the_line[2])
	bi_full_dict[vocab_list[idx_word -1] + "," + vocab_list[idx_word_followed - 1]] = float(count_bi)/ int(uni_list[idx_word -1])
file.close
print("Done loading bigram dictionary")

def uni_word(word):
	word_index = vocab_list.index(word)
	uni_prob = float(uni_list[word_index])/total_count
	return uni_prob

def uni_log(sentence):
	input_list = sentence.split()
	uni_product = 1
	with open('plot_uni_b.txt', 'w') as f:
		for word in input_list:
			uni_product *= uni_word(word)
			f.write(word+'\t'+ str(uni_word(word))+'\n')
	log_result = math.log(uni_product)
	print("the log likelihood of unigram is ", log_result)
	return log_result

def bi_log(sentence):
	input_list = ['<s>'] + sentence.split()
	bi_product = 1
	with open('plot_bi_x.txt','w')as f:
		for i in range(1,len(input_list)):
			key = input_list[i-1] + "," + input_list[i]
			if key in bi_full_dict:
				f.write(key+'\t'+str(bi_full_dict[key])+'\n')
				bi_product *= bi_full_dict[key]
			elif key not in bi_full_dict:
				f.write(key+'\t'+'0'+'\n')


print("\n  Calculating sentence 'THE SIXTEEN OFFICIALS SOLD FIRE INSURANCE'")
uni_log("THE SIXTEEN OFFICIALS SOLD FIRE INSURANCE")
bi_log("THE SIXTEEN OFFICIALS SOLD FIRE INSURANCE")




