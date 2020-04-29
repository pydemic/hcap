import csv

from django.core.management import call_command

from hcap_utils.contrib.management import BaseCommand
from hcap_utils.models import SeedState


class BaseSeedCommand(BaseCommand):
    app = "app"
    model = "model"

    context = None
    kind = "base"

    model_verbose_name = None
    model_verbose_name_plural = None

    context_choices = None
    default_context = None

    raise_on_failure = True

    def __init__(self, *args, **kwargs):
        if self.model_verbose_name is None:
            self.model_verbose_name = self.model

        if self.model_verbose_name_plural is None:
            self.model_verbose_name_plural = self.model_verbose_name + "s"

        self.help = f"Seed {self.app} {self.model_verbose_name} {self.kind} data"

        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        if self.context_choices is not None:
            if self.default_context is None:
                self.default_context = self.context_choices[0]

            parser.add_argument(
                "context",
                choices=self.context_choices,
                nargs="?",
                const=True,
                default=self.default_context,
                help="Seed context",
            )

        parser.add_argument(
            "--no-wait-db",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="If set, command will not check database connection",
        )

        parser.add_argument(
            "--migrate",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="If set, command will migrate database before seeding",
        )

    def safe_handle(self, *args, **kwargs):
        self.context = kwargs.get("context") or "default"

        if kwargs.get("no_wait_db") is False:
            call_command("wait_db", verbosity=self.verbosity)

        if kwargs.get("migrate") is True:
            call_command("migrate", verbosity=self.verbosity)

        self.inform(
            f'Seeding "{self.context}" {self.app} {self.model_verbose_name} {self.kind} data',
            topic=True,
        )

        (state, created) = SeedState.objects.get_or_create(
            app=self.app, model=self.model, kind=self.kind
        )

        if state.seeded is False:
            self.seed()
            state.context = self.context
            state.seeded = True
            state.full_clean()
            state.save()
        else:
            self.inform(
                f"{self.app.title()} {self.model_verbose_name} {self.kind} data already seeded",
                depth=1,
            )
            self.inform(f"context: {state.context}", depth=2)
            self.inform(f"seed date: {state.seeded_at}", depth=2)

    def seed(self):
        self.raise_message("seed method must be overwritten in order to execute command.")

    def seed_from_csv(self, csv_file_path, **kwargs):
        depth = kwargs.get("depth", 1)

        self.inform(f'Seeding from "{csv_file_path}" csv file', topic=True, depth=depth)

        kwargs["depth"] = depth + 1

        with open(str(csv_file_path) + ".csv", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            self.seed_many(reader, **kwargs)

    def seed_many(self, items, **kwargs):
        total_seeded = 0
        for item in items:
            try:
                self.seed_one(item, **kwargs)

                if self.verbosity > 1:
                    self.inform(self.style.SUCCESS(" OK"))

                total_seeded += 1
            except Exception as exception:
                if self.verbosity > 1:
                    self.inform(self.style.NOTICE(" FAILED"))

                if self.raise_on_failure is True:
                    raise exception

        if self.verbosity >= 1:
            styled_total_seeded = self.style.SUCCESS(str(total_seeded))
            depth = kwargs.get("depth", 1)
            self.inform(
                f"Seeded {styled_total_seeded} {self.model_verbose_name_plural}", depth=depth
            )

    def seed_one(self, item, **kwargs):
        model = self.fetch_model(item)

        if self.verbosity > 1:
            if hasattr(model, "id") and model.id is not None:
                action = f"Updating {model}..."
            else:
                action = f"Seeding {model}..."
            depth = kwargs.get("depth", 1)
            self.inform(action, depth=depth, ending="")

        model.full_clean()
        model.save()
        self.fetch_relations(model, item)

    def fetch_model(self, item):
        self.raise_message(
            "fetch_model method must be overwritten in order to use seed_one method."
        )

    def fetch_relations(self, model, item):
        pass
