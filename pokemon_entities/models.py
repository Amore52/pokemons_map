from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200, verbose_name='Название (англ.)')
    title_jp = models.CharField(max_length=200, verbose_name='Название (яп.)')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(null=True, verbose_name='Описание')
    evolved_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name='Эволюционировал из', related_name='evolutions_to')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон', related_name='entities')
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время появление')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время исчезновения')
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strength = models.IntegerField(verbose_name='Сила')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Выносливость')

    def __str__(self):
        return f"{self.pokemon.title} (Уровень {self.level}, Координаты: {self.lat}, {self.lon})"