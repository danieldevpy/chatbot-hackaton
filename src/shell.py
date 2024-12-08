import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from customuser.models import CustomUser

user = CustomUser.objects.first()

print(user.json())