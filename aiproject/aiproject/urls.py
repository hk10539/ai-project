from django.contrib import admin
from django.urls import path

from home.views import (
    pdf_length,
    metadata,
    readdata,
    build_faiss_index,
    semantic_search
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/pdf-length/', pdf_length),
    path('api/metadata/', metadata),
    path('api/read-data/', readdata),

    path('api/faiss/build/', build_faiss_index),
    path('api/faiss/search/', semantic_search),
]
