from django.db import models


class Ditina(models.Model):
    REGION_CHOICES = [
        ('UKR', 'Ukraina'),
        ('PL', 'Polska'),
        ('TU', 'Turcja'),
        ('JA', 'Japonia'),
        ('USA', 'USA'),
    ]

    GENDER_CHOICES = [
        ('M', 'Chłopiec'),
        ('K', 'Dziewczynka'),
    ]

    imya = models.CharField(max_length=100, verbose_name="Imię")
    prizvische = models.CharField(max_length=100, verbose_name='Nazwisko')
    plec = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Płeć', default='M')
    region = models.CharField(max_length=4, choices=REGION_CHOICES, verbose_name='Region')
    vik = models.PositiveIntegerField(verbose_name='Wiek')
    zrist = models.PositiveIntegerField(verbose_name='Wzrost (w cm)')
    pryimaie_gormony = models.BooleanField(default=False, verbose_name='Przyjmuje hormony')
    data_stvorennia = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    data_onovlennia = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

    class Meta:
        verbose_name = 'Dziecko'
        verbose_name_plural = 'Dzieci'
        ordering = ['prizvische', 'imya']

    def __str__(self):
        return f"{self.prizvische} {self.imya}"