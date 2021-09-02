from fastapi.middleware.cors import CORSMiddleware
from src.models.models_old import *
from src.examples import *
from fastapi import FastAPI
import uvicorn
from tortoise import Tortoise
from fastapi import Body
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel, validator, ValidationError

# Initial config
app = FastAPI(title='Qt App')

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['src.models.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

Tortoise.init_models(["src.models.models"], "models")
Tortoise.generate_schemas()


class Item(BaseModel):
    target_class: str
    data: dict

    @validator('target_class', allow_reuse=True)
    def target_class_validator(cls, v):
        if v not in list(adapter_dict['models'].keys()):
            raise ValidationError
        return v


@app.post("/create_single", name="Создать один объект")
async def create_single(item: Item = Body(
    ...,
    examples={
        "create_gene": {
            "description": "Create gene",
            "value": ADD_GENE_EXAMPLE
        },
        "create_person": {
            "description": "Create person",
            "value": ADD_PERSON_EXAMPLE
        }
    }
)):

    target_class = item.target_class
    data = item.data
    status = "Ok"
    error_data = {}
    if target_class == 'people':
        genes = data.get('genes')
        data.pop('genes')
    try:
        obj_creator = adapter_dict['objects_in'][target_class].parse_obj(data)
        response = await adapter_dict['models'][target_class].create(**obj_creator.dict())
        if target_class == 'people':
            data = {
                "people_id": {
                    "id": response.id
                },
                "genes_ids": genes
            }
            body = Item(target_class="people", data=data)
            await tie_single(body)

    except Exception as e:
        error_data[f'error in {data}'] = str(e)
        status = "not ok"
    return {"status": status, "data": response, "error_data": error_data}


@app.post('/create_many', name="Создать несколько объектов")
async def create_many(item: Item = Body(
    ...,
    examples={
        "create_many_genes": {
            "description": "Create genes",
            "value": ADD_MANY_GENES_EXAMPLE
        },
        "create_many_persons": {
            "description": "Create persons",
            "value": ADD_MANY_PERSONS_EXAMPLE
        }
    }
)):
    target_class = item.target_class
    data = item.data
    num_of_items = len(data['list_to_create'])
    status = 'stopped at the beginning'
    created_objects = []
    error_data = {}
    num_created_items = 0

    for obj in data['list_to_create']:
        try:
            obj_creator = adapter_dict['objects_in'][target_class].parse_obj(obj)
            created_obj = await adapter_dict['models'][target_class].create(**obj_creator.dict())
            created_objects.append(created_obj)
            num_created_items += 1
        except Exception as e:
            error_data[f"in: {obj}"] = f"error: {e}"
        status = 'not ok' if len(error_data) else 'ok'

    return {
        'status': status,
        'data': f'IDs that were created: {created_objects}',
        "created": f'{num_created_items}/{num_of_items}',
        "error_data": error_data,
    }





@app.post('/get_all', name="Получить все объекты")
async def get_all(item: Item = Body(
    ...,
    examples={
        "get_all_genes": {
            "description": "Get genes",
            "value": GET_ALL_GENES
        },
        "get_all_persons": {
            "description": "Get persons",
            "value": GET_ALL_PEOPLE
        }
    }
)):
    target_class = item.target_class
    response = await adapter_dict['objects_out'][target_class].from_queryset(adapter_dict['models'][target_class].all())
    num_of_items = len(response)
    return {"status": "Ok", "data": response, "num_of_items": num_of_items}


@app.post('/get_single', name="Получить один объект")
async def get_single(item: Item = Body(
    ...,
    examples={
        "get_single_gene": {
            "description": "Get single gene",
            "value": GET_SINGLE_GENE_EXAMPLE
        },
        "get_single_person": {
            "description": "Get single person",
            "value": GET_SINGLE_PERSON_EXAMPLE
        }
    }
)):
    target_class = item.target_class
    data = item.data
    try:
        response = (
            await adapter_dict['objects_out'][target_class].from_queryset_single(
                adapter_dict['models'][target_class].get(**data)))
    except Exception as e:
        return {"status": "not ok", "data": str(e)}
    return {"status": "Ok", "data": response}


@app.post('/delete', name="Удалить один или несколько объектов")
async def delete(item: Item = Body(
    ...,
    examples={
        "delete_genes": {
            "description": "Delete genes",
            "value": DEL_GENE_EXAMPLE
        },
        "delete_persons": {
            "description": "Delete persons",
            "value": DEL_PERSON_EXAMPLE
        }
    }
)):
    target_class = item.target_class
    data = item.data
    deleted_objects = []
    num_deleted_items = 0
    num_of_items = len(data['list_to_delete'])
    error_data = {}
    status = 'error at the beginning'

    for obj in data['list_to_delete']:
        try:
            obj_to_delete = await adapter_dict['models'][target_class].get(**obj)
            await obj_to_delete.delete()
            deleted_objects.append(obj['id'])
            num_deleted_items += 1
        except Exception as e:
            error_data[f"in ID: {obj['id']}"] = f"error: {e}"
        status = 'not ok' if len(error_data) else 'ok'

    return {
        'status': status,
        'data': f'IDs that were deleted: {deleted_objects}',
        "deleted": f'{num_deleted_items}/{num_of_items}',
        "error_data": error_data,
    }


@app.post('/get_all_depend', name="Получить все объекты со связями")
async def get_all_depend(item: Item = Body(
    ...,
    examples={
        "get_all_persons": {
            "description": "Get persons",
            "value": GET_ALL_PEOPLE
        }
    }
)):
    target_class = "people"
    response = await adapter_dict['models'][target_class].all().prefetch_related("genes")
    num_of_items = len(response)
    for i, x in enumerate(response):
        list_for_person = x.genes.related_objects
        response[i] = response[i].__dict__
        response[i].pop("_genes")
        response[i].pop("_partial")
        response[i]["genes"] = list_for_person

    return {"status": "Ok", "data": response, "num_of_items": num_of_items}


@app.post('/tie', name="Объединить один объект другими")
async def tie_single(item: Item = Body(
    ...,
    examples={
        "tie_gene_with_persons": {
            "description": "Delete genes",
            "value": TIE_GENE_EXAMPLE
        },
        "tie_person_with_genes": {
            "description": "Delete persons",
            "value": TIE_PERSON_EXAMPLE
        }
    }
)):
    """
    target_class - То, к чему присоединяем
    """
    target_class = item.target_class
    data = item.data
    errors_list = []
    status = 'error at the beginning'
    try:
        objects_to_tie = []
        target_obj = await adapter_dict['models'][target_class].get(**data[f'{target_class}_id'])
        combiners = 'people' if target_class == 'genes' else 'genes'
        for obj in data[f"{combiners}_ids"]:
            try:
                objects_to_tie.append(
                    await adapter_dict['models'][combiners].get(**obj)
                )
            except Exception as e:
                errors_list.append(f'{str(e)} in {obj}')

        if target_class == 'people':
            await target_obj.genes.add(*objects_to_tie)
        else:
            await target_obj.people.add(*objects_to_tie)
        status = 'not ok' if errors_list else 'ok'
        num_of_success = len(objects_to_tie)
        num_of_combiners = len(data[f'{combiners}_ids'])
        return {"status": status,
                "data": f"successfully combined {num_of_success}/{num_of_combiners}",
                "errors": errors_list
                }
    except Exception as e:
        return {"status": status, "data": f"{str(e)} while adding preprocessed objects"}


@app.post('/get_params_of_object', name="Получить связи объекта")
async def get_params_of_obj(item: Item = Body(
    ...,
    examples={
        "get_gene_with_persons": {
            "description": "gene's persons",
            "value": GET_GENE_WITH_PERSONS_EXAMPLE
        },
        "get_person_with_genes": {
            "description": "persons' genes",
            "value": GET_PERSON_WITH_GENES_EXAMPLE
        }
    }
)):
    target_class = item.target_class
    data = item.data
    error_data = []
    response = x = full_info = 'error at the beginning'
    combiners = 'genes' if target_class == 'people' else 'people'
    try:
        target_obj = await adapter_dict['models'][target_class].get(**data[f'{target_class}_id'])
        response = []
        await target_obj.fetch_related(combiners)
        if target_class == 'people':
            for x in target_obj.genes:
                response.append(x)
        else:
            for x in target_obj.people:
                response.append(x)
        full_info = {f'{combiners} ids for {target_class} with ID {target_obj.id}: {[x.id for x in response]}'}
    except Exception as e:
        error_data.append(f'{e} in {x}')

    return {
        "status": "ok",
        "data": response,
        "full_info": full_info,
        "error_data": error_data
    }

if __name__ == '__main__':
    uvicorn.run(app)
