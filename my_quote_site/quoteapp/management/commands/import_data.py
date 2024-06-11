import json
from django.core.management.base import BaseCommand
from quoteapp.models import Autors, Tag, Quotes

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('authors_file', type=str)
        parser.add_argument('quotes_file', type=str)

    def handle(self, *args, **kwargs):
        authors_file = kwargs['authors_file']
        quotes_file = kwargs['quotes_file']

        try:
            with open(authors_file, 'r', encoding='utf-8') as f:
                authors_data = json.load(f)
                for author in authors_data:
                    Autors.objects.get_or_create(
                        name=author['fullname'],
                        born_date=author['born_date'],
                        born_location=author['born_location'],
                        description=author['description']
                    )
            
            with open(quotes_file, 'r', encoding='utf-8') as f:
                quotes_data = json.load(f)
                for quote_data in quotes_data:
                    author = Autors.objects.get(name=quote_data['author'])
                    quote_instance = Quotes.objects.create(
                        author=author,
                        quote=quote_data['quote']
                    )
                    for tag_name in quote_data['tags']:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        quote_instance.tags.add(tag)

            self.stdout.write(self.style.SUCCESS('Successfully imported authors and quotes'))

        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f'File not found: {e.filename}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
