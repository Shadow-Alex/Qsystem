# Generated by Django 3.0 on 2019-12-12 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Qsystem', '0003_questioncomment_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestiondetail',
            name='inPaper',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Qsystem.UserPaperDetail'),
        ),
    ]