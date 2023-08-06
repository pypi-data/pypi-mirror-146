# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prose', 'prose.migrations']

package_data = \
{'': ['*'], 'prose': ['static/prose/*', 'templates/prose/forms/widgets/*']}

install_requires = \
['bleach>=4.0', 'django>=3.0']

setup_kwargs = {
    'name': 'django-prose',
    'version': '1.0.0',
    'description': 'Wonderful rich text for Django',
    'long_description': '# Django Prose\n\n![PyPI - Downloads](https://img.shields.io/pypi/dw/django-prose?color=purple) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-prose)\n\nDjango Prose provides your Django applications with wonderful rich-text editing.\n\n## Requirements\n\n- Python 3.6.2 or later\n- Django 3.0 or later\n- Bleach 4.0 or later\n\n## Getting started\n\nTo get started with Django Prose, first make sure to install it. We use and suggest using Poetry, although Pipenv and pip will work seamlessly as well\n\n```console\npoetry add django-prose\n```\n\nThen, add `prose` in Django\'s installed apps (example: [`prose_example/prose_example/settings.py`](https://github.com/withlogicco/django-prose/blob/55fb9319e55d873afe43968817a2f5ea3f055d11/prose_example/prose_example/settings.py#L46)):\n\n```python\nINSTALLED_APPS = [\n    # Django stock apps (e.g. \'django.contrib.admin\')\n\n    \'prose\',\n\n    # your application\'s apps\n]\n```\n\nLast, run migrations so you can use Django Prose\'s Document model:\n\n```\npython manage.py migrate prose\n```\n\nNow, you are ready to go 🚀.\n\n## Usage\n\nThere are different ways to use Django prose according to your needs. We will examine all of them here.\n\n### Small rich-text information\n\nYou might want to add rich-text information in a model that is just a few characters (e.g. 140), like an excerpt from an article. In that case we suggest using the `RichTextField`. Example:\n\n```py\nfrom django.db import models\nfrom prose.fields import RichTextField\n\nclass Article(models.Model):\n    excerpt = RichTextField()\n```\n\nThen you can display the article excerpt in your HTML templates by marking it as [`safe`](https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#safe)\n\n```django\n<div class="article-excerpt">{{ article.excerpt | safe}}</div>\n```\n\n### Large rich-text information\n\nIn case you want to store large rich-text information, like the content of an article, which can span to quite a few thousand characters, we suggest you use the `AbstractDocument` model. This will save large rich-text information in a separate database table, which is better for performance. Example:\n\n```py\nfrom django.db import models\nfrom prose.fields import RichTextField\nfrom prose.models import AbstractDocument\n\nclass ArticleContent(AbstractDocument):\n    pass\n\nclass Article(models.Model):\n    excerpt = RichTextField()\n    body = models.OneToOneField(ArticleContent, on_delete=models.CASCADE)\n```\n\nSimilarly here you can display the article\'s body by marking it as `safe`\n\n```django\n<div class="article-body">{{ article.body.content | safe}}</div>\n```\n\n### Attachments\n\nDjango Prose can also handle uploading attachments with drag and drop. To set this up, first you need to:\n\n- [x] Set up the `MEDIA_ROOT` of your Django project (example in [`prose_example/prose_example/settings.py`](https://github.com/withlogicco/django-prose/blob/55fb9319e55d873afe43968817a2f5ea3f055d11/prose_example/prose_example/settings.py#L132)))\n- [x] Include the Django Prose URLs (example in [`prose_example/prose_example/urls.py`](https://github.com/withlogicco/django-prose/blob/9073d713f8d3febe5c50705976dbb31063270886/prose_example/prose_example/urls.py#L9-L10))\n- [x] (Optional) Set up a different Django storage to store your files (e.g. S3)\n\n## 🔒 A note on security\n\nAs you can see in the examples above, what Django Prose does is provide you with a user friendly editor ([Trix](https://trix-editor.org/)) for your rich text content and then store it as HTML in your database. Since you will mark this HTML as safe in order to use it in your templates, it needs to be **sanitised**, before it gets stored in the database.\n\nFor this reason Django Prose is using [Bleach](https://bleach.readthedocs.io/en/latest/) to only allow the following tags and attributes:\n\n- **Allowed tags**: `p`, `ul`, `ol`, `li`, `strong`, `em`, `div`, `span`, `a`, `blockquote`, `pre`, `figure`, `figcaption`, `br`, `code`, `h1`, `h2`, `h3`, `h4`, `h5`, `h6`, `picture`, `source`, `img`\n- **Allowed attributes**: `alt`, `class`, `id`, `src`, `srcset`, `href`, `media`\n\n## Screenshots\n\n### Django Prose Documents in Django Admin\n\n\n![Django Prose Document in Django Admin](./docs/django-admin-prose-document.png)\n\n## Development for Django Prose\n\nIf you plan to contribute code to Django Prose, this section is for you. All development tooling for Django Prose has been set up with Docker. To get started run these commands in the provided order:\n\n```console\ndocker compose run --rm migrate\ndocker compose run --rm createsuperuser\ndocker compose up\n```\n\n---\n\n<p align="center">\n  <i>🦄 Built with ❤️ by <a href="https://withlogic.co/">LOGIC</a>. 🦄</i>\n</p>\n',
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@withlogic.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/parisk/django-prose',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
