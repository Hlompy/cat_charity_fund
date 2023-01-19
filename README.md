# QRKot - Pet Charity App

API for charity projects: create simple projects for fundraising and register incoming donations with automatic netting of funds.

`Python 3.9`
`FastAPI 0.78`
`SQLAlchemy 1.4`

## Start & Usage

### Installing

```
git clone https://github.com/Hlompy/cat_charity_fund.git
```

```
cd cat_charity_fund
```

```
python3 -m venv venv

source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

```
touch .env
```

`.env` file example:

```
APP_TITLE=Благотворительный фонд поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=somekey
```

### Launching

Command to start project on local server:

```
uvicorn app.main:app
```

Swagger interface will be available on your localhost adress for discovering API's opportunetes: localhost/docs


---

Author:
Kryukov George
