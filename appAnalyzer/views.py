from django.shortcuts import render, get_object_or_404
from .models import Channel,Message, Url


from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
import json
import operator
from django.core.serializers import deserialize
from django.core.paginator import Paginator

# Create your views here.

def Home(request):

    channels = Channel.objects.all()
    context = {
        'channels': channels
    }

    return render(request, 'home.html', context)

def Channels(request):
    return render(request, 'channels.html')

def Ranking(request):
    return render(request, 'ranking.html')

def Detail(request, id):
    channel = get_object_or_404(Channel, id_channel=id)
    messages = extractMessageFromJson(channel.messages)
    total_messages = len(messages)
    channel.messages =  messages

    report_words_list = AnalyseWordList(messages, channel.restricted_words)
    # Messages Paginator
    next_msgs, previous_msgs = GetMessagesPaginator(channel,request)

    urls = extractUrlsFromJson(channel.urls)
    total_urls = len(channel.urls)
    channel.urls = urls
    # Urls Paginator
    next_urls, previous_urls = GetUrlsPaginator(channel, request)

    media_list_all,media_list_page,next_media, previous_media = GetMediaPaginator(messages,request)

    tab_active = GetTabActive(request.GET.dict())

    recap_analise =  RecapResults(urls,media_list_all)
    print(int(channel.current_user_id))
    context = {
        'channel': channel,
        'next_page_messages': next_msgs,
        'previous_page_messages': previous_msgs,
        'total_messages': total_messages,
        'total_urls': total_urls,
        'next_page_urls': next_urls,
        'previous_page_urls': previous_urls,
        'tab_active': tab_active,
        'media_list':media_list_page,
        'previous_page_media':previous_media,
        'next_page_media':next_media,
        'recap_analise': recap_analise,
        'current_user_id': int(channel.current_user_id),
        'report_words_list': report_words_list
    }
    return render(request, 'channel-detail.html', context)

def RecapResults(urls, media_list):
    recap_urls=0
    recap_files = 0
    for item in urls:
        if item.classification == 'malicious':
            recap_urls =recap_urls + 1
    
    for item in media_list:
        if item.prediction and item.prediction != 'Harmless':
            recap_files =  recap_files + 1
    result = CalculateScoringChannel(len(urls),recap_urls,len(media_list),recap_files)
    print(result)
    return result


def CalculateScoringChannel(total_urls:int,recap_urls:int,total_media_list:int,recap_files:int):
    malware_threshold = 20
    percent = lambda part, whole:float(whole) / 100 * float(part)
    percentage_malware_url = percent(recap_urls,total_urls)
    percentage_malware_media = percent(recap_files,total_media_list)

    if percentage_malware_media > malware_threshold and percentage_malware_url > malware_threshold:
        return 'Malicious'
    elif (percentage_malware_media + percentage_malware_url) > 0:
        return 'Suspicious'
    else:
        return 'Safely'


def GetMediaPaginator(messages,request):
    media_list = []
    [media_list.append(item) for item in messages if item.id_media]
    paginator_media = Paginator(media_list, 10)
    page_number_media = request.GET.get('page_media', 1)
    page_media = paginator_media.get_page(page_number_media)

    if page_media.has_next():
        next_media = f'?page_media={page_media.next_page_number()}'
    else:
        next_media = ''

    if page_media.has_previous():
        previous_media = f'?page_media={page_media.previous_page_number()}'
    else:
        previous_media = ''

    return media_list,page_media, next_media, previous_media

def GetMessagesPaginator(channel,request):
    paginator_msgs = Paginator(channel.messages, 10)
    page_number_msgs = request.GET.get('page_msgs', 1)
    page_msgs = paginator_msgs.get_page(page_number_msgs)
    channel.messages = page_msgs

    if page_msgs.has_next():
        next_msgs = f'?page_msgs={page_msgs.next_page_number()}'
    else:
        next_msgs = ''

    if page_msgs.has_previous():
        previous_msgs = f'?page_msgs={page_msgs.previous_page_number()}'
    else:
        previous_msgs = ''
    return next_msgs, previous_msgs


def GetUrlsPaginator(channel,request):
    paginator_urls = Paginator(channel.urls, 10)
    page_number_urls = request.GET.get('page_urls', 1)
    page_urls = paginator_urls.get_page(page_number_urls)
    channel.urls = page_urls

    if page_urls.has_next():
        next_urls = f'?page_urls={page_urls.next_page_number()}'
    else:
        next_urls = ''

    if page_urls.has_previous():
        previous_urls = f'?page_urls={page_urls.previous_page_number()}'
    else:
        previous_urls = ''
    return next_urls, previous_urls


def GetTabActive(params):
    result = 'msgs'
    if params and 'page_urls' in params:
        result = 'urls'
    elif 'page_media' in params:
        result = 'media'
    return result


def extractMessageFromJson(msgs: []):
    messages = []
    for msg in msgs:
        messages.append(Message(**json.loads(msg)))
    return messages

def extractUrlsFromJson(urls: []):
    urls_new = []
    for url in urls:
        urls_new.append(Url(**json.loads(url)))
    return urls_new

def AnalyseWordList(messages, restricted_words: str):
    words_list = restricted_words.split(",")
    dict_words = dict.fromkeys(words_list , 0)
    for msg in messages:
        matching = [word for word in words_list if word in msg.message]
        for match in matching:
            if match in dict_words.keys():
                dict_words[match] +=1
    sorted_dict = dict(sorted(dict_words.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_dict
