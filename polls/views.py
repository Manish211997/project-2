from django.shortcuts import render,redirect
from django.template.loader import get_template
from polls.form import formed
# Create your views here.
from django.http import HttpResponse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import bs4
import requests
from gensim.summarization import summarize
from textblob import TextBlob

def index(request):
    form = formed()
    if request.method == "POST":
        form=formed(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if name=='':
                url=form.cleaned_data['url']
                if url=='':
                    return render(request,'polls/answer.html',{'url':None})
                else:
                    data=requests.get(url)
                    soup=bs4.BeautifulSoup(data.text,'html.parser')
                    send=[]
                    for para in soup.find_all('p'):
                        send.append(para.text)
                    text=""
                    for sen in send:
                        text=text+sen+" "
                    sid_obj = SentimentIntensityAnalyzer()
                    sentiment_dict = sid_obj.polarity_scores(text)
                    output=summarize(text,word_count=100)
                    blob=TextBlob(output)
                    nouns=blob.noun_phrases
                    url1 = ('https://newsapi.org/v2/everything?'
                            'q='+nouns[0]+'&'
                            'from=2019-04-04&'
                            'sortBy=popularity&'
                        'apiKey=72b95801dff84c9c8b26c84ced603aea')
                    news=requests.get(url1).json()
                    article=news["articles"]
                    result=[]
                    for ar in article:
                        result.append(ar["title"])
                    neg=format(sentiment_dict['neg'] * 100,'.2f')
                    pos=format(sentiment_dict['pos'] * 100,'.2f')
                    neu=format(sentiment_dict['neu'] * 100,'.2f')
                    return render(request,'polls/answer.html',{'mess':output,'url':url,'recieved':text,'pos':pos,'neg':neg,'neu':neu,'news':result,'topic':nouns[0]})
            else:
                output=summarize(name,word_count=100)
                sid_obj = SentimentIntensityAnalyzer()
                sentiment_dict = sid_obj.polarity_scores(output)
                blob=TextBlob(output)
                nouns=blob.noun_phrases
                url1 = ('https://newsapi.org/v2/everything?'
                       'q='+nouns[0]+'&'
                       'from=2019-04-04&'
                        'sortBy=popularity&'
                        'apiKey=72b95801dff84c9c8b26c84ced603aea')
                news=requests.get(url1).json()
                article=news["articles"]
                result=[]
                for ar in article:
                   result.append(ar["title"])
                neg=format(sentiment_dict['neg'] * 100,'.2f')
                pos=format(sentiment_dict['pos'] * 100,'.2f')
                neu=format(sentiment_dict['neu'] * 100,'.2f')
                return render(request,'polls/answer.html',{'mess':output,'recieved':name,'pos':pos,'neg':neg,'neu':neu,'news':result,'topic':nouns[0]})
        else:
            name="NO text"
            return render(request,'polls/index.html',{'form':name})
    return render(request,'polls/index.html',{'form':form})

