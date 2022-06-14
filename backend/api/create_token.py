from base64 import b64encode
import os
import datetime

from images.models import Link_Token


def create_token(instance, delta_time, kwargs):    
    time = datetime.datetime.now()+datetime.timedelta(seconds=delta_time)
    token = str(b64encode(os.urandom(20)).decode('utf-8'))
    token = token.replace("/", '1').replace("+", '3').replace("=", '2')   
    link_token = Link_Token.objects.create(token=token,
    image = instance, expiration_time=time)
    link_token.save()
    return token