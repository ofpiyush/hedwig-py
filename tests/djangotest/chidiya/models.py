from django.db import models


# Create your models here.

class BaseTest(models.Model):
    class Meta:
        abstract = True
    char = models.CharField(max_length=255, null=False, blank=False)
    int = models.IntegerField(null=False, blank=False)
    nullable = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField()


class BasicTest(BaseTest):

    def natural_key(self):
        return self.char, self.int, self.nullable, self.date


class HiddenTest(BaseTest):
    class Hedwig:
        fields = False


class ForeignKeyTest(BaseTest):
    class Hedwig:
        fields = ('char', 'int', 'basic',)
    basic = models.ForeignKey(BasicTest)


class ManyToManyTest(BaseTest):
    basic = models.ManyToManyField(BasicTest)
    uuid = models.UUIDField()
    url = models.URLField()
