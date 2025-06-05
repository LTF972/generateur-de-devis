from django.db import migrations, models
import django.db.models.deletion

def set_default_creator(apps, schema_editor):
    Client = apps.get_model('clients', 'Client')
    User = apps.get_model('auth', 'User')
    # Récupérer le premier utilisateur superuser comme créateur par défaut
    default_user = User.objects.filter(is_superuser=True).first()
    if default_user:
        Client.objects.filter(cree_par__isnull=True).update(cree_par=default_user)

class Migration(migrations.Migration):
    dependencies = [
        ('clients', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='cree_par',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='auth.user',
                verbose_name='Créé par'
            ),
        ),
        migrations.RunPython(set_default_creator),
    ] 