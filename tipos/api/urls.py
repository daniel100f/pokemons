from tipos.api.views import TiposViewSet
from rest_framework import routers

router=routers.DefaultRouter()
router.register("",TiposViewSet,basename='tipos')

urlpatterns=router.urls