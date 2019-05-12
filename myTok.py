
punc = '()[]{}%%."\''
def split (data):
	res = []
	tmp = ''
	hash_table = {}
	cnt = 0

	sentence = []
	for i in data:
		if i == ' ':
			if tmp != '':
				if tmp not in hash_table:
					cnt += 1
					hash_table[tmp] = cnt

				sentence.append (hash_table[tmp])
				tmp = ''
		else:
			if i in punc:
				if i not in hash_table:
					cnt += 1
					hash_table[i] = cnt
				if tmp != '':	
					if tmp not in hash_table:
						cnt += 1
						hash_table[tmp] = cnt
					
					sentence.append (hash_table[tmp])

				sentence.append (hash_table[i])
			else:
				tmp += i
				
			if i == '.':
				res.append (sentence)
				sentence = []

	return res

print (split ('Tôi đi. học'))