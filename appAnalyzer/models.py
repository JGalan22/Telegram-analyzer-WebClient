from django.db import models
from django.contrib.postgres.fields import JSONField

from datetime import date, datetime

# Create your models here.
class Channel(models.Model):
    id_channel = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    is_channel = models.BooleanField(blank=True, null=True)
    verified = models.BooleanField(blank=True, null=True)
    megagroup = models.BooleanField(blank=True, null=True)
    participants_count = models.IntegerField(blank=True, null=True)
    access_hash = models.CharField(max_length=80, blank=True, null=True)
    username = models.CharField(max_length=80, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    current_user_id = models.CharField(max_length=500,blank=True)
    restricted_words = models.CharField(max_length=500,blank=True)
    messages =JSONField()  
    urls = JSONField() 

    class Meta:
        managed = False
        db_table = 'channel'


class Message():
    
    def __init__(self,
                id_msg: int,
                id_from: int,
                date: datetime,
                message: str,
                id_media: int, # For the message that is a file
                prediction: str,
                detected_by: str,
                type: str,
                sha256: str,
                sha1: str,
                md5: str,
                hash: str,
                file_name: str,
                access_hash_media:int,
                size_media: int):
        self.id_msg = id_msg
        self.id_from = id_from
        self.date = date
        self.message = message
        self.prediction = prediction #whether if the media is detected as a malware
        self.detected_by = detected_by #whether if the media is detected as a malware
        self.type = type
        self.sha256 = sha256
        self.sha1 = sha1
        self.md5 = md5
        self.hash = hash
        if id_media:
            self.id_media = id_media
            self.file_name = file_name
            self.access_hash_media = access_hash_media
            self.size_media = size_media
        else:
            self.id_media = None
            self.file_name = None
            self.access_hash_media = None
            self.size_media = None


    def __str__(self):
        type = "File" if not self.id_media == '-' else "Message"
        if not self.id_media:
            return f"{type} \t {self.id_msg} \t {self.id_from} \t {self.message} \t {self.date}"
        else:
            return f"{type} \t {self.id_msg} \t {self.id_from} \t {self.message} \t ID Media: {self.id_media} \t File_name: {self.file_name} \t Size:{self.size_media} bytes"

    def GetRepresentationInList(self):
        type = "File" if not self.id_media == '-' else "Message"
        return [type,str(self.id_msg), str(self.id_from), self.message,str(self.id_media),self.file_name,str(self.size_media)]


class Url():

    def __init__(self,
                url: str,
                malicious,
                detected_by: str,
                date: datetime,
                urlchecksum: str,
                classification: str,
                info_malicious: []):
        self.url = url
        self.malicious = malicious
        self.detected_by = detected_by
        self.date = date
        self.urlchecksum = urlchecksum
        self.classification = classification
        self.info_malicious = info_malicious