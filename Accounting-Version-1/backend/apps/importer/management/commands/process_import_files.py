from django.core.management.base import BaseCommand
from apps.importer.models import ImportFile
from apps.importer.services import process_import_file

class Command(BaseCommand):
    help = 'Process all pending import files'

    def handle(self, *args, **options):
        pending = ImportFile.objects.filter(status='pending')
        count = pending.count()
        self.stdout.write(f"Found {count} pending import files")
        for imp in pending:
            # Use pk rather than id for primary key reference
            self.stdout.write(f"Processing {imp.pk}: {imp.file.name} (type: {imp.file_type})")
            errors = process_import_file(imp)
            if errors:
                self.stdout.write(self.style.WARNING(f"Completed with {len(errors)} errors"))
            else:
                self.stdout.write(self.style.SUCCESS("Completed successfully"))
