# Generated by Django 3.0 on 2019-12-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Qsystem', '0007_question_correct_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestiondetail',
            name='option',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=32),
        ),
    ]
