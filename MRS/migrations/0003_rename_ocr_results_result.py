# Generated by Django 5.0.2 on 2024-03-02 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MRS', '0002_rename_image_ocr_results'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OCR_Results',
            new_name='Result',
        ),
    ]
