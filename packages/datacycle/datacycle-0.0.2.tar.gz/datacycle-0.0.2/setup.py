# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datacycle', 'datacycle.providers']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=13.3.4,<14.0.0',
 'dataconf>=1.4.0,<2.0.0',
 'furl>=2.1.2,<3.0.0',
 'sqlparse>=0.4.1,<0.5.0',
 'tdqm>=0.0.1,<0.0.2',
 'typer>=0.4.1,<0.5.0']

extras_require = \
{':extra == "all" or extra == "mongo"': ['pymongo>=4.1.0,<5.0.0'],
 'all': ['SQLAlchemy>=1.4.13,<2.0.0',
         'pg8000>=1.19.4,<2.0.0',
         'gsutil>=5.9,<6.0'],
 'google': ['gsutil>=5.9,<6.0'],
 'postgres': ['SQLAlchemy>=1.4.13,<2.0.0', 'pg8000>=1.19.4,<2.0.0']}

entry_points = \
{'console_scripts': ['datacycle = datacycle.main:cli']}

setup_kwargs = {
    'name': 'datacycle',
    'version': '0.0.2',
    'description': 'General toolset to backup & restore with random/filtered/anonymized data (Mongo/Postgres/GCS).',
    'long_description': '# Datacycle\n\n## Getting started\n\n```\ncp .env.example .env\nvim .env\nsource .env\n\npoetry install --extras all\npoetry run datacycle\n```\n\n```\ndocker build -f Dockerfile -t datacycle .\ndocker run -it --rm --env-file .env datacycle\n```\n\n### Mac requirements\n\n```\nbrew install mongodb/brew/mongodb-database-tools\nbrew install libpq\nbrew link --force libpq\nnpm install elasticdump -g\n```\n\n### Linux requirements\n\n```\napt install -y mongo-tools\napt install -y postgresql-client\nnpm install elasticdump -g\n```\n\n## How to\n\n```\ndatacycle --help\ndatacycle doctor\n\ndatacycle mongo "mongodb://user:password@localhost:27017/test1?authSource=admin" "mongodb://user:password@localhost:27017/test2?authSource=admin" --transform "\n    transforms {\n        test1 {\n            before-transform {}\n        }\n    }\n"\n\ndatacycle mongo mongodb://user:password@localhost:27017/test1?authSource=admin gs://datacycle-test/test1/snapshot --transform ops.hocon\n\ndatacycle mongo mongodb://user:password@localhost:27017/test1?authSource=admin mongodb://user:password@localhost:27017/test2?authSource=admin\ndatacycle mongo mongodb://user:password@localhost:27017/test1?authSource=admin gs://datacycle-test/test1/snapshot\ndatacycle mongo mongodb://user:password@localhost:27017/test1?authSource=admin test1/snapshot\n\ndatacycle mongo gs://datacycle-test/test1/snapshot mongodb://user:password@localhost:27017/test2?authSource=admin\ndatacycle mongo gs://datacycle-test/test1/snapshot gs://datacycle-test/test2/snapshot\ndatacycle mongo gs://datacycle-test/test1/snapshot test2/snapshot\n\ndatacycle mongo test1/snapshot mongodb://user:password@localhost:27017/test2?authSource=admin\ndatacycle mongo test1/snapshot gs://datacycle-test/test2/snapshot\ndatacycle mongo test1/snapshot test2/snapshot\n```\n\n## Providers\n\n### Postgres\n\nhttps://www.postgresql.org/docs/9.1/backup.html\n\n- SQL dump\n- file system snapshot\n- continuous archiving\n\n```\npg_dump --clean "postgres://user:password@localhost:5432/test" | gzip > dump.gz\ngunzip -c dump.gz | psql "postgres://user:password@localhost:5432/test"\n```\n\n### Mongo\n\nhttps://docs.mongodb.com/manual/core/backups/\n\n- BSON dump\n- file system snapshot\n- CDC\n\n```\nmongodump --uri="mongodb://user:password@localhost:27017/test?authSource=admin" --out=dump --numParallelCollections=10 -v --gzip\nmongorestore --uri="mongodb://user:password@localhost:27017/test?authSource=admin" dump/test --numParallelCollections=10 -v --gzip\n```\n\n### Elasticsearch\n\nhttps://github.com/elasticsearch-dump/elasticsearch-dump\n\n- dump\n\n```\nelasticdump --input=https://localhost:9200 --output=$ --limit 2000 | gzip > dump.gz\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/smood/recycle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
