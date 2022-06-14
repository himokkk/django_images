from base64 import b64encode
import os
import datetime

from images.models import Link_Token


def create_token(instance, delta_time, kwargs):
    
    while 1:
        token = str(b64encode(os.urandom(20)).decode('utf-8'))
        token = token.replace("/", '1').replace("+", '3').replace("=", '2')
        time = datetime.datetime.now()+datetime.timedelta(seconds=delta_time)

        token_instance = None
        try:
            token_instance = Link_Token.objects.get(token=token)
        except:
            token_instance = Link_Token.objects.create(token=token,
            image=instance, expiration_time=time)
            token_instance.save()
            return token 

        if  instance is None:
            token_instance = Link_Token.objects.create(token=token,
            image=instance, expiration_time=time)
            token_instance.save()
            return token  

    return token