# Generated by Django 2.0 on 2017-12-11 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sendgrid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('register', 'Register'), ('newsletter', 'Newsletter'), ('purchase', 'Purchase')], max_length=15, unique=True)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('template_id', models.CharField(max_length=255)),
            ],
        ),
    ]
