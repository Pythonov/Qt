from fastapi.middleware.cors import CORSMiddleware
from tortoise.query_utils import Q
from src.models.models import *
from src.examples import *
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi import Body
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
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


class Item(BaseModel):
    target_class: str
    data: dict

    @validator('target_class', allow_reuse=True)
    def target_class_validator(cls, v):
        if v not in list(adapter_dict.keys()):
            raise ValidationError
        return v


@app.delete("/delete_id={num_id}", name="Удалить объект")
async def delete_single(num_id):
    target_class = 'drug'
    status = 'not ok'
    error_data = {}
    try:
        obj_to_delete = await adapter_dict[target_class].get(id=num_id)
        res = await obj_to_delete.delete()
        status = 'ok'
    except Exception as e:
        res = 'ERROR 500'
        error_data['error'] = str(e)

    return {'status': status, 'data': res, 'error_data': error_data}


@app.post("/create_single", name="Создать один объект")
async def create_single(item: Item = Body(
    ...,
    examples=CREATE_SINGLE_GREAT_EXAMPLE
)):
    target_class = item.target_class
    data = item.data
    status = "Ok"
    error_data = {}
    try:
        obj = pydantic_model_creator(
            adapter_dict[target_class],
            name=target_class + 'In',
            exclude_readonly=True
        )
        obj_creator = obj.parse_obj(data)
        response = await adapter_dict[target_class].create(**obj_creator.dict())

    except Exception as e:
        error_data[f'error in {data}'] = str(e)
        response = {"error while creating object"}
        status = "not ok"
    return {"status": status, "data": response, "error_data": error_data}


@app.post('/create_many', name="Создать несколько объектов")
async def create_many(item: Item = Body(
    ...,
    examples={
        "create_many_br_names": {
            "description": "Create br_names",
            "value": ADD_MANY_BR_NAMES_EXAMPLE
        },
        "create_many_categories": {
            "description": "Create categories",
            "value": ADD_MANY_CATEGORIES_EXAMPLE
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
            obj_pyd = pydantic_model_creator(
                adapter_dict[target_class],
                name=target_class + 'In',
                exclude_readonly=True
            )
            obj_creator = obj_pyd.parse_obj(obj)
            created_obj = await adapter_dict[target_class].create(**obj_creator.dict())
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
        "get_all_drugs": {
            "description": "Get drugs",
            "value": GET_ALL_DRUGS
        },
        "get_all_categories": {
            "description": "Get categories",
            "value": GET_ALL_CATEG
        }
    }
)):
    target_class = item.target_class
    obj_pyd = pydantic_model_creator(
            adapter_dict[target_class],
            name=target_class,
        )
    response = await obj_pyd.from_queryset(adapter_dict[target_class].filter(Q()))
    num_of_items = len(response)
    return {"status": "Ok", "data": response, "num_of_items": num_of_items}


@app.post('/get_single', name="Получить один объект")
async def get_single(item: Item = Body(
    ...,
    examples={
        "get_single_category": {
            "description": "Get single category",
            "value": GET_SINGLE_CATEG_EXAMPLE
        }
    }
)):
    target_class = item.target_class
    data = item.data
    try:
        obj_pyd = pydantic_model_creator(
            adapter_dict[target_class],
            name=target_class,
        )
        response = (
            await obj_pyd.from_queryset_single(
                adapter_dict[target_class].get(**data)))
    except Exception as e:
        return {"status": "not ok", "data": str(e)}
    return {"status": "Ok", "data": response}


@app.post('/delete', name="Удалить один или несколько объектов")
async def delete(item: Item = Body(
    ...,
    examples=DELETE_GREAT_EXAMPLE
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
            obj_to_delete = await adapter_dict[target_class].get(**obj)
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


@app.post('/tie', name="Объединить один объект другими")
async def tie_single(item: Item = Body(
    ...,
    examples={
        "tie_drug_with_others": {
            "description": "Tie Drugs",
            "value": TIE_DRUG_EXAMPLE
        }
    }
)):
    """
    target_class - То, к чему присоединяем
    """
    target_class = item.target_class
    data = item.data
    errors_list = []
    counter_succ = num_of_objects = 0
    status = 'error at the beginning'
    objects_to_tie = []
    params = data[f'{target_class}_id']
    alias_dict = {
        'link': 'link',
        'drugClass': 'drug_class',
        "drug": 'drug',
        "therUse": 'therapeutic_use',
        "brandName": 'brand_name',
        "category": 'category',
    }

    async def create_if_not_exist(target, parameters):
        obj_pyd = pydantic_model_creator(
            adapter_dict[target],
            name=target + 'In',
            exclude_readonly=True
        )
        obj_orm = obj_pyd.parse_obj(parameters)
        await adapter_dict[target].create(**obj_orm.dict())
        output_obj = await adapter_dict[target].get(**parameters)
        return output_obj

    """
    Получение/создание дейст. в-ва
    """
    try:
        target_obj = await adapter_dict[target_class].get(Q(**params))
    except:
        target_obj = await create_if_not_exist(target_class, params)

    parameters = data.copy()
    parameters.pop('drug_id')

    try:
        for k, v in parameters.items():
            for obj in v:
                num_of_objects += 1
                try:
                    await adapter_dict[k].get(Q(**obj))
                except Exception:
                    await create_if_not_exist(k, obj)

                try:
                    objects_to_tie.append(
                        await adapter_dict[k].get(Q(**obj))
                    )
                except Exception as e:
                    errors_list.append(f'{str(e)} in {obj}')

            counter_succ += len(objects_to_tie)
            f = getattr(target_obj, alias_dict[k])
            await f.add(*objects_to_tie)
            objects_to_tie = []

        status = 'not ok' if errors_list else 'ok'
        return {"status": status,
                "data": f"successfully combined {counter_succ}/{num_of_objects}",
                "errors": errors_list
                }
    except Exception as e:
        return {"status": status, "data": f"{str(e)} while adding preprocessed objects"}

if __name__ == '__main__':
    uvicorn.run(app)
