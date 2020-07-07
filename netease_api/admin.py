from django.contrib import admin

# Register your models here.
from netease_api.models import User, PlayList, Artist, Album, Song, Tag, Alias

admin.site.register(User)
admin.site.register(PlayList)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Tag)
admin.site.register(Alias)
