punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']

#Punctuation Stripper

def strip_punctuation(sentence):
    for words in sentence:
        for punc in punctuation_chars:
            if words==punc:
                sentence=sentence.replace(words,"")
    return sentence
# lists of words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())

#Positivity Counter
def get_pos(sentence):
    amt_pos=0
    sentence=sentence.lower()
    stripped=strip_punctuation(sentence)
    stripped=stripped.split()
    for words in stripped:
        for pos_words in positive_words:
            if pos_words==words:
                amt_pos+=1
    return amt_pos
            
            
negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())
#Negativity Counter
def get_neg(sentence):
    amt_neg=0
    sentence=sentence.lower()
    stripped=strip_punctuation(sentence)
    stripped=stripped.split()
    for words in stripped:
        for neg_words in negative_words:
            if neg_words==words:
                amt_neg+=1
    return amt_neg


#Open CSV
file = open('project_twitter_data.csv',"r") #Text | Num_Ret | Num Replies
print(file.readlines())
#Create Sentiment Classifier
# Num_Ret | Num_Rep | Pos Score | Neg Score | Net Score


#Step 1, Create Writeable CSV File
data = open("resulting_data.csv","w")

#Step 2, Output headers
data.write("Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score")
data.write('\n')

#Step 3, Extract Data
lines = len(file.readlines())
first=True
incoming =[]
for line in file.readlines():
    if first:
        first=False
        continue
    incoming.append(line.split(","))
    
    
#Step 4, Process Data
outgoing=""

for i in range(lines-1):
    num_ret = (incoming[i][1])
    num_rep = ((incoming[i][2]).replace("\n",""))
    pos=get_pos(incoming[i][0])
    neg=get_neg(incoming[i][0])
    net=pos-neg
    form = "{}, {}, {}, {}, {}\n"
    #print(form.format(num_ret,num_rep,pos,neg,net))
    outgoing+=form.format(num_ret,num_rep,pos,neg,net)
#Spet 5, Output Data
data.write(outgoing)

#Step 6, Close
data.close()
file.close()
