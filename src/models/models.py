"""

You have to register all new models
and created pydantic objects
in adapter_dict

"""
from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class BasicClass(models.Model):
    name = fields.CharField(max_length=100, unique=True, null=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class Drug(BasicClass):
    brand_name = fields.ForeignKeyField("models.BrandName", null=True)
    category = fields.ForeignKeyField("models.Category", null=True)
    drug_class: fields.ManyToManyRelation["DrugClass"] = fields.ManyToManyField(
        "models.DrugClass", related_name="drug class", through="drugs_class", null=True
    )
    therapeutic_use: fields.ManyToManyRelation["TherapeuticUse"] = fields.ManyToManyField(
        "models.TherapeuticUse", related_name="therapeutic usage", through="drugs_usage", null=True
    )


class DrugClass(BasicClass):
    drug: fields.ManyToManyRelation[Drug]


class TherapeuticUse(BasicClass):
    drug: fields.ManyToManyRelation[Drug]


class BrandName(BasicClass):
    pass


class Category(BasicClass):
    pass


obj_In_drugs = pydantic_model_creator(Drug, name='drugsIn', exclude_readonly=True)
obj_drugs = pydantic_model_creator(Drug, name='drugs')
obj_In_drug_class = pydantic_model_creator(DrugClass, name='DrugClassIn', exclude_readonly=True)
obj_drug_class = pydantic_model_creator(DrugClass, name='drugClass')
obj_In_ther_use = pydantic_model_creator(TherapeuticUse, name='therUseIn', exclude_readonly=True)
obj_ther_use = pydantic_model_creator(TherapeuticUse, name='therUse')
obj_In_brand_name = pydantic_model_creator(BrandName, name='brandnameIn', exclude_readonly=True)
obj_brand_name = pydantic_model_creator(BrandName, name='brandName')
obj_In_category = pydantic_model_creator(Category, name='categoryIn', exclude_readonly=True)
obj_category = pydantic_model_creator(Category, name='category')

adapter_dict = {
    "models": {
        "drug": Drug,
        "drugClass": DrugClass,
        "therUse": TherapeuticUse,
        "brandName": BrandName,
        "category": Category
    },
    "objects_in": {
        "drug": obj_In_drugs,
        "drugClass": obj_In_drug_class,
        "therUse": obj_In_ther_use,
        "brandName": obj_In_brand_name,
        "category": obj_In_category
    },
    "objects_out": {
        "drug": obj_drugs,
        "drugClass": obj_drug_class,
        "therUse": obj_ther_use,
        "brandName": obj_brand_name,
        "category": obj_category
    },
}
