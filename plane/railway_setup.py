import os
import time
import uuid

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from plane.db.models import Profile, User
from plane.license.models import Instance, InstanceAdmin


class Command(BaseCommand):
    help = "Railway: create the instance admin from PLANE_ADMIN_EMAIL / PLANE_ADMIN_PASSWORD"

    def handle(self, *args, **options):
        # The api program registers the instance right after migrations.
        for _ in range(150):
            instance = Instance.objects.first()
            if instance:
                break
            time.sleep(2)
        else:
            raise CommandError("Instance not registered after 5 minutes")

        if instance.is_setup_done or InstanceAdmin.objects.exists():
            self.stdout.write("Instance admin already set up")
            return

        email = os.environ.get("PLANE_ADMIN_EMAIL", "").strip().lower()
        password = os.environ.get("PLANE_ADMIN_PASSWORD", "")
        if not email or not password:
            self.stdout.write("PLANE_ADMIN_EMAIL or PLANE_ADMIN_PASSWORD is empty: create the admin at /god-mode/")
            return
        org = os.environ.get("PLANE_ORGANIZATION", "").strip() or "Plane"

        # Same steps as InstanceAdminSignUpEndpoint, under the same lock.
        with transaction.atomic():
            instance = Instance.objects.select_for_update().get(pk=instance.pk)
            if instance.is_setup_done or InstanceAdmin.objects.exists():
                return
            user = User.objects.filter(email=email).first()
            if user is None:
                user = User.objects.create(
                    first_name="Admin",
                    email=email,
                    username=uuid.uuid4().hex,
                    password=make_password(password),
                    is_password_autoset=False,
                    is_active=True,
                )
                Profile.objects.create(user=user, company_name=org)
            InstanceAdmin.objects.create(user=user, instance=instance)
            instance.is_setup_done = True
            instance.instance_name = org
            instance.save()

        # /api/instances/ is cached for 2 hours; drop the pre-setup answer.
        cache.clear()
        self.stdout.write(self.style.SUCCESS(f"Created instance admin {email}"))
