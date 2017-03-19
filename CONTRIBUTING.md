# Installation

1. Clone repository.
2. Start `git-flow`
2. Make virtual env and install requirements.
3. Create docker databases.
4. Create tables with data & superuser.

```bash
git clone git@github.com:lecovi/teachers-rest.git
cd teachers-rest
git checkout master   # Creating local master branch
git checkout develop  # Going back to develop branch
git flow init -d
mkvirtualenv -p $(which pypy3) trest
add2virtualenv .      # Adds  project directory to PYTHONPATH in virtualenv.
pip install -r requirements/development.txt
docker run --name trest-db -e POSTGRES_PASSWORD=lecovi.trest -e POSTGRES_USER=lecovi -e POSTGRES_DB=trest -p 5432:5432 -d postgres
cp .env.dist .env     # Make sure to change your variables!
```

# Documentation

Create HTML documentation:

1. Switch to `docs` directory
2. Use `make html` command to create html files.
3. Open `index.html`.

```bash
cd docs
make html
xdg-open _build/html/index.html
```

# Running application

1. Run Falcon application using `gunicorn`.

```bash
gunicorn --bind 0.0.0.0:8000 --log-level debug --reload wsgi
```

# Development

I use [git-flow](http://nvie.com/posts/a-successful-git-branching-model/) 
as my development model. You always must create a new feature from 
`develop` branch. You are responsible to merge your feature into 
`develop`. 
 
1. Make sure your Docker DB is running using command line or [Portainer](http://portainer.io/).
2. Create new feature with `git-flow`.
 
```bash
docker start domi-db
git flow feature start awesome_new_feature
```

## Migrations

1. Inherit your model from `database.AppModel`.
2. Run alembic migration with `autogenerate` flag.

```bash
alembic revision --autogenerate -m "Added Test3 table with extra column"
```

3. Apply migration into DB.

```bash
alembic upgrade head
```

> **NOTE**: inside alembic folder there is an `env.py` file with config
> options. In the Installation steps we'd used `add2virtualenv` command to
> add the project folder into the `PYTHONPATH`, that's because we need
> to import the model metadata from the main module.
> Also we need database configuration from the database module, so alembic
> knows how to connect to apply the changes.