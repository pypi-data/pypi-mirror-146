# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['adlfs>=2022.2.0,<2023.0.0',
 'dacite>=1.6.0,<2.0.0',
 'docker>=5.0.3,<6.0.0',
 'networkx>=2.5.1,<3.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pymgclient==1.2.0']

setup_kwargs = {
    'name': 'gqlalchemy',
    'version': '1.2.0',
    'description': 'GQLAlchemy is library developed with purpose of assisting writing and running queries on Memgraph.',
    'long_description': '# GQLAlchemy\n\n\n<p>\n    <a href="https://github.com/memgraph/gqlalchemy/actions"><img src="https://github.com/memgraph/gqlalchemy/workflows/Build%20and%20Test/badge.svg" /></a>\n    <a href="https://github.com/memgraph/gqlalchemy/blob/main/LICENSE"><img src="https://img.shields.io/github/license/memgraph/gqlalchemy" /></a>\n    <a href="https://pypi.org/project/gqlalchemy"><img src="https://img.shields.io/pypi/v/gqlalchemy" /></a>\n    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n    <a href="https://memgraph.com/docs/gqlalchemy" alt="Documentation"><img src="https://img.shields.io/badge/documentation-GQLAlchemy-orange" /></a>\n    <a href="https://github.com/memgraph/gqlalchemy/stargazers" alt="Stargazers"><img src="https://img.shields.io/github/stars/memgraph/gqlalchemy?style=social" /></a>\n</p>\n\n**GQLAlchemy** is a fully open-source Python library and **Object Graph Mapper** (OGM) - a link between graph database objects and Python objects.\n\nAn Object Graph Mapper or OGM provides a developer-friendly workflow that allows for writing object-oriented notation to communicate with graph databases. Instead of writing Cypher queries, you will be able to write object-oriented code, which the OGM will automatically translate into Cypher queries.\n\nGQLAlchemy is built on top of Memgraph\'s low-level Python client `pymgclient`\n([PyPI](https://pypi.org/project/pymgclient/) /\n[Documentation](https://memgraph.github.io/pymgclient/) /\n[GitHub](https://github.com/memgraph/pymgclient)).\n\n## Installation\n\nBefore you install `gqlalchemy`, make sure that you have `cmake` installed by running:\n```\ncmake --version\n```\nYou can install `cmake` by following the [official instructions](https://cgold.readthedocs.io/en/latest/first-step/installation.html#).\n\nTo install `gqlalchemy`, simply run the following command:\n```\npip install gqlalchemy\n```\n\n## Build & Test\n\nThe project uses [Poetry](https://python-poetry.org/) to build the GQLAlchemy Python library. To build and run tests, execute the following command:\n`poetry install`\n\nBefore starting the tests, make sure you have an active Memgraph instance running. Execute the following command:\n`poetry run pytest .`\n\n## GQLAlchemy example\n\nWhen working with the `gqlalchemy`, a Python developer can connect to the database and execute a `MATCH` Cypher query using the following syntax:\n\n```python\nfrom gqlalchemy import Memgraph\n\nmemgraph = Memgraph("127.0.0.1", 7687)\nmemgraph.execute("CREATE (:Node)-[:Connection]->(:Node)")\nresults = memgraph.execute_and_fetch("""\n    MATCH (from:Node)-[:Connection]->(to:Node)\n    RETURN from, to;\n""")\n\nfor result in results:\n    print(result[\'from\'])\n    print(result[\'to\'])\n```\n\n## Query builder example\n\nAs we can see, the example above can be error-prone, because we do not have abstractions for creating a database connection and `MATCH` query.\n\nNow, rewrite the exact same query by using the functionality of GQLAlchemy\'s query builder:\n\n```python\nfrom gqlalchemy import match, Memgraph\n\nmemgraph = Memgraph()\n\nresults = (\n    match()\n    .node("Node", variable="from")\n    .to("Connection")\n    .node("Node", variable="to")\n    .return_()\n    .execute()\n)\n\nfor result in results:\n    print(result["from"])\n    print(result["to"])\n```\n\nAn example using the `Node` and `Relationship` classes:\n\n```python\nfrom gqlalchemy import Memgraph, Node, Relationship, match, Field\n\nmemgraph = Memgraph("127.0.0.1", 7687)\n\n\nclass User(Node):\n    id: int = Field(index=True, exist=True, unique=True, db=memgraph)\n\n\nclass Follows(Relationship, type="FOLLOWS"):\n    pass\n\n\nu1 = User(id=1).save(memgraph)\nu2 = User(id=2).save(memgraph)\nr = Follows(_start_node_id=u1._id, _end_node_id=u2._id).save(memgraph)\n\nresult = list(\n    match(memgraph.new_connection())\n    .node(variable="a")\n    .to(variable="r")\n    .node(variable="b")\n    .where("a.id", "=", u1.id)\n    .or_where("b.id", "=", u2.id)\n    .return_()\n    .execute()\n)[0]\n\nprint(result["a"])\nprint(result["b"])\nprint(result["r"])\n```\n\n## Development (how to build)\n```\npoetry run flake8 .\npoetry run black .\npoetry run pytest . -k "not slow"\n```\n\n## Documentation\n\nThe GQLAlchemy documentation is available on [memgraph.com/docs/gqlalchemy](https://memgraph.com/docs/gqlalchemy/).\n\nThe documentation can be generated by executing:\n```\npip3 install python-markdown\npython-markdown\n```\n\n## License\n\nCopyright (c) 2016-2022 [Memgraph Ltd.](https://memgraph.com)\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use\nthis file except in compliance with the License. You may obtain a copy of the\nLicense at\n\n     http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software distributed\nunder the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied. See the License for the\nspecific language governing permissions and limitations under the License.\n',
    'author': 'Jure Bajic',
    'author_email': 'jure.bajic@memgraph.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/memgraph/gqlalchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
