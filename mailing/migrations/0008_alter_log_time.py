# Generated by Django 4.2.2 on 2023-07-20 19:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailing", "0007_alter_client_tasks_alter_log_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="log",
            name="time",
            field=models.DateTimeField(auto_now_add=True, verbose_name="время"),
        ),
    ]