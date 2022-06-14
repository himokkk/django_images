from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (List_Images, Upload_Image,
 OriginalImageView, TokenLinkView, ThumbnailView, ExpireView)


urlpatterns = [
    path(r'upload-image/', Upload_Image.as_view()),
    path(r'images/token/<string>', TokenLinkView.as_view()),
    path(r'images/media/<int:id>', OriginalImageView.as_view()),    
    path(r'images/thumbnail/<string>', ThumbnailView.as_view()),    
    path(r'images/create-expiring/<string>', ExpireView.as_view()),       
    path(r'list-images/', List_Images.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)