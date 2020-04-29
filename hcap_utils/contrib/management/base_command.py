from django.core.management.base import BaseCommand as DjangoBaseCommand, CommandError


class BaseCommand(DjangoBaseCommand):
    verbosity = 1

    def handle(self, *args, **options):
        self.verbosity = options["verbosity"]

        try:
            self.safe_handle(*args, **options)
        except KeyboardInterrupt:
            raise CommandError("Interrupted")

    def safe_handle(self, *args, **options):
        pass

    def inform(self, message, depth=0, topic=False, style_func=None, ending=None):
        if self.verbosity > 0:
            if topic:
                message += ":"
                if style_func is None:
                    style_func = self.style.MIGRATE_HEADING

            if depth > 0:
                message = ("  " * depth) + message

            self.stdout.write(message, style_func, ending)

    def raise_message(self, message):
        raise CommandError(message)
