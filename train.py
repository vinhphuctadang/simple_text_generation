from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
# from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku 
import numpy as np

filters = '"#$%&()*+-/:;<=>@[\\]^_`{|}~\t“”'
sentence_delimiter='?!.\n'
tokenizer = Tokenizer(filters=filters)
def preprocess (data):
	res = ''
	for i in data:
		if i in filters or i in filters:
			res+= ' '+i;
		else:
			res += i;
	return res

def mysplit (data,delim=sentence_delimiter):

	seq = []
	tmp = ''
	for i in data:
		if i in delim:
			seq.append (tmp+i)
			tmp = ''
		else:
			tmp += i
	if tmp != '':
		seq.append (tmp + ' .')
	return seq

def dataset_preparation(data):
	
	data = data.lower().split ('\n')
	corpus = []
	for line in data:
		line = preprocess (line)
		corpus.extend (mysplit (line))

	# print (corpus)
	tokenizer.fit_on_texts (corpus)
	total_words = len(tokenizer.word_index) + 1

	input_sequences = []
	for line in corpus:
		token_list = tokenizer.texts_to_sequences([line])[0]
		# print (token_list)
		for i in range(1, len(token_list)):
			n_gram_sequence = token_list[:i+1]
			input_sequences.append(n_gram_sequence)
	max_sequence_len = max([len(x) for x in input_sequences])
	input_sequences = np.array(pad_sequences(input_sequences,   
						  maxlen=max_sequence_len, padding='pre'))
	predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
	label = ku.to_categorical(label, num_classes=total_words)
	return np.array (predictors), np.array(label), max_sequence_len, total_words
def create_model(predictors, label, max_sequence_len, total_words):
	input_len = max_sequence_len - 1
	model = Sequential()
	model.add(Embedding(total_words, 10, input_length=input_len))
	model.add(LSTM(150,return_sequences=True))
	model.add(Dropout(0.2))
	model.add(LSTM(100))
	model.add(Dropout(0.2))
	# model.add(LSTM(150))
	model.add(Dense(total_words, activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
	# model.fit(predictors, label, epochs=100, verbose=1)

def generate_text(seed_text, next_words, max_sequence_len, model):
	for j in range(next_words):
		token_list = tokenizer.texts_to_sequences([seed_text])[0]
		token_list = pad_sequences([token_list], maxlen= 
							 max_sequence_len-1, padding='pre')
		predicted = model.predict_classes(token_list, verbose=0)
  
		output_word = ""
		for word, index in tokenizer.word_index.items():# get output word
			if index == predicted:
				output_word = word
				break
		seed_text += " " + output_word
		print (output_word,end=' ')
	return seed_text

def save_lobe (lobe,name='model.keras'):
	lobe.save(name)

def load_lobe (name='model.keras'):
	from keras.models import load_model
	model = load_model(name)
	return model

def main ():
	data = open ('input.txt', 'r', encoding='utf-8').read ()
	# print (data)
	X, Y, max_len, total_words = dataset_preparation(data)

	# print (X, len (X))
	# return;
	from os.path import isfile
	if not isfile ('model.keras'):
		model = create_model(X, Y, max_len, total_words)
		model.fit(X, Y, epochs=500, verbose=1)
		save_lobe (model)
	else:
		model = load_lobe ()

	txt = generate_text("Tôi", 500, max_len, model)
	# print (txt)
	# pd, lab = dataset_preparation (data)
	# print (pd);
	# print (lab)

if __name__=='__main__':
	main ()