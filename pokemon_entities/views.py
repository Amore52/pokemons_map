import folium
import json

from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntity



MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)

def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_pokemon_image_url(pokemon, request):
    if pokemon.image:
        return request.build_absolute_uri(pokemon.image.url)
    return DEFAULT_IMAGE_URL


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = timezone.localtime()
    active_entities = PokemonEntity.objects.filter(appeared_at__lte=now,
                                                   disappeared_at__gte=now).select_related('pokemon')
    for pokemon_entity in active_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_pokemon_image_url(pokemon_entity.pokemon, request)
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_pokemon_image_url(pokemon, request),
            'title_ru': pokemon.title
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemons_on_page = {
        'pokemon_id': pokemon.id,
        'img_url': get_pokemon_image_url(pokemon, request),
        'title_ru': pokemon.title,
        'title_en' : pokemon.title_en,
        'title_jp' : pokemon.title_jp,
        'description': pokemon.description,
    }
    if pokemon.evolved_from:
        evolved_from = pokemon.evolved_from
        pokemons_on_page['previous_evolution'] = {
            'pokemon_id': evolved_from.id,
            'title_ru': evolved_from.title,
            'img_url': get_pokemon_image_url(evolved_from, request),
        }

    evolutions = pokemon.evolutions.all()
    if evolutions.exists():
        next_evolution = evolutions.first()
        pokemons_on_page['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'title_ru': next_evolution.title,
            'img_url': get_pokemon_image_url(next_evolution, request),
        }


    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon.entities.filter(
            appeared_at__lte=timezone.localtime(),
            disappeared_at__gte=timezone.localtime()):
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            get_pokemon_image_url(pokemon, request))

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
