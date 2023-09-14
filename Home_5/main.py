import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static', html=True), name='static')


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str


class User(UserIn):
    id: int


users = []
for i in range(10):
    users.append(User(
        id=i + 1,
        name=f'user_{i + 1}',
        email=f'user{i + 1}@mail.ru',
        password=f'{str(i) * 3}'
    ))


@app.get('/users/', response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/add_user/', response_class=HTMLResponse)
async def add_user(request: Request):
    return templates.TemplateResponse('add_user.html', {'request': request})


@app.post('/add_user/', response_model=dict)
async def add_user(username: str = Form(), email: str = Form(), password: str = Form()):
    await create_user(UserIn(name=username, email=email, password=password))
    return {'message': f'User {username} has added'}


@app.post('/users/', response_model=list[User])
async def create_user(new_user: UserIn):
    users.append(
        User(
            id=len(users) + 1,
            name=new_user.name,
            email=new_user.email,
            password=new_user.password
        ))
    return users


@app.put('/users/', response_model=UserOut)
async def update_user(user_id: int, update_user: UserIn):
    for user in users:
        if user.id == user_id:
            user = users[user_id - 1]
            user.name = update_user.name
            user.email = update_user.email
            user.password = update_user.password
            res_user = UserOut(id=user.id, name=user.name, email=user.email)
            return res_user
    raise HTTPException(status_code=404, detail='This user didnt found')


@app.delete('/users/', response_model=dict)
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {'message': 'User has deleted'}
    raise HTTPException(status_code=404, detail='User didnt found')


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level='debug',
        reload=True
    )
