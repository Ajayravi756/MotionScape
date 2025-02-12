# Generated by Django 5.0.4 on 2024-05-02 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customertbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam', models.CharField(max_length=100)),
                ('cnum', models.CharField(max_length=100)),
                ('eml', models.CharField(max_length=100)),
                ('password', models.CharField(default='website', max_length=100)),
                ('uname', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('is_pending_approval', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(upload_to='videos/')),
                ('gif_file', models.ImageField(blank=True, null=True, upload_to='gifs/')),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(upload_to='videos/')),
            ],
        ),
    ]
