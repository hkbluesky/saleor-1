# Generated by Django 3.0.6 on 2020-06-23 07:43

import django.db.models.deletion
from django.db import migrations, models


def migrate_products_publishable_data(apps, schema_editor):
    Channel = apps.get_model("channel", "Channel")
    Product = apps.get_model("product", "Product")
    ProductChannelListing = apps.get_model("product", "ProductChannelListing")

    channels_dict = {}

    for product in Product.objects.iterator():
        currency = product.currency
        channel = channels_dict.get(currency)
        if not channel:
            channel, _ = Channel.objects.get_or_create(
                currency_code=currency,
                defaults={
                    "name": f"Channel {currency}",
                    "slug": f"channel-{currency.lower()}",
                },
            )
            channels_dict[currency] = channel
        ProductChannelListing.objects.create(
            product=product,
            channel=channel,
            is_published=product.is_published,
            publication_date=product.publication_date,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("channel", "0001_initial"),
        ("product", "0120_auto_20200714_0539"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductChannelListing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("publication_date", models.DateField(blank=True, null=True)),
                ("is_published", models.BooleanField(default=False)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_listing",
                        to="channel.Channel",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channel_listing",
                        to="product.Product",
                    ),
                ),
            ],
            options={"ordering": ("pk",), "unique_together": {("product", "channel")}},
        ),
        migrations.RunPython(migrate_products_publishable_data),
        migrations.RemoveField(model_name="product", name="is_published",),
        migrations.RemoveField(model_name="product", name="publication_date",),
    ]