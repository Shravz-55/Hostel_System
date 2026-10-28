from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=20, unique=True)),
                ('room_type', models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Triple', 'Triple')], max_length=20)),
                ('floor', models.IntegerField()),
                ('total_beds', models.IntegerField(default=1)),
                ('available_beds', models.IntegerField(default=1)),
                ('rent', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('room_image', models.ImageField(blank=True, null=True, upload_to='rooms/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'rooms',
                'ordering': ['room_number'],
            },
        ),
    ]
