# Generated by Django 5.0.7 on 2024-07-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("complicanceAI", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankaccount",
            name="bank_statement",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="<django.db.models.fields.CharField>_<django.db.models.fields.CharField>_bankStatement/",
            ),
        ),
    ]