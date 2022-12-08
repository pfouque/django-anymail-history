# Generated by Django 3.2.16 on 2022-12-08 05:16

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("anymail_history", "0002_initial"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="messageevent",
            name="anymail_his_created_01395c_idx",
        ),
        migrations.RemoveIndex(
            model_name="messageevent",
            name="anymail_his_event_n_e3a465_idx",
        ),
        migrations.AddIndex(
            model_name="messageevent",
            index=models.Index(
                fields=["created_on"], name="anymail_his_created_04c5bf_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="messageevent",
            index=models.Index(
                fields=["event_name"], name="anymail_his_event_n_63f45f_idx"
            ),
        ),
    ]
