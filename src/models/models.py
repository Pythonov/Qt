"""

You have to register all new models
and created pydantic objects
in adapter_dict

"""
from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Genes(models.Model):
    id = fields.IntField(pk=True, index=True)
    gene_code = fields.CharField(max_length=50, unique=False)
    rs_code = fields.CharField(max_length=25, unique=False)
    poly_type = fields.CharField(max_length=50, unique=False)
    poly_status = fields.CharField(max_length=50, unique=False)
    interpretation = fields.TextField()
    protein = fields.TextField()
    comment = fields.TextField()
    people: fields.ManyToManyRelation["People"] = fields.ManyToManyField(
        'models.People', related_name='genes', through='genes_people',
    )

    def __str__(self):
        return self.id

    class Meta:
        ordering = ["id"]
        unique_together = (("rs_code", "gene_code", "poly_type"),)


class People(models.Model):
    id = fields.IntField(pk=True)
    lab_number = fields.CharField(max_length=10, unique=True)
    name = fields.CharField(max_length=50, unique=False)
    sex = fields.CharField(max_length=10, unique=False)
    date_of_birth = fields.CharField(max_length=20, unique=False)
    material_type = fields.CharField(max_length=50, unique=False)
    date_of_analysis = fields.CharField(max_length=50, unique=False)
    reason_of_analysis = fields.TextField()
    comment = fields.TextField(null=True)
    genes: fields.ManyToManyRelation[Genes]

    class Meta:
        ordering = ["date_of_analysis"]

    def __str__(self):
        return f'{self.id}_{self.lab_number}'


obj_In_genes = pydantic_model_creator(Genes, name='genesIn', exclude_readonly=True)
obj_genes = pydantic_model_creator(Genes, name='genes')
obj_In_people = pydantic_model_creator(People, name='peopleIn', exclude_readonly=True)
obj_people = pydantic_model_creator(People, name='people')

adapter_dict = {
    "models": {
        "people": People,
        "genes": Genes,
    },
    "objects_in": {
        "people": obj_In_people,
        "genes": obj_In_genes,
    },
    "objects_out": {
        "people": obj_people,
        "genes": obj_genes,
    },
}
