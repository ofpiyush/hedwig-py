from .serializers import BasicTestSerializer, HiddenTestSerializer, ForeignKeyTestSerializer, ManyToManyTestSerializer
from .models import BasicTest, HiddenTest, ForeignKeyTest, ManyToManyTest
from rest_framework.viewsets import ModelViewSet


class BasicTestViewSet(ModelViewSet):
    queryset = BasicTest.objects.all()
    serializer_class = BasicTestSerializer


class HiddenTestViewSet(ModelViewSet):
    queryset = HiddenTest.objects.all()
    serializer_class = HiddenTestSerializer


class ForeignKeyTestViewSet(ModelViewSet):
    queryset = ForeignKeyTest.objects.all()
    serializer_class = ForeignKeyTestSerializer

class ManyToManyTestViewSet(ModelViewSet):
    queryset = ManyToManyTest.objects.all()
    serializer_class = ManyToManyTestSerializer