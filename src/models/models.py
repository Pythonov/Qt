"""

You have to register all new models
and created pydantic objects
in adapter_dict

"""
from tortoise import models, fields
from tortoise import Tortoise


class BasicClass(models.Model):
    name = fields.CharField(max_length=100, unique=True, null=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Drug(BasicClass):
    link: fields.ManyToManyRelation[
        "Link"
    ] = fields.ManyToManyField(
        "models.Link",
        related_name="link",
        through="drugs_links",
        null=True,
    )

    category: fields.ForeignKeyRelation["Category"] = fields.ForeignKeyField(
        "models.Category",
        null=True,
        related_name="category"
    )
    brand_name: fields.ManyToManyRelation[
        "BrandName"
    ] = fields.ManyToManyField(
        "models.BrandName",
        related_name="Brand name",
        through="drugs_brands",
        null=True,
    )
    drug_class: fields.ManyToManyRelation["DrugClass"] = fields.ManyToManyField(
        "models.DrugClass", related_name="drug class", through="drugs_class", null=True
    )
    therapeutic_use: fields.ManyToManyRelation[
        "TherapeuticUse"
    ] = fields.ManyToManyField(
        "models.TherapeuticUse",
        related_name="therapeutic usage",
        through="drugs_usage",
        null=True,
    )


class DrugClass(BasicClass):
    drug: fields.ManyToManyRelation[Drug]


class TherapeuticUse(BasicClass):
    drug: fields.ManyToManyRelation[Drug]


class BrandName(BasicClass):
    drug: fields.ManyToManyRelation[Drug]


class Category(BasicClass):
    pass


class Link(BasicClass):
    drug: fields.ManyToManyRelation[Drug]


Tortoise.init_models(["src.models.models"], "models")

adapter_dict = {
    "link": Link,
    "drug": Drug,
    "drugClass": DrugClass,
    "therUse": TherapeuticUse,
    "brandName": BrandName,
    "category": Category,
}
