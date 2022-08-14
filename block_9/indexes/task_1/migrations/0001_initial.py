# Generated by Django 3.2.13 on 2022-08-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inn', models.CharField(max_length=12, verbose_name='ИНН')),
                ('fname', models.CharField(max_length=300, verbose_name='Фамилия')),
                ('iname', models.CharField(max_length=300, verbose_name='Имя')),
                ('oname', models.CharField(max_length=300, null=True, verbose_name='Отчество')),
                ('country', models.CharField(max_length=3, verbose_name='Страна местонахождения на момент приема')),
                ('department_id', models.IntegerField(verbose_name='ID подразделения')),
                ('position_id', models.IntegerField(verbose_name='ID должности')),
                ('begin', models.DateField(verbose_name='Дата приема')),
                ('end', models.DateField(null=True, verbose_name='Дата увольнения')),
                ('additional_info', models.TextField(default='', verbose_name='Дополнительная информация')),
            ],
            options={
                'db_table': 'indexes_employees',
            },
        ),
    ]
