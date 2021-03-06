# Generated by Django 3.0.6 on 2020-05-22 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='Sliders')),
                ('rank', models.IntegerField()),
                ('status', models.CharField(choices=[('active', 'active'), (' ', 'default')], max_length=20)),
                ('description', models.TextField()),
            ],
        ),
    ]
