from django.contrib.auth.models import User
from myproject.janrain.models import JanrainUser 
from hashlib import sha1
from base64 import b64encode


class JanrainBackend(object):
    def authenticate(self, profile):
        # identifier is the unique identifier used to sign user into site
        identifier = profile['identifier']  # a URL to the user profile of the service

        # these fields MAY be in the profile, but are not guaranteed. it
        # depends on the provider and their implementation.
        providerName = profile.get('providerName')  # e.g. "Google" or "Facebook"
        displayName = profile.get('displayName')    # for google, this is the username
        givenName, familyName = self.get_name_from_profile(profile)
        email = self.get_email(profile)

        try:
            janrain_user = JanrainUser.objects.get(identifier=identifier, provider=providerName)
            return janrain_user.django_user
        except JanrainUser.DoesNotExist:
            # create new JanrainUser record and associate with a django User object,
            # creating one if one does not exist
            janrain_user = JanrainUser(
                                identifier=identifier,
                                provider=providerName,
                                display_name=displayName
                            )

            # try to associate with an existing user by first and last name and email
            try:
                u = User.objects.get(
                    first_name__iexact=givenName, 
                    last_name__iexact=familyName, 
                    email__iexact=email)
            except User.DoesNotExist, User.MultipleObjectsReturned:
                u = User()
                # if provider is google make the username the google username
                if providerName == 'Google':
                    u.username = displayName
                elif providerName == 'Facebook':
                    # TODO: parse the url profile field and extract the username
                    u.username = b64encode(sha1(identifier).digest())
                else:
                    # django.contrib.auth.models.User.username is required and 
                    # has a max_length of 30 so to ensure that we don't go over 
                    # 30 characters we base64 encode the sha1 of the identifier 
                    # returned from janrain 
                    u.username = b64encode(sha1(identifier).digest())
                u.first_name = givenName
                u.last_name = familyName
                u.is_superuser = False
                u.is_active = True
                u.set_unusable_password()
                u.is_staff = False
                if email:
                    u.email = email
                u.save()
    
            # associate django user, and save
            janrain_user.django_user = u
            janrain_user.save()

            return janrain_user.django_user

    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except User.DoesNotExist:
            return None

    def get_name_from_profile(self, p):
        nt = p.get('name')
        if type(nt) == dict:
            fname = nt.get('givenName')
            lname = nt.get('familyName')
            if fname and lname:
                return (fname, lname)
        dn = p.get('displayName')
        if len(dn) > 1 and dn.find(' ') != -1:
            (fname, lname) = dn.split(' ', 1)
            return (fname, lname)
        elif dn == None:
            return ('', '')
        else:
            return (dn, '')

    def get_email(self, p):
        return p.get('verifiedEmail') or p.get('email') or ''

