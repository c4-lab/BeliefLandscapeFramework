import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language
from allTokens import *
from langdetect import detect
my_nlp = None

extraChar = {'&quot;': '"',
 '&amp;': 'and',
 '&lt;': '<',
 '&gt;': '>',
 '&nbsp;': 'un-linebreak-able space',
 '&iexcl;': '¡',
 '&cent;': '¢',
 '&pound;': '£',
 '&curren;': '¤',
 '&yen;': '¥',
 '&brvbar;': '¦',
 '&sect;': '§',
 '&uml;': '¨',
 '&copy;': '©',
 '&ordf;': 'ª',
 '&laquo;': '«',
 '&not;': '¬',
 '&shy;': '\xad',
 '&reg;': '®',
 '&macr;': '¯',
 '&deg;': '°',
 '&plusmn;': '±',
 '&sup2': '²',
 '&sup3;': '³',
 '&acute;': '´',
 '&micro;': 'µ',
 '&para;': '¶',
 '&middot;': '·',
 '&cedil;': '¸',
 '&sup1;': '¹',
 '&ordm;': 'º',
 '&raquo;': '»',
 '&frac14;': '¼',
 '&frac12;': '½',
 '&frac34;': '¾',
 '&iquest;': '¿',
 '&times;': '×',
 '&divide;': '÷',
 '&ETH;': 'Ð',
 '&eth;': 'ð',
 '&THORN;': 'Þ',
 '&thorn;': 'þ',
 '&AElig;': 'Æ',
 '&aelig;': 'æ',
 '&OElig;': 'Œ',
 '&oelig;': 'œ',
 '&Aring;': 'Å',
 '&Oslash;': 'Ø',
 '&Ccedil;': 'Ç',
 '&ccedil;': 'ç',
 '&szlig;': 'ß',
 '&Ntilde;': 'Ñ',
 '&ntilde;': 'ñ'}

special = {
    "’":"'",
    "‘":"'",
    "`":"'",
    '“':'"',
    '”':'"',
    '…':"."
}

@Language.factory('language_detector')
def language_detector(nlp, name):
    return LanguageDetector()

def get_nlp():
    global my_nlp
    if not my_nlp:        
        my_nlp = spacy.load('en_core_web_lg')
        my_nlp.add_pipe('language_detector')
    return my_nlp

def is_english(text):
    doc = get_nlp()(text)
    return doc._.language['score']>0.95
        
def removeTags(text,splitter):
    div = text.split(splitter)
    endExists = True
    i = len(div)-1
    while i>=0 and endExists:
        if len(div[i].strip().split(" "))  == 1:
            div.pop(i)
            i-=1
        else:
            endExists = False
        
    return " "+splitter.join(div).strip()

def removeTagsFromStart(text,splitter):
    div = text.split(splitter)
    endExists = True
    i = 0
    while len(div)>0 and endExists:
        if len(div[i].strip().split(" "))  == 1:
            div=div[i+1:]
        else:
            div[i] = splitter+div[i]
            endExists = False
    if len(div) == 0:
        return ''
    splitfirst = div[0].split(" ")
    if "you" in splitfirst[1].lower() and "@" in splitfirst[0]:
        splitfirst[1] = splitfirst[0]
        splitfirst = splitfirst[1:]
        div[0] = " ".join(splitfirst)
    if "@" in splitfirst[0].strip()[0:2]:
        splitfirst = splitfirst[1:]
        div[0] = " ".join(splitfirst)
    return " ".join(div).strip()


def removeRT(text):
    if text[0:2] == 'RT':
        return ":".join(text.split(":")[1:]).strip()
    return text  

def clean_tweet(text,removeFromMiddle):
    text = text.strip()
    for key,value in special.items():
        text = re.sub(key,value,text)
    for key,value in abbr_dict.items():
        text = re.sub(key,value,text,flags=re.I)
    for key,value in extraChar.items():
        text = re.sub(key,value,text)
    
        #print(text)
    if removeFromMiddle:
        text = re.sub("@[A-Za-z0-9_]+","", text)
        text = re.sub("#[A-Za-z0-9_]+","", text)
    text = re.sub(r"http\S+", "", text)
    text = emoji_pattern.sub(r' ', text)
    text = removeTags(text,"#")
    text = removeTags(text,"@")
    text = removeTags(text,"#")
    text = removeTagsFromStart(text,"@")
    text = removeRT(text)
    text = re.sub(' +', ' ', text)
    text = re.sub("@",'',text)
    text = re.sub("#",'',text)
    text = re.sub(r'[\n\r]+',r'\n',text)
    text = re.sub('(?<![.?!])\n',". ",text)
    text = re.sub('\n'," ",text)
    #text = ' '.join(text.replace('\r', ' ').split())
    text = re.sub("\s+"," ",text)
    #text = re.sub(r"[^A-Za-z.!?'', ]",'',text)
    
    if not is_english(text):
        return ''
    return text.strip()