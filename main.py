import re
# Process the input string

sing_pron=["আমি","আপনি","তুমি","তোমার", "তুই", "সে", "আমার", "তিনি", "তার","ওর",  "তোর", "আপনার"]
plu_pron=["তোমরা","তোরা", "তারা", "আপনারা", "তোমাদের", "তোদের", "আপনাদের", "আমাদের", "ওদের"]

fp_pron=["আমি","আমার","আমাদের"]
sp_pron=["তোমরা","তোরা","আপনার","আপনারা","তুই","আপনি","তুমি","তোমার", "তোর","তোমাদের", "তোদের","আপনাদের"]
tp_pron=["তারা","তার","সে", "তিনি","ওদের", "ওর"]

status_respect=["আপনি", "আপনাদের","আপনার","আপনারা","তিনি"]
status_okayish=["তার", "তোমার","তুমি","তোমরা","সে", "তোমাদের","তারা"]
status_close = ["তোরা", "তোদের","তুই", "ওর" "তোর", "ওদের"]
status_na=["আমার","আমি", "আমাদের"]
def process_tokens(str):
	tokens=str.split(' ')
	processed_sentence=[]
	token_id=1
	for i in tokens:
		word_dict={}
		temp_list=i.split('/')
		# print(temp_list)
		word_dict['word'] = temp_list[0]
		word_dict['id']=token_id
		if(len(temp_list)==1):
			word_dict['POS'] = "SYM"
			word_dict['number'] ="NA"
			word_dict['person'] ="NA"
			word_dict['honor'] ="NA"
		else:
			word_dict['POS'] = temp_list[1]
			word_dict['number'] =temp_list[2]
			word_dict['person'] = temp_list[3]
			word_dict['honor'] = temp_list[4]
		token_id+=1
		processed_sentence.append(word_dict)
	return(processed_sentence)

def detect_anaphores(dic):
	anaphores=[]
	for i in dic:
		if(i['POS']=="PRP" or i['POS']=="PRP$"):
			anaphores.append(i)
	return anaphores

def detect_antecedents(dic):
	antecedents=[]
	for i in dic:
		if(i['POS']=="NP" or i['POS']=="NN"):
			antecedents.append(i)
	return antecedents
def identify(anaphore,antecedents):
	person=0
	formality=0
	number=0
	if anaphore['word'] in tp_pron:
		person = 3
	elif anaphore['word'] in sp_pron:
		person = 2
	elif anaphore['word'] in fp_pron:
		person = 1
	else:
		if(anaphore['person']=='T'):
			person=3
		elif(anaphore['person']=='S'):
			person=2
		elif(anaphore['person']=='F'):
			person=1
		else:
			print("person error in",anaphore['word'])


	if anaphore['word'] in status_respect:
		formality = 3
	elif anaphore['word'] in status_okayish:
		formality = 2
	elif anaphore['word'] in status_close:
		formality = 1
	elif anaphore['word'] in status_na:
		formality=4
	else:
		if(anaphore['honor']=='F'):
			formality=3
		elif(anaphore['honor']=='I'):
			formality=2
		elif(anaphore['honor']=='C'):
			formality=1
		elif(anaphore['honor']=='NA' and person==1):
			formality=4
		else:
			print("formality error in ",anaphore['word'])


	if anaphore['word'] in sing_pron:
		number = 1
	elif anaphore['word'] in plu_pron:
		number = 2
	else:
		if(anaphore['number']=='S'):
			number=1
		elif(anaphore['number']=='P'):
			number=2
		else:
			print("number error in ",anaphore['word'])

	human=1
	if(anaphore['word'].endswith("টা") or anaphore['word'].endswith("টি") or anaphore['word'].endswith("টির") or anaphore['word'].endswith("টিকে") or anaphore['word'].endswith("টাকে")):
		human=0

	survived_list=[]
	for i in antecedents:
		if(i['id']<anaphore['id']):
			# print(i)
			if(i['number']=='S' and number!=1):
				continue
			elif(i['number']=='P' and number!=2):
				continue

			if(i['person']=='T' and person!=3):
				continue
			elif(i['person']=='S' and person!=2):
				continue
			# elif(i['person']=='F' and person!=1):
			# 	continue

			if(i['honor']=='F' and formality!=3):
				continue
			elif(i['honor']=='I' and formality!=2):
				continue
			elif(i['honor']=='C' and formality!=1):
				continue

			if(human==1 and i['POS']!='NP'):
				continue
			if(human==0 and i['POS']!='NN'):
				continue


			survived_list.append(i)

	if(len(survived_list)==0):
		print("None of the antecedents matched the constraints for",anaphore['word'])
	else:
		print("Set of antecedents that matched the constraints for",anaphore['word'],":")
		print(survived_list)



inp_str=input()
processed_sentence=process_tokens(inp_str)
# print(processed_sentence)
anaphores=detect_anaphores(processed_sentence)
print("Pronomial anaphores:")
print(anaphores)
antecedents=detect_antecedents(processed_sentence)
print("Possible antecedents:")
print(antecedents)
for i in anaphores:
	identify(i,antecedents)

