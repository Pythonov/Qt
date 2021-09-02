"""

You have to register all new models
in models_dict in format
{'name_for_json': name of class}

"""

from tortoise import models, fields


class BaseForQueries(models.Model):
    target_class = fields.CharField(max_length=50, null=False)
    data = fields.JSONField()


class BasicClass(models.Model):
    name = fields.CharField(max_length=100, unique=True, null=True)
    drug = fields.ForeignKeyField("models.Drug")

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class Drug(models.Model):
    generic_name = fields.CharField(max_length=100, unique=True, null=False)


class BrandName(BasicClass):
    pass


class DrugClass(BasicClass):
    pass


class TherapeuticUse(BasicClass):
    pass


class Category(BasicClass):
    pass


models_dict = {
    "drug": Drug,
    "brand_name": BrandName,
    "drug_class": DrugClass,
    "ther_use": TherapeuticUse,
    "category": Category
}