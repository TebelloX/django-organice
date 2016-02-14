"""
A label command (sub-command) for the Organice management command.
"""
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _


class InitdbCommandMixin(object):

    def initdb_command(self):
        """
        Initialize the Organice database and apps
        """
        if self.verbosity >= 1:
            self.stdout.write(_('Initialize database:'))
        call_command('migrate', verbosity=self.verbosity)

        if self.verbosity >= 1:
            self.stdout.write(_('Configure site #1 ...'))
        s, created = Site.objects.get_or_create(id=1)
        s.name, s.domain = 'Organice Demo', 'demo.organice.io'
        s.save()

        username, password, email = 'admin', 'admin', 'demo@organice.io'
        if self.verbosity >= 1:
            self.stdout.write(_('Create admin user ({}/{}) ...').format(username, password))
        try:
            call_command('createsuperuser', '--noinput', username=username, email=email, verbosity=self.verbosity)
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
        except IntegrityError:
            if self.verbosity >= 1:
                self.stdout.write(_("WARNING: Looks like a user '{}' already exists.".format(username)))