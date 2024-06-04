from django.db import models

class MLModule(models.Model):
    code = models.CharField("Название модуля", max_length=50)
    address = models.CharField("адрес модуля", max_length=100)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'ML модуль'
        verbose_name_plural = 'ML модули'