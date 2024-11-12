from django.db import migrations, models
import hashlib


def forwards_func(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    CustomTbl = apps.get_model('actionapp', 'customertbl')

    for customer in CustomTbl.objects.all():
        # Hash password securely before creating a User object
        hashed_password = hashlib.sha256(customer.password.encode('utf-8')).hexdigest()
        user = User.objects.create_user(username=customer.uname, password=hashed_password)

        # Optional: Map additional fields from customertbl to User fields
        # user.email = customer.email  # Example

class Migration(migrations.Migration):

    dependencies = [
        ('actionapp', '0001_initial'),  # Replace with your app's initial migration
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
