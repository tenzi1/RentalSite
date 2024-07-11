# Generated by Django 5.0.3 on 2024-07-10 07:47

import django.db.models.deletion
import rentals.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='RentalLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, verbose_name='Address of rental property')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('is_seen', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recieved_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rental_id', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.province')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(verbose_name='Description of Rental Property')),
                ('num_bedrooms', models.IntegerField(default=0)),
                ('num_bathrooms', models.IntegerField(default=0)),
                ('is_bathroom_shared', models.BooleanField(default=False, help_text='Denotes whether bathroom is personal or shared with other renter.')),
                ('has_attached_bathroom', models.BooleanField(default=False, help_text='Denotes whether bathroom is attached.')),
                ('is_kitchen_shared', models.BooleanField(default=False, help_text='Denotes wheter the kitchen space is shared among other renters or not.')),
                ('square_footage', models.DecimalField(blank=True, decimal_places=2, help_text='Overall dimension of property.', max_digits=10, null=True)),
                ('monthly_rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_for_rent', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('category', models.ForeignKey(default=rentals.models.get_default_category, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='rentals', to='rentals.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='users.userprofile')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rentals', to='rentals.rentallocation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.rental')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('rent_start_date', models.DateField()),
                ('rent_end_date', models.DateField()),
                ('status', models.CharField(choices=[('PENDING', 'pending'), ('CONFIRMED', 'confirmed'), ('CANCELLED', 'cancelled'), ('REJECTED', 'rejected')], default='PENDING', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.rental')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RentalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='upload/rental/')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rental_images', to='rentals.rental')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_no', models.PositiveSmallIntegerField()),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.district')),
            ],
        ),
        migrations.AddField(
            model_name='rentallocation',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rentals.ward'),
        ),
    ]
