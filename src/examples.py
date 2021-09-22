ADD_DRUG_EXAMPLE = {
  "target_class": "drug",
  "data": {
    "name": "NAME2889",
    "category_id": "1"
  }
}

ADD_DRUG_CLASS_EXAMPLE = {
    "target_class": "drugClass",
    "data": {
        "name": "NAME"
    }
}

ADD_THER_USE_EXAMPLE = {
    "target_class": "therUse",
    "data": {
        "name": "NAME"
    }
}

ADD_BRAND_NAME_EXAMPLE = {
    "target_class": "brandName",
    "data": {
        "name": "NAME"
    }
}

ADD_CATEGORY_EXAMPLE = {
    "target_class": "category",
    "data": {
        "name": "CATEGORY"
    }
}

CREATE_SINGLE_GREAT_EXAMPLE = {
        "create_drug": {
            "description": "Create drug",
            "value": ADD_DRUG_EXAMPLE
        },
        "create_drug_class": {
            "description": "Create drug class",
            "value": ADD_DRUG_CLASS_EXAMPLE
        },
        "create_ther_use": {
            "description": "Create ther_use",
            "value": ADD_THER_USE_EXAMPLE
        },
        "create_brand_name": {
            "description": "Create brand_name",
            "value": ADD_BRAND_NAME_EXAMPLE
        },
        "create_category": {
            "description": "Create category",
            "value": ADD_CATEGORY_EXAMPLE
        }
}


GET_GENE_EXAMPLE = {
    "target_class": "genes",
    "data": {}
}

DELETE_DRUG_EXAMPLE = {
  "target_class": "drug",
  "data": {
    "list_to_delete": [{"id": "29"}, {"id": "21"}, {"id": "33"}]
  }
}

DELETE_DRUG_CLASS_EXAMPLE = {
    "target_class": "drugClass",
    "data": {
        "list_to_delete": [{"id": "29"}, {"id": "21"}, {"id": "33"}]
    }
}

DELETE_THER_USE_EXAMPLE = {
    "target_class": "therUse",
    "data": {
        "list_to_delete": [{"id": "29"}, {"id": "21"}, {"id": "33"}]
    }
}

DELETE_BRAND_NAME_EXAMPLE = {
    "target_class": "brandName",
    "data": {
        "list_to_delete": [{"id": "29"}, {"id": "21"}, {"id": "33"}]
    }
}

DELETE_CATEGORY_EXAMPLE = {
    "target_class": "category",
    "data": {
        "list_to_delete": [{"id": "29"}, {"id": "21"}, {"id": "33"}]
    }
}


DELETE_GREAT_EXAMPLE = {
        "delete_drug": {
            "description": "Delete drug",
            "value": DELETE_DRUG_EXAMPLE
        },
        "delete_drug_class": {
            "description": "Delete drug class",
            "value": DELETE_DRUG_CLASS_EXAMPLE
        },
        "delete_ther_use": {
            "description": "Delete ther_use",
            "value": DELETE_THER_USE_EXAMPLE
        },
        "delete_brand_name": {
            "description": "Delete brand_name",
            "value": DELETE_BRAND_NAME_EXAMPLE
        },
        "delete_category": {
            "description": "Delete category",
            "value": DELETE_CATEGORY_EXAMPLE
        }
}

GET_ALL_DRUGS = {
  "target_class": "drug",
  "data": {}
}

GET_ALL_CATEG = {
  "target_class": "category",
  "data": {}
}

ADD_MANY_BR_NAMES_EXAMPLE = {
  "target_class": "brandName",
  "data": {
    "list_to_create": [
      {
    "name": "NAME5"
  },
      {
    "name": "NAME6"
  },
      {
    "name": "NAME3"
  }
    ]
  }
}

ADD_MANY_PERSONS_EXAMPLE = {
  "target_class": "people",
  "data": {
    "list_to_create": [
        {
            "lab_number": "33",
            "name": "person's name",
            "sex": "W",
            "date_of_birth": "date",
            "material_type": "type",
            "date_of_analysis": "date",
            "reason_of_analysis": "reason",
            "comment": "comment text"
        },
        {
            "lab_number": "34",
            "name": "person's name",
            "sex": "W",
            "date_of_birth": "date",
            "material_type": "type",
            "date_of_analysis": "date",
            "reason_of_analysis": "reason",
            "comment": "comment text"
        },
        {
            "lab_number": "35",
            "name": "person's name",
            "sex": "W",
            "date_of_birth": "date",
            "material_type": "type",
            "date_of_analysis": "date",
            "reason_of_analysis": "reason",
            "comment": "comment text"
        }
    ]
  }
}

ADD_PERSON_EXAMPLE = {
    "target_class": "people",
    "data": {
        "lab_number": "3",
        "name": "person's name",
        "sex": "W",
        "date_of_birth": "date",
        "material_type": "type",
        "date_of_analysis": "date",
        "reason_of_analysis": "reason",
        "comment": "comment text",
        "genes": []
    }
}

TIE_PERSON_EXAMPLE = {
  "target_class": "people",
  "data": {
    "people_id": {
      "id": "1"
    },
    "genes_ids": [
      {"id": "4"}, {"id": "44"}, {"id": "9"}
    ]
  }
}

TIE_DRUG_EXAMPLE = {
  "target_class": "drug",
  "data": {
    "drug_id": {
      "id": "1"
    },
    "ids": {
        "drug_class": [{"id": "1"}],
        "brand_name": [{"id": "1"}],
        "therapeutic_use": [{"id": "1"}]
    }
  }
}


GET_SINGLE_CATEG_EXAMPLE = {
  "target_class": "category",
  "data": {
    "id": "1"
  }
}

GET_SINGLE_PERSON_EXAMPLE = {
  "target_class": "people",
  "data": {
    "id": "3"
  }
}

GET_PERSON_WITH_GENES_EXAMPLE = {
  "target_class": "people",
  "data": {
    "people_id": {
      "id": "1"
    }
  }
}

GET_GENE_WITH_PERSONS_EXAMPLE = {
  "target_class": "genes",
  "data": {
    "genes_id": {
      "id": "4"
    }
  }
}
