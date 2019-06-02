
from konlpy.tag import Twitter
import pandas as pd


def clean_text(txt):
    try:
        txt = txt.replace(u'\xa0','')
        txt = txt.replace('\t','')
        txt = txt.replace('\n','')
        return txt
    except AttributeError:
        return 'ㅋ'
    
# 네이버 블로그 포스팅, 트위터 크롤링 데이터 불러오기    
nb_text = pd.read_csv('C:/hackerthon/nb_text.csv')
nb_text = nb_text['0']
tw_text = pd.read_csv('C:/hackerthon/tw_text.csv', encoding='ms949')
tw_text = tw_text['text']

# 긍정, 부정 사전
positive = ['좋다','아름답다','즐기다','멋지다','특별하다','화려하다','독특하다','즐겁다','좋다','저렴하다']
negative = ['비싸다','안되다','늦다','오래되다','낡다','지치다', '춥다','아쉽다','힘들다','없다']

# 결과를 저장할 DataFrame
nb_result_pn=pd.DataFrame(
        data = {'text':[],
                'pos_neg':[]})
tw_result_pn=pd.DataFrame(
        data = {'text':[],
                'pos_neg':[]})

# Naver Blog 포스팅 감정분석    
t = Twitter()
for idx,s in enumerate(nb_text):
    s = clean_text(s)
    nb_token_pn = t.pos(s, norm=True, stem=True)
    text=[]
    pos_neg = 0  # 긍정부정 점수
    pos = 0  # 긍정 점수
    neg = 0  # 부정 점수

    for word in nb_token_pn:
        if word[1] in ['Noun', 'Verb', 'Adjective', 'Alpha', 'Determiner', 'Conjunction', 'Number', 'Adverb', 'VerbPrefix']:
            text.append(word[0])
            if word[0] in positive:
                pos += 1
            elif word[0] in negative:
                neg -= 1 
    nb_result_pn.loc[idx, 'text'] = str(text)
    nb_result_pn.loc[idx, 'pos_neg'] = pos+neg

print("naver 완료")        

# 트위터 감정분석
for idx,s in enumerate(tw_text):
    s = clean_text(s)
    tw_token_pn = t.pos(s, norm=True, stem=False)
    text=[]
    pos_neg = 0  # 긍정부정 점수
    pos = 0  # 긍정 점수
    neg = 0  # 부정 점수

    for word in tw_token_pn:
        if word[1] in ['Noun', 'Verb', 'Adjective', 'Alpha', 'Determiner', 'Conjunction', 'Number', 'Adverb', 'VerbPrefix']:
            text.append(word[0])
            if word[0] in positive:
                pos += 1
            elif word[0] in negative:
                neg -= 1
    tw_result_pn.loc[idx, 'text'] = str(text)
    tw_result_pn.loc[idx, 'pos_neg'] = pos+neg

print("twitter 완료")        



nb_pos = len(nb_result_pn[nb_result_pn['pos_neg']>0])/len(nb_result_pn)
nb_neg = len(nb_result_pn[nb_result_pn['pos_neg']<0])/len(nb_result_pn)
tw_pos = len(tw_result_pn[tw_result_pn['pos_neg']>0])/len(tw_result_pn)
tw_neg = len(tw_result_pn[tw_result_pn['pos_neg']<0])/len(tw_result_pn)


print("Naver 긍정 : ", nb_pos)
print("Naver 부정 : ", nb_neg)
print("Twitter 긍정 : ", tw_pos)
print("Twitter 부정 : ", tw_neg)





