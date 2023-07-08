# Generated by Django 4.2.3 on 2023-07-07 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_operational', models.BooleanField(default=True)),
                ('is_maintenance', models.BooleanField(default=False)),
                ('direction', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_number', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elevators.elevator')),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elevators.floor')),
            ],
        ),
        migrations.AddField(
            model_name='elevator',
            name='current_floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elevators.floor'),
        ),
    ]