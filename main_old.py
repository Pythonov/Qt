from fastapi import FastAPI
import uvicorn
from src.models.models_old import *
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, ValidationError


app = FastAPI()


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['src.models.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Early-init

Tortoise.init_models(["src.models.models"], "models")
query_pydantic = pydantic_model_creator(BaseForQueries, name="BaseForQueries",
                                        exclude_readonly=True)


class SeparatorPyd(BaseModel):
    target_class: str
    data: dict


def parse_args(input_JSON: dict):
    try:
        input_data = SeparatorPyd.parse_obj(input_JSON)
        data = input_data.data
        target_class = input_data.target_class
    except ValidationError as e:
        target_class = "Wrong_data"
        data = e
    assert target_class in models_dict.keys()
    return target_class, data


@app.post(f'/post')  # Create object
async def post(cp: query_pydantic):
    target_class, data = parse_args(cp.dict())
    objIn_pydantic = pydantic_model_creator(models_dict[target_class], name=target_class, exclude_readonly=True)
    obj_created = objIn_pydantic.parse_obj(data)
    obj = await models_dict[target_class].create(**obj_created.dict(exclude_unset=True))
    response = await objIn_pydantic.from_tortoise_orm(obj)
    return {"status": "Ok", "data": response}
"""
Пример ввода для модели drug:
{
  "target_class": "drug",
  "data": {"generic_name": "Ибупрофен"}
}
"""


@app.post('/post_by_drug_name')  # Создает параметры по названию дженерика, а не по id
async def post(cp: query_pydantic):
    target_class, data = parse_args(cp.dict())
    drug_name = data['generic_name']
    obj_pydantic_drug = pydantic_model_creator(models_dict['drug'], name='drug')
    drug_id = await obj_pydantic_drug.from_queryset_single(models_dict['drug'].get(generic_name=drug_name))
    data['drug_id'] = drug_id.dict()['id']
    data.pop('generic_name')
    objIn_pydantic = pydantic_model_creator(models_dict[target_class], name=target_class, exclude_readonly=True)
    obj_created = objIn_pydantic.parse_obj(data)
    obj = await models_dict[target_class].create(**obj_created.dict(exclude_unset=True))
    response = await objIn_pydantic.from_tortoise_orm(obj)

    return {"status": "Ok", "data": response}
"""
Пример ввода:
{
  "target_class": "brand_name", -----------ЭТО КЛАСС, ЭКЗЕМПЛЯР КОТОРОГО ХОТИМ СОЗДАТЬ В БД
  "data": {
           "generic_name": "Ибупрофен",----ЭТО ДЖЕНЕРИК, К ОТОРОМУ ПРИКРЕПЛЯЕМ "name", ОН ДОЛЖЕН СУЩЕСТВОВАТЬ В ТАБЛИЦЕ НА МОМЕНТ ЗАПРОСА
           "name" : "Нурофен" -------------ЭТО "target_class", КОТОРЫЙ КРЕПИМ К "generic_name"
           }
}
"""


@app.post('/get')
async def get_single(cp: query_pydantic):  # Get 1 object
    target_class, data = parse_args(cp.dict())
    obj_pydantic = pydantic_model_creator(models_dict[target_class], name=target_class)
    response = await obj_pydantic.from_queryset_single(models_dict[target_class].get(**data))
    return {"status": "Ok", "data": response}
"""
Пример ввода для модели drug
{
  "target_class": "drug",
  "data": {"generic_name": "Ибупрофен"}
}
"""


@app.post('/get_all')
async def get_all(cp: query_pydantic):  # Get all objects
    target_class, data = parse_args(cp.dict())
    objIn_pydantic = pydantic_model_creator(models_dict[target_class], name=target_class)
    response = await objIn_pydantic.from_queryset(models_dict[target_class].all())
    return {"status": "Ok", "data": response}


@app.delete('/delete')
async def delete(cp: query_pydantic):  # Delete object
    target_class, data = parse_args(cp.dict())
    obj_to_delete = await models_dict[target_class].get(**data)
    await obj_to_delete.delete()
    return {f"Deleted {obj_to_delete.name}": obj_to_delete.name}


@app.put('/upd')
async def update(cp: query_pydantic):  # Update object
    target_class, data = parse_args(cp.dict())
    targ_params = data["targ_params"]
    search_param = data["search_param"]
    obj = models_dict[target_class].filter(**search_param)
    for parameter in targ_params.items():
        await obj.update(**{parameter[0]: parameter[1]})
    return {"status": "Ok", "data": "ДОПИСАТЬ"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
