'''
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
'''
from django.conf.urls import url, include
from django.urls import re_path,  path
from django.contrib import admin

admin.site.site_header = "Dramatis Personae Administration"
admin.site.site_title = "Dramatis Personae Administration portal"
admin.site.index_title = "Welcome to Dramatis Personae. Be a good gamemaster."

urlpatterns = [
    re_path('admin/', admin.site.urls),
    path('', include('collector.urls')),
    path('', include('scenarist.urls')),
    path('', include('optimizer.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # new
  #re_path('__debug__', include(debug_toolbar.urls)),
]
