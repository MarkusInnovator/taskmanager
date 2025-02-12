from fastapi import APIRouter, HTTPException ,status
from api.models.todo import Todo
from api.schemas.todo import GetTodo,PutTodo,PostTodo

todo_router= APIRouter(prefix="/API",tags=["todo"])


@todo_router.get("/")
async def all_todos():
    data = Todo.all()
    return await GetTodo.from_queryset(data)

@todo_router.post("/")
async def post_todos(body:PostTodo):
    row = await Todo.create(**body.dict(exclude_unset=True))
    return await GetTodo.from_tortoise_orm(row)

@todo_router.put("/{key:int}")
async def update_todos(key: int , body:PutTodo):
    data = body.dict(exclude_unset=True)
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise  HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, 
    detail="Item not found"
    )
    await Todo.filter(id=key).update(**data)
    return GetTodo.from_queryset_single(Todo.get(id=key))

@todo_router.delete("/{key:int}")
async def delete_todos(key:int):
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise  HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, 
    detail="Item not found"
    )
    await Todo.filter(id=key).delete()
    return "Todo successfully deleted"