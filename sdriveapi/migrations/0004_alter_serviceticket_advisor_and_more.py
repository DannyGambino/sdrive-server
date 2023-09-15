# Generated by Django 4.2.5 on 2023-09-15 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sdriveapi', '0003_alter_advisor_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceticket',
            name='advisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tickets', to='sdriveapi.advisor'),
        ),
        migrations.AlterField(
            model_name='serviceticket',
            name='technician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_tickets', to='sdriveapi.technician'),
        ),
    ]
