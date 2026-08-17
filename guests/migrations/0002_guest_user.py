from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='user',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='guest_profile',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
