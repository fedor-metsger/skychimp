# Generated by Django 4.2.2 on 2023-07-20 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailing", "0006_rename_timewindow_interval"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="tasks",
            field=models.ManyToManyField(
                related_name="clients", to="mailing.task", verbose_name="рассылки"
            ),
        ),
        migrations.AlterField(
            model_name="log",
            name="status",
            field=models.CharField(
                choices=[("success", "удачно"), ("unsuccess", "неудачно")],
                max_length=9,
                verbose_name="статус",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("created", "создана"),
                    ("running", "запущена"),
                    ("finished", "завершена"),
                ],
                default="created",
                max_length=8,
                verbose_name="статус",
            ),
        ),
    ]
