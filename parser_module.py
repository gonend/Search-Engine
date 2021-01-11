import re

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize
from unicodedata import numeric

from document import Document
from nltk.stem import PorterStemmer

class Parse:

    def __init__(self):

        self.stop_words = stopwords.words('english')
        add_add_stop = ["//", '/', '.', '..', '...', ':', ';', '?', '[', ']', '{', '}',
                        '(', ')', '<', '>', '!', '*', '+', '-', '=', '^', '~', '_', '|', '||', "'", "'", ',', '$', '&',
                        '’']
        self.stop_words.extend(add_add_stop)

    def hashTag_handler(self, term):
        hash_term = []
        if term.__contains__('_'):
             term = term.replace('#', '')  # removing the # symbol
             hash_term.extend(term.split('_'))  #
             # checks if the term is all upperCase and not all lowerCase
             # idea- replace: term!= '#COVID19' -> term.isalpha()
        elif sum(map(str.isupper, term)) != len(term) and sum(
                 map(str.isupper, term)) != 0 and term[1:].isalpha():
             term = term.replace('#', '')  # remove the '#' symbol
             temp = re.split('(?=[A-Z])', term)
             temp.pop(0)
             hash_term.extend(temp)  # spliting the hashTag by upperCase letters
        return hash_term


    def upperCase_handler(self, term):
        if len(term) > 0 and term.isalpha():  # deals with whiteSpace and check if the term is all lphabetic
            if term[0].isupper():
                temp = term.replace(term, term.upper())
            else:
                temp = term.replace(term, term.lower())
            return temp
        return term


    def percentage_handler(self, text_tokens):
        pre = ''
        while text_tokens.__contains__('%') or text_tokens.__contains__('percent') or text_tokens.__contains__('percentage'):
            if text_tokens.__contains__('%'):
                inx = text_tokens.index('%')
            elif text_tokens.__contains__('percent'):
                inx = text_tokens.index('percent')
            elif text_tokens.__contains__('percentage'):
                inx = text_tokens.index('percentage')
            if inx > 0 and (text_tokens[inx - 1].isnumeric() or re.findall("([0-9]+[,.]+[0-9]+)", text_tokens[inx - 1])):
                pre += text_tokens[inx - 1] + '%'
                text_tokens.pop(inx - 1)
                text_tokens.pop(inx - 1)
                text_tokens.insert(inx - 1, pre)
                pre = ''
            else:
                break

    def big_number_hendler(self, text_tokens):
        pre = ''
        sign = ''
        while text_tokens.__contains__('thousand') or text_tokens.__contains__('THOUSAND') \
                or text_tokens.__contains__('million') or text_tokens.__contains__('MILLION')\
                or text_tokens.__contains__('billion') or text_tokens.__contains__('BILLION')\
                or text_tokens.__contains__('trillion') or text_tokens.__contains__('TRILLION'):
            if text_tokens.__contains__('thousand'):
                inx = text_tokens.index('thousand')
                sign = 'K'
            elif text_tokens.__contains__('THOUSAND'):
                inx = text_tokens.index('THOUSAND')
                sign = 'K'
            elif text_tokens.__contains__('million'):
                inx = text_tokens.index('million')
                sign = 'M'
            elif text_tokens.__contains__('MILLION'):
                inx = text_tokens.index('MILLION')
                sign = 'M'
            elif text_tokens.__contains__('billion'):
                inx = text_tokens.index('billion')
                sign = 'B'
            elif text_tokens.__contains__('BILLION'):
                inx = text_tokens.index('BILLION')
                sign = 'B'
            elif text_tokens.__contains__('trillion'):
                inx = text_tokens.index('trillion')
                sign = 'T'
            elif text_tokens.__contains__('TRILLION'):
                inx = text_tokens.index('TRILLION')
                sign = 'T'
            if text_tokens[inx - 1] == '1.4B':
                print("asdasd")
            if inx > 0 and (text_tokens[inx - 1].isnumeric() or re.findall("([0-9]+[,.]+[0-9])", text_tokens[inx - 1])):
                if type(text_tokens[inx-1]) != float:
                    if text_tokens[inx-1].__contains__(','):
                        text_tokens[inx-1] = text_tokens[inx-1].replace(",", ".")
                    if text_tokens[inx-1].__contains__('-'):
                        text_tokens[inx-1] = text_tokens[inx-1].replace("-", "")
                    if text_tokens[inx-1].__len__() <= 1:
                        x = unicodedata.numeric(text_tokens[inx-1])
                    else:
                        if text_tokens[inx-1] != '1.4B':
                            break
                        x = float(text_tokens[inx-1]) # hendle the 1.4B essue
                pre += text_tokens[inx - 1] + sign
                text_tokens.pop(inx - 1)
                text_tokens.pop(inx - 1)
                text_tokens.insert(inx - 1, pre)
                pre = ''
                sign = ''
            else:
                break

    #def index_of_numbers(self, text_tokens):
    #    indexes = [i for i in range(0, len(text_tokens)) if text_tokens[i].isnumeric()]
    #    return indexes

    def combine_numbers(self, term, text_tokens, inx):  # combine number with shever
        if 0 < term < 1:
            if text_tokens[inx - 1].isnumeric():
                full_number = text_tokens[inx - 1] + text_tokens[inx]
                return full_number
        return None

    def number_handler(self, term, text_tokens, inx):
        # frac = unicodedata.numeric('¼')
        if term.__contains__('…'):
            term = term.replace('…', '')
        if term == '1.5661818…':
            term = term.replace('…', '')
        if term.isnumeric() or re.findall("[0-9]+[,.]+[0-9]", term):
            temp = term
            if re.findall("[(0-9)]+[' ']+[0-9]+[.-]+[0-9]", term):  # if it is IP addres
                return temp
            if re.findall("[0-9]+[.-]+[0-9]+[.-]+[0-9]", term):  # if it is IP addres
                return temp
            if term.__contains__('https') or term.__contains__('www'):
                return temp
            num = term.replace(",", "")
            if len(num) < 2:
                num = numeric(num)
            if re.findall("[0-9a-zA-Z]+[.]+[a-zA-Z]", term):
                splited1 = re.split("[.]+[A-Z]", term)
                splited2 = re.split("[A-Za-z]+[.]", term)
                inx = text_tokens.index(term)
                text_tokens.pop(inx)
                text_tokens.insert(inx,splited2[len(splited2)-1])
                text_tokens.insert(inx, splited1[0])
                return True
            if re.findall("[A-Za-z]", term):
                return temp
            if re.findall("[/]", term):
                num = num.replace('/', '')
                print(temp)
            try:
                temp = float(num)
            except:
                return temp
            if 0 < temp.__abs__() < 1:             #number is rational like '½'
                res = self.combine_numbers(temp, text_tokens, inx)
                return res
            num = temp
            if num == int(num):
                num = int(num)
            if num.__abs__() >= 1000:
                if 1000 <= num < 1000000:
                    num = num / 1000
                    if num == int(num):
                        num = int(num)
                    temp = str(num) + 'K'
                elif 1000000 <= num < 1000000000:
                    num = round(num / 1000000, 3)
                    if num == int(num):
                        num = int(num)
                    temp = str(num) + 'M'
                elif num > 1000000000:
                    num = round(num / 1000000, 3)
                    if num == int(num):
                        num = int(num)
                    temp = str(num) + 'B'
            elif inx+1 == len(text_tokens):
                return temp
            elif text_tokens[inx + 1].__contains__('thousand') or text_tokens[inx + 1].__contains__('THOUSAND'):
                temp = str(num) + 'K'
            elif text_tokens[inx + 1].__contains__('million') or text_tokens[inx + 1].__contains__('MILLION'):
                temp = str(num) + 'M'
            elif text_tokens[inx + 1].__contains__('billion') or text_tokens[inx + 1].__contains__('BILLION'):
                temp = str(num) + 'B'
            elif text_tokens[inx + 1].__contains__('t') or text_tokens[inx + 1].__contains__('T'):
                temp = str(num) + 'B'
            return temp


    def stem_terms(self, text_tokens):
        ps = PorterStemmer()
        for inx, term in enumerate(text_tokens):
            if term.isupper():
                temp = ps.stem(term).upper()
            else:
                temp = ps.stem(term)
            text_tokens.pop(inx)
            text_tokens.insert(inx, temp)
        return text_tokens

    def hyphen_handler(self, term):
        new_term = ''
        if re.findall("[A-Za-z]+[-][A-Za-z]", term):
            new_term = term
            new_term = new_term.split('-')
        elif re.findall("[A-Za-z]+[-]", term):
            new_term = term
            new_term = new_term.split('-')
        elif re.findall("[0-9]+[-]+[0-9]", term):
            return new_term
        elif re.findall("[0-9]+[-+]", term):
            new_term = term
            if term.__contains__('-'):
                new_term = new_term.split('-')
            elif term.__contains__('+'):
                new_term = new_term.split('+')
        elif re.findall("[A-Za-z]+[-_][19]", term) or term == 'COVID' or re.findall("[1-9]+[-_]", term):
            term = term.replace('-', '')
            term = term.replace('_', '')
        elif term == '3.7-':
            term = term.replace('-', '')
            term = term.replace('_', '')
        return new_term

    def covid_handler(self,text_tokens):
        while text_tokens.__contains__('covid') or text_tokens.__contains__('COVID'):
            if text_tokens.__contains__('covid'):
                inx = text_tokens.index('covid')
            elif text_tokens.__contains__('COVID'):
                inx = text_tokens.index('COVID')
            if inx+1 < len(text_tokens) and (text_tokens[inx+1] == '19' or text_tokens[inx+1] == '_19' or text_tokens[inx+1] == '-19'):

                text_tokens.pop(inx+1)
                term = text_tokens[inx] + '19'
                text_tokens.pop(inx)
                text_tokens.insert(inx, term)
            else:
                break

    def apostrophe_handler(self, text_tokens):
        while text_tokens.__contains__('’'):
            inx = text_tokens.index('’')
            if inx+1 < len(text_tokens) and inx-1 > 0:
                pre = text_tokens[inx-1] + '’' + text_tokens[inx+1]
                text_tokens.pop(inx-1)
                text_tokens.pop(inx - 1)
                text_tokens.pop(inx - 1)
                text_tokens.insert(inx-1, pre)
            else:
                break


    def parse_sentence(self, text, stemming):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        #doc = nlp(text)
        text_tokens = TweetTokenizer.tokenize(TweetTokenizer(),text)
        text_tokens = [w for w in text_tokens if w not in self.stop_words] #removing the stop words

        self.apostrophe_handler(text_tokens)
        # new format of parse
        flag = False
        for inx, token in enumerate(text_tokens):
            if flag == True:
                flag = False
                continue
            if token.__contains__("6.5k.Just"):
                print(token)
            if token.__contains__('#'):                 # hash tag
                hashed = self.hashTag_handler(token)
                if len(hashed) > 0:
                    text_tokens.extend(hashed)
            new_tokens = self.hyphen_handler(token)        # hyphen handler
            if new_tokens != '':
                text_tokens.pop(inx)
                for i in range(len(new_tokens)):
                    text_tokens.insert(inx+i, new_tokens[i])
                token = text_tokens[inx]           #update token after change
            new_token = self.upperCase_handler(token)           # upper case
            text_tokens.pop(inx)                # removes the element from his place in the list
            text_tokens.insert(inx, new_token)  # insert the new term where we removed the old one
            token = text_tokens[inx]
            number_token = self.number_handler(token, text_tokens, inx)        # all numbers handler thosand, milliom, rational
            if not number_token is None and number_token is not True:
                text_tokens.pop(inx)
                text_tokens.insert(inx, str(number_token))
            elif number_token == True:
                flag =True
            if token.__contains__('http') or token.__contains__('https'):    # remove url from full text
                text_tokens.pop(inx)

        # not need in loop
        self.covid_handler(text_tokens)    # covid handler
        if text_tokens.__contains__('%' or 'percent' or 'percentage'):  # percent
            self.percentage_handler(text_tokens)


        text_tokens_without_stopwords = [w for w in text_tokens if w not in self.stop_words]
        if stemming:
            text_tokens_without_stopwords = self.stem_terms(text_tokens_without_stopwords)
        return text_tokens_without_stopwords

    def parse_url(self, url_text):
        parsed_url = []
        splited_url = ''
        if len(url_text) > 0 and url_text != None:
            if url_text.__len__() > 2 and url_text.__contains__('https'):
                i = url_text.index('https')
                url_text = url_text[i:]
                if url_text.__contains__(':'):
                    splited_url = url_text.split(':')
                for inx in range(len(splited_url)):
                    if splited_url[inx].__contains__('t.co'):
                        continue
                    parsed_url += splited_url[inx].split('/')
                    while parsed_url.__contains__(''):
                            parsed_url.remove('')
                    for inx in range(len(parsed_url)):
                        if parsed_url[inx].__contains__('}{'):
                            temp = parsed_url[inx].split('}{')
                            parsed_url.pop(inx)
                            parsed_url.insert(inx, temp[1])
                            parsed_url.insert(inx, temp[0])
                        if parsed_url[inx].__contains__('['):
                            parsed_url[inx] = parsed_url[inx].lstrip('[')
                        if parsed_url[inx].__contains__(']'):
                            parsed_url[inx] = parsed_url[inx].strip(']')
                        if parsed_url[inx].__contains__('{'):
                            parsed_url[inx] = parsed_url[inx].lstrip('{')
                        if parsed_url[inx].__contains__('}'):
                            parsed_url[inx] = parsed_url[inx].strip('}')
                        if parsed_url[inx].__contains__('-'):
                            parsed_url += parsed_url[inx].split('-')
                            parsed_url.pop(inx)
                        if parsed_url[inx].__contains__('www.'):
                            parsed_url[inx] = parsed_url[inx].lstrip('www.')
        return parsed_url



    def parse_doc(self, doc_as_list,stemming=True):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-presenting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        if full_text.startswith('RT'):
            return None
        tokenized_text = self.parse_sentence(full_text, stemming)
        parsed_url = []
        if url != None and len(url) > 15:
            parsed_url.append(self.parse_url(url))
        if retweet_url != None and len(retweet_url) > 15:
            parsed_url.append(self.parse_url(retweet_url))
        if quote_url != None and len(quote_url) > 15:
            parsed_url.append(self.parse_url(quote_url))
        if quote_text != None and len(quote_text) > 15:
            parsed_url.append(self.parse_url(quote_text))
        if retweet_text != None and len(retweet_text) > 15:
            parsed_url.append(self.parse_url(retweet_text))
        if len(parsed_url) > 0:
            for w in parsed_url:
                for i in w:
                    if i.__contains__('https') or i.__contains__('http'):
                        continue
                    else:
                        tokenized_text.append(i)

        tokenized_text = [w for w in tokenized_text if
                          w.lower() not in self.stop_words]  # remove stop words second time
        doc_length = len(tokenized_text)  # after text operations.
        term_dict = dict()
        for inx, term in enumerate(tokenized_text):
            if term not in term_dict.keys() and term is not '' and term is not '':
                term_dict[term] = [1, [inx], 0.0]

            elif term is not '':
                term_dict[term][0] = term_dict[term][0] + 1
                term_dict[term][1].append(inx)
        max_fi = 0
        if len(term_dict) >= 1:
            max_fi = term_dict[max(term_dict, key=lambda k: term_dict[k][0])][0]
        for term in term_dict.keys():
            fi = term_dict[term][0]
            if max_fi != 0:
                term_dict[term][2] = fi / max_fi

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document

