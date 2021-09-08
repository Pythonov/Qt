ADD_DRUG_EXAMPLE = {
    "target_class": "drug",
    "data": {
        "name": "NAME",
        "brand_name": "br_name",
        "category": "categ",
        "drug_class": "3",
        "ther_use": "3"
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

DEL_GENE_EXAMPLE = {
  "target_class": "genes",
  "data": {
    "list_to_delete": [{"id": "29"}, {"id": "21"}, {"id": "33"}]
  }
}

DEL_PERSON_EXAMPLE = {
  "target_class": "people",
  "data": {
    "list_to_delete": [{"id": "29"}, {"id": "21"}, {"id": "33"}]
  }
}

GET_ALL_GENES = {
    "target_class": "genes",
    "data": {}
}

GET_ALL_PEOPLE = {
    "target_class": "people",
    "data": {}
}

ADD_MANY_GENES_EXAMPLE = {
  "target_class": "genes",
  "data": {
    "list_to_create": [
        {
            "gene_code": "1",
            "comment": "comment text",
            "rs_code": "1",
            "poly_type": "1",
            "poly_status": "1",
            "interpretation": "interpretation text",
            "protein": "protein text"
        },
        {
            "gene_code": "2",
            "comment": "comment text",
            "rs_code": "2",
            "poly_type": "2",
            "poly_status": "2",
            "interpretation": "interpretation text",
            "protein": "protein text"
        },
        {
            "gene_code": "3",
            "comment": "comment text",
            "rs_code": "3",
            "poly_type": "3",
            "poly_status": "3",
            "interpretation": "interpretation text",
            "protein": "protein text"
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

TIE_GENE_EXAMPLE = {
  "target_class": "genes",
  "data": {
    "genes_id": {
      "id": "1"
    },
    "people_ids": [
      {"id": "4"}, {"id": "44"}, {"id": "9"}
    ]
  }
}

GET_SINGLE_GENE_EXAMPLE = {
  "target_class": "genes",
  "data": {
    "id": "3"
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
