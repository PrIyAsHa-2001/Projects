# Generated by Django 2.2.6 on 2020-02-17 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0004_auto_20200215_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='owner_detail',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Room.Status'),
        ),
    ]
