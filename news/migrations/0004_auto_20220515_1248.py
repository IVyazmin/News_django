# Generated by Django 3.2 on 2022-05-15 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20220427_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='get_news', to='news.category'),
        ),
    ]
