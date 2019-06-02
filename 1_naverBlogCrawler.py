from bs4 import BeautifulSoup as bs
import requests
import pandas as pd



#시간 설정
count = 0
blog_url = []
date_posts = []
#2008-02-10 ~ 2019-02-10 기간의 텍스트 크롤링
start_year = ['20080210','20090210','20100210','20110210','20120210','20130210','20140210','20150210',
              '20160210','20170210','20180210']
final_year = ['20090210','20100210','20110210','20120210','20130210','20140210','20150210','20160210',
              '20170210','20180210','20190210']

for i in range(len(start_year)):
    for p in range(100):
        
        html = requests.get('https://search.naver.com/search.naver?date_from=' + start_year[i] + '&date_option=8&date_to=' + final_year[i] + '&dup_remove=1&nso=so%3Add%2Cp%3Afrom20180201to20190214&post_blogurl=&post_blogurl_without=&query=크루즈%20여행&sm=tab_pge&srchby=all&st=date&where=post&start='+str(1+10*p))    
        soup = bs(html.text, 'html.parser')
        url_date = soup.select('dd.txt_inline')
        urlWay = soup.select('a.sh_blog_title._sp_each_url._sp_each_title')
         
#blog_url에 url입력
#date_post에 포스티 날짜 입력
        for i in range(len(urlWay)):
            date_posts.append(url_date[i].getText().replace('. ',''))
            print(url_date[i].getText())
            count += 1
            print(count)
            blog_url.append(urlWay[i]['href'])

#가져온 url에 앞에 'https://blog.'를 입력하여 완전한 url생성
naverUrl = []
for u in range(len(blog_url)):
    if blog_url[u].split('naver')[0] =='https://blog.':
        naverUrl.append(blog_url[u])

#user_id와 login번호를 가져와 보이는 사이트의 값이 아닌 텍스트를 가져오는 창에 들어 갈 수 있게 한다.

user_id = []
logNums = []
count = 0
for i in range(len(naverUrl)):
     try:  
        a = naverUrl[i].split('/')
        user_id.append(a[3].split('?')[0]) 
        logNums.append(a[3].split('=')[2])
        count += 1
     except IndexError or IndentationError as e:
        count += 1
        print('pass')
        pass

count_put = 0
count_pass = 0

text_list = []

for f in range(len(user_id)):
    #진짜로 텍스트를 가지고 있는 url
    theUrl = requests.get('https://blog.naver.com/PostView.nhn?blogId='+ user_id[f] +'&logNo=' + logNums[f] + '&redirect=Dlog&widgetTypeCall=true&directAccess=false')
    soup = bs(theUrl.text,'html.parser')
    text_craw = soup.select('div.se-component.se-l-default')
    
    #포스팅 글이 있으면 엔터를 공백으로 바꾸어서 text_list에 입력한다.
    try:
        if len(text_craw) > 0:
            count_put += 1
            print(count_put)
            for i in text_craw:
                if len(i.getText().replace('\n','')[0]) == 0:
                    text_list.append('0')
                    print('0')
                else:
                    text_list.append(i.getText().replace('\n',''))
                
                
        else:
            count_put += 1
            theUrl = requests.get('https://blog.naver.com/PostView.nhn?blogId='+ user_id[f] +'&logNo=' + logNums[f] + '&redirect=Dlog&widgetTypeCall=true&directAccess=false')    
            soup = bs(theUrl.text,'html.parser')
            text_craw = soup.select('div[id=postViewArea]')
            print(count_put)
            for i in text_craw:
                if len(i.getText().replace('\n','')[0]) == 0:
                    text_list.append('0')    
                    print('0')
                else:
                    text_list.append(i.getText().replace('\n',''))
    except IndexError as e:
        text_list.append('0')
        print('0')
        


#인덱스 리스트 생성
indx = []
for i in range(len(text_list)):
    indx.append(i)
    


naverBlogDf = pd.DataFrame(data=text_list)


file = open('C:/Users/Administrator/Desktop/nb_text.txt','wt', encoding = 'utf-8')

for i in range(len(text_list)):
    file.write(str(naverBlogDf))







#results = pd.DataFrame(data=naverBlogDf)
#results.to_csv("naverBlogDf3.csv",index=0, encoding = 'utf-8')
#print(results)



