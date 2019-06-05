# Generated by Django 2.0 on 2019-05-30 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20190530_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='root_comment', to='comment.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_comment', to='comment.Comment'),
        ),
    ]