# pokemons/management/commands/load_pokemons_from_api.py

# pokemons/management/commands/load_pokemons_from_api.py

import requests
from django.core.management.base import BaseCommand, CommandError
from pokemons.models import Pokemons # ¡Importa el modelo Type también!
from tipos.models import Tipos
from decimal import Decimal

class Command(BaseCommand):
    help = 'Carga Pokémon desde la PokeAPI a la base de datos, incluyendo estadísticas, detalles y tipos.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=151,
            help='Número de Pokémon a cargar desde la PokeAPI.',
        )
        parser.add_argument(
            '--offset',
            type=int,
            default=0,
            help='Número de Pokémon a saltar desde el inicio de la lista.',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        offset = options['offset']
        base_url = 'https://pokeapi.co/api/v2/pokemon/'

        self.stdout.write(self.style.SUCCESS(f'Iniciando carga de Pokémon (limit={limit}, offset={offset})...'))

        try:
            # Petición principal para obtener la lista de Pokémon
            list_response = requests.get(f'{base_url}?offset={offset}&limit={limit}')
            list_response.raise_for_status()
            pokemon_list = list_response.json()['results']

            if not pokemon_list:
                self.stdout.write(self.style.WARNING('No se encontraron Pokémon en el rango especificado.'))
                return

            for index, pokemon_data in enumerate(pokemon_list):
                pokemon_name_from_list = pokemon_data['name']
                pokemon_detail_url = pokemon_data['url']

                self.stdout.write(f'Procesando: {pokemon_name_from_list} ({index + 1}/{len(pokemon_list)})')

                # Obtener detalles de cada Pokémon individual
                detail_response = requests.get(pokemon_detail_url)
                detail_response.raise_for_status()
                detail = detail_response.json()

                pokemon_id = detail['id']
                pokemon_name = detail['name']
                
                pokemon_height = detail.get('height')
                if pokemon_height is not None:
                    pokemon_height = Decimal(str(pokemon_height)) / Decimal('10.0') # Convertir a metros
                
                pokemon_weight = detail.get('weight')
                if pokemon_weight is not None:
                    pokemon_weight = Decimal(str(pokemon_weight)) / Decimal('10.0') # Convertir a kilogramos
                
                pokemon_image_url = detail['sprites'].get('front_default', '')
                if pokemon_image_url is None:
                    pokemon_image_url = ''

                vida = None
                ataque = None
                defensa = None
                velocidad = None

                for stat in detail.get('stats', []):
                    stat_name = stat['stat']['name']
                    base_stat_value = stat['base_stat']

                    if stat_name == 'hp':
                        vida = base_stat_value
                    elif stat_name == 'attack':
                        ataque = base_stat_value
                    elif stat_name == 'defense':
                        defensa = base_stat_value
                    elif stat_name == 'speed':
                        velocidad = base_stat_value
                
                # Crear o actualizar el Pokémon
                pokemon_obj, created = Pokemons.objects.update_or_create(
                    id=pokemon_id,
                    defaults={
                        'name': pokemon_name,
                        'image': pokemon_image_url,
                        'vida': vida,
                        'ataque': ataque,
                        'defensa': defensa,
                        'velocidad': velocidad,
                        'altura': pokemon_height,
                        'peso': pokemon_weight,
                    }
                )

                # --- ¡NUEVO CÓDIGO PARA TIPOS! ---
                # Borra los tipos existentes para este Pokémon antes de añadir los nuevos
                # Esto es importante si el Pokémon ya existía y sus tipos cambiaron en la API
                pokemon_obj.types.clear() 

                # La API devuelve los tipos en 'detail['types']' como una lista
                for type_info in detail.get('types', []):
                    type_name_from_api = type_info['type']['name']
                    try:
                        # Busca el objeto Type que ya cargamos en la DB
                        type_obj = Tipos.objects.get(name=type_name_from_api)
                        pokemon_obj.types.add(type_obj) # Asigna el tipo al Pokémon
                    except Tipos.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f'    ADVERTENCIA: Tipo "{type_name_from_api}" no encontrado en la DB para {pokemon_name}. '
                            'Asegúrate de haber ejecutado load_types_from_api primero.'
                        ))
                # --- FIN DEL NUEVO CÓDIGO PARA TIPOS ---


                if created:
                    self.stdout.write(self.style.SUCCESS(f'    Creado nuevo Pokémon: {pokemon_obj.name} (ID: {pokemon_obj.id})'))
                else:
                    self.stdout.write(self.style.WARNING(f'    Actualizado Pokémon existente: {pokemon_obj.name} (ID: {pokemon_obj.id})'))

            self.stdout.write(self.style.SUCCESS('Carga de Pokémon completada exitosamente.'))

        except requests.exceptions.RequestException as e:
            raise CommandError(f'Error al conectarse a la PokeAPI: {e}')
        except Exception as e:
            raise CommandError(f'Ocurrió un error inesperado durante la carga: {e}')