from django.db import models  # noqa F401



class Pokemon(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID покемона')
    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200, verbose_name='Название (англ.)')
    title_jp = models.CharField(max_length=200, verbose_name='Название (яп.)')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(null=True, verbose_name='Описание')
    next_evolution = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='previous_evolutions', verbose_name='Следующая эволюция')
    previous_evolution = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='next_evolutions', verbose_name='Предыдущая эволюция')


    def __str__(self):
        return format(self.title)


class PokemonEntity(models.Model):
    lat = models.FloatField(null=True, verbose_name='Широта')
    lon = models.FloatField(null=True, verbose_name='Долгота')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    appeared_at = models.DateTimeField(null=True, verbose_name='Дата и время появление')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Дата и время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')