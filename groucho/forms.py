import random
import logging
from django import forms
from django.db import transaction
from groucho.models import AttemptUser, AttemptSource, Configuration

logger = logging.getLogger(__name__)


class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=100)

    def __init__(self, *args, source_ip=None, **kwargs):
        self.source_ip = source_ip
        self.configuration = Configuration.objects.all()[0]
        super(LoginForm, self).__init__(*args, **kwargs)

        
    def get_error_message(self, user):
        if not user or not user.exists:
            # This should never happen without a user unless something has gone completely wrong.
            # If that's the case then let's always say the account doesn't exist so we can
            # avoid saying a user exists when there's no record of what we said.
            if not user:
                logger.error('Trying to get LoginForm error message without a user.')
            return self.configuration.invalid_user_message
        
        return self.configuration.invalid_password_message
        
        
    @transaction.atomic
    def get_user(self, username, source_ip):
        try:
            user = None
        
            try:
                user = AttemptUser.objects.get(username=username)
            except AttemptUser.DoesNotExist:
                exists = False

                # Adding a simple alphanumeric check for now so that usernames
                # must look somewhat valid. If they are completely bogus then
                # the response should always say it doesn't exist.  Ultimately,
                # this could be a more sophisticated check where certain non-alphanumeric
                # characters are also okay, and that it matches a certain pattern.
                # The application could offer configuration for different types of
                # username patterns like only digits for certain situations.
                if username.isalpha():
                    exists = self.randomize_user_existence()

                user = AttemptUser.objects.create(username=username, exists=exists)
            except AttemptUser.MultipleObjectsReturned:
                logger.error('Multiple AttemptUser records found for user {}'.format(username))

            if user:
                AttemptSource.objects.create(ip=source_ip, credentials=user)
                return user

        except:
            logger.exception('The application failed while trying to create an AttemptUser object when saving a LoginForm instance.')


    def randomize_user_existence(self):
        return random.randint(1, 100) <= self.configuration.new_user_exists_rate


    def clean(self):
        cleaned_data = super().clean()
        # If the form has already failed validation for whatever reason then go ahead and let those
        # errors propagate before beginning the process of recording login attempts.
        if not self.errors:
            username = self.cleaned_data.get('username')
            raise forms.ValidationError(self.get_error_message(self.get_user(username, self.source_ip)))

    class Meta:
        model = AttemptUser
        fields = ['username', 'password']
