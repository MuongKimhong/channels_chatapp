from django.contrib import admin
from django.urls import path, include


from rest_framework_simplejwt.views import TokenRefreshView
from api.views import CustomTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]
