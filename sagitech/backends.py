from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find a user matching the provided email
            user = User.objects.get(Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # If multiple users have the same email, return the first one
            return User.objects.filter(email=username).order_by('id').first()