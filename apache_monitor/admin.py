from django.contrib import admin

from .models import *

admin.site.register(RemoteHost)
admin.site.register(UserAgent)
admin.site.register(SearchEngine)
admin.site.register(RequestedUri)
admin.site.register(Referer)
admin.site.register(LogEntry)
admin.site.register(IgnoredUri)
admin.site.register(IgnoredHost)
admin.site.register(CacheableParam)
