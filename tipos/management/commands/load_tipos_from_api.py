# pokemons/management/commands/load_types_from_api.py

import requests
from django.core.management.base import BaseCommand, CommandError
from tipos.models import Tipos # ¡Importa tu modelo Type!

class Command(BaseCommand):
    help = 'Carga los tipos de Pokémon desde la PokeAPI a la base de datos.'

    def handle(self, *args, **options):
        types_url = 'https://pokeapi.co/api/v2/type/'
        self.stdout.write(self.style.SUCCESS('Iniciando carga de tipos de Pokémon...'))

        try:
            response = requests.get(types_url)
            response.raise_for_status() # Lanza un error para códigos de estado HTTP incorrectos
            types_data = response.json()

            for type_entry in types_data['results']:
                type_name = type_entry['name']
                # Necesitamos obtener el ID del tipo haciendo una petición a su URL de detalle
                type_detail_url = type_entry['url']
                
                detail_response = requests.get(type_detail_url)
                detail_response.raise_for_status()
                type_detail = detail_response.json()
                
                type_id = type_detail['id'] # El ID del tipo

                # Usamos update_or_create para evitar duplicados y actualizar si ya existe
                type_obj, created = Tipos.objects.update_or_create(
                    id=type_id,
                    defaults={'name': type_name}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'    Creado nuevo Tipo: {type_obj.name} (ID: {type_obj.id})'))
                else:
                    self.stdout.write(self.style.WARNING(f'    Actualizado Tipo existente: {type_obj.name} (ID: {type_obj.id})'))

            self.stdout.write(self.style.SUCCESS('Carga de tipos completada exitosamente.'))

        except requests.exceptions.RequestException as e:
            raise CommandError(f'Error al conectarse a la PokeAPI para tipos: {e}')
        except Exception as e:
            raise CommandError(f'Ocurrió un error inesperado durante la carga de tipos: {e}')