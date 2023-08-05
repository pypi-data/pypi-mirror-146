# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datapane',
 'datapane.client',
 'datapane.client.api',
 'datapane.client.api.report',
 'datapane.client.apps',
 'datapane.common',
 'datapane.resources',
 'datapane.resources.local_report',
 'datapane.resources.report_def',
 'datapane.resources.templates',
 'datapane.resources.templates.app',
 'datapane.resources.templates.hello',
 'datapane.resources.templates.report_py',
 'datapane.runner']

package_data = \
{'': ['*'], 'datapane.resources.templates': ['report_ipynb/*']}

install_requires = \
['Jinja2>=2.11.0,<3.1.0',
 'PyYAML>=6.0.0,<7.0.0',
 'altair>=4.0.0,<5.0.0',
 'boltons>=20.0.0,<22.0.0',
 'chardet>=3.0.4,<5.0.0',
 'click-spinner>=0.1.8,<0.2.0',
 'click>=7.1.0,<9.0.0',
 'colorlog>=4.1.0,<7.0.0',
 'dacite>=1.0.2,<2.0.0',
 'datacommons-pandas>=0.0.3,<0.0.4',
 'datacommons>=1.4.3,<2.0.0',
 'dominate>=2.4.0,<3.0.0',
 'furl>=2.0.0,<3.0.0',
 'glom>=20.5.0,<21.0.0',
 'importlib_resources>=3.0.0,<6.0.0',
 'jsonschema>=3.2.0,<5.0.0',
 'lxml>=4.0.0,<5.0.0',
 'micawber>=0.5.0',
 'munch>=2.3.0,<3.0.0',
 'nbconvert>=5.6.1,<7.0.0',
 'packaging>=20.0.0,<22.0.0',
 'pandas>=1.1.0,<2.0.0',
 'posthog>=1.4.0,<2.0.0',
 'pyarrow>=3.0.0,<7.0.0',
 'pydantic>=1.6.0,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.19.0,<3.0.0',
 'stringcase>=1.2.0,<2.0.0',
 'tabulate>=0.8.0,<0.9.0',
 'toolz>=0.11.0,<0.12.0',
 'validators>=0.18.0,<0.19.0',
 'vega-datasets>=0.9.0,<1.0.0']

extras_require = \
{'cloud': ['flit-core>=3.0.0,<3.1.0'],
 'plotting': ['matplotlib>=3.0.0,<4.0.0',
              'plotly>=4.0.0,<6.0.0',
              'bokeh>=2.2.0,<2.3.0',
              'folium>=0.12.0,<0.13.0']}

entry_points = \
{'console_scripts': ['datapane = datapane.client.__main__:main',
                     'dp-runner = datapane.runner.__main__:main']}

setup_kwargs = {
    'name': 'datapane',
    'version': '0.14.0',
    'description': 'Datapane client library and CLI tool',
    'long_description': '<p align="center">\n  <a href="https://datapane.com">\n    <img src="https://datapane.com/static/datapane-logo-dark.png" width="250px" alt="Datapane" />\n  </a>\n</p>\n<p align="center">\n    <a href="https://datapane.com">Datapane Teams</a> |\n    <a href="https://docs.datapane.com">Documentation</a> |\n    <a href="https://datapane.github.io/datapane/">API Docs</a> |\n    <a href="https://docs.datapane.com/changelog">Changelog</a> |\n    <a href="https://twitter.com/datapaneapp">Twitter</a> |\n    <a href="https://blog.datapane.com">Blog</a>\n    <br /><br />\n    <a href="https://pypi.org/project/datapane/">\n        <img src="https://img.shields.io/pypi/dm/datapane?label=pip%20downloads" alt="Pip Downloads" />\n    </a>\n    <a href="https://pypi.org/project/datapane/">\n        <img src="https://img.shields.io/pypi/v/datapane?color=blue" alt="Latest release" />\n    </a>\n    <a href="https://anaconda.org/conda-forge/datapane">\n        <img alt="Conda (channel only)" src="https://img.shields.io/conda/vn/conda-forge/datapane">\n    </a>\n</p>\n<h4>Share interactive plots and data in 3 lines of Python.</h4>\n\nDatapane is a Python library for building interactive reports for your end-users in seconds.\n\nImport our library into your existing script/notebook and build reports from pandas Dataframes, plots from Python viz libraries, Markdown, as well as data exploration and layout components.\n\nExport your reports as standalone HTML documents, or share and embed them via our free hosted platform.\n\n# Getting Started\n\n## Installing Datapane\n\nThe best way to install Datapane is through pip or conda.\n\n#### pip\n\n```\n$ pip3 install -U datapane\n$ datapane hello-world\n```\n\n#### conda\n\n```\n$ conda install -c conda-forge "datapane>=0.12.0"\n$ datapane hello-world\n```\n\nDatapane also works well in hosted Jupyter environments such as Colab or Binder, where you can install as follows:\n\n```\n!pip3 install --quiet datapane\n!datapane signup\n```\n\n## Explainer Video\n\nhttps://user-images.githubusercontent.com/16949044/134007757-0b91074a-2b32-40ba-b385-5623dff8c04e.mp4\n\n## Hello world\n\nLet\'s say you wanted to create a report with an interactive plot and table viewer:\n\n```python\nimport altair as alt\nfrom vega_datasets import data\nimport datapane as dp\n\nsource = data.cars()\n\nplot1 = alt.Chart(source).mark_circle(size=60).encode(\n  x=\'Horsepower\',\n  y=\'Miles_per_Gallon\',\n  color=\'Origin\',\n  tooltip=[\'Name\', \'Origin\', \'Horsepower\', \'Miles_per_Gallon\']\n).interactive()\n\ndp.Report(\n    dp.Text("## Hello world!"),\n    dp.Plot(plot1),\n    dp.DataTable(source)\n).save(path="Hello_world.html")\n```\n\nThis will package a standalone HTML document that looks as follows:\n\n<img width="1269" alt="Simple Datapane report example with text, plot and table" src="https://user-images.githubusercontent.com/16949044/134021084-39b3369b-3c42-478c-b1fb-79f2b5b4b4a2.png">\n\nYour users can scroll & zoom on the chart, filter and download the tabular data.\n\n## Advanced Layout Options\n\nDatapane is great for presenting complex data and provides many components for creating advanced interactive layouts. Let\'s you need to write a technical document:\n\n```python\nimport altair as alt\nfrom vega_datasets import data\nimport datapane as dp\n\nsource = data.cars()\nplot1 = alt.Chart(source).mark_circle(size=60).encode(\n    x=\'Horsepower\',\n    y=\'Miles_per_Gallon\',\n    color=\'Origin\',\n    tooltip=[\'Name\', \'Origin\', \'Horsepower\', \'Miles_per_Gallon\']\n).interactive()\n\ndp.Report(\n    dp.Page(title="Charts and analysis",\n            blocks=[\n                dp.Formula("x^2 + y^2 = z^2"),\n                dp.Group(\n                    dp.BigNumber(\n                        heading="Number of percentage points",\n                        value="84%",\n                        change="2%",\n                        is_upward_change=True\n                    ),\n                    dp.BigNumber(\n                        heading="Simple Statistic",\n                        value=100\n                    ), columns=2,\n                ),\n                dp.Select(blocks=[\n                    dp.Plot(plot1, label="Plot"),\n                    dp.HTML(\'\'\'<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\'\'\', label="Video")\n                ]),\n            ]),\n    dp.Page(title="Dataset", blocks=[\n            dp.DataTable(source)\n    ])\n).save(path="Complex_layout.html", open=True)\n```\n\nLayout blocks like `dp.Select`, `dp.Group` and `dp.Page` allow you to highlight key points without sacrificing detail, while content blocks like `dp.HTML` and `dp.Formula` (LaTeX) can enrich your report. The final result looks like this:\n\n<img width="1000" alt="Complex Datapane report example" src="https://user-images.githubusercontent.com/16949044/134022445-5d417993-808f-4de8-8e8c-f510bdf4a17e.png">\n\nCheck out the full list of blocks in our [documentation](https://docs.datapane.com/reports/blocks).\n\n# Sharing Reports\n\n## Sign up for a free account\n\nIn addition to saving documents locally, you can host, share and embed reports via [Datapane Studio](https://datapane.com/).\n\nTo get your free API key, run the following command in your terminal to sign up via email/OAuth:\n\n```\n$ datapane signup\n```\n\nIf you\'re using Jupyter, run `!datapane signup` instead.\n\nNext, in your Python notebook or script simply change the `save` function to `upload` on your report:\n\n```python\ndp.Report(\n ...\n#).save(path="hello_world.html")\n).upload(name="Hello world")\n```\n\nYour Studio account comes with the following:\n\n- **Unlimited public reports** - great for embedding into places like Medium, Reddit, or your own website (see [here](https://docs.datapane.com/reports/embedding-reports-in-social-platforms))\n- **5 private reports** - share these via email within your organization\n\n### Featured Examples\n\nHere a few samples of the top reports created by the Datapane community. To see more, check out our [gallery](https://datapane.com/gallery) section.\n\n- [Tutorial Report](https://datapane.com/u/leo/reports/tutorial-1/) by Datapane Team\n- [Coindesk analysis](https://datapane.com/u/greg/reports/initial-coindesk-article-data/) by Greg Allan\n- [COVID-19 Trends by Quarter](https://datapane.com/u/keith8/reports/covid-19-trends-by-quarter/) by Keith Johnson\n- [Ecommerce Report](https://datapane.com/u/leo/reports/e-commerce-report/) by Leo Anthias\n- [Example Academic Paper](https://datapane.com/u/kalru/reports/supplementary-material/) by Kalvyn Roux\n- [Exploration of Restaurants in Kyoto](https://datapane.com/u/ryancahildebrandt/reports/kyoto-in-stations-and-restaurants/) by Ryan Hildebrandt\n\n# Teams\n\n[Datapane Teams](https://datapane.com/teams/) is our plan for teams, which adds the following features on top of our open-source and Studio plans:\n\n- Private domain and organizational workspace\n- Multiple projects\n- Client-sharing functionality\n- Unlimited Datapane Apps\n- Custom App packages and environments\n- Secure Warehouse & API Integration\n- File and Dataset APIs\n- Private Slack or Teams support\n\nDatapane Teams is offered as both a managed SaaS service and an on-prem install. For more information, see [the documentation](https://docs.datapane.com/datapane-teams/tut-deploying-a-script). You can find pricing [here](https://datapane.com/pricing).\n\n## Next Steps\n\n- [Sign up for a free account](https://datapane.com/accounts/signup)\n- [Read the documentation](https://docs.datapane.com)\n- [Browse the API docs](https://datapane.github.io/datapane/)\n- [View featured reports](https://github.com/datapane/gallery/)\n\n# Analytics\n\nBy default, the Datapane Python library collects error reports and usage telemetry.\nThis is used by us to help make the product better and to fix bugs.\nIf you would like to disable this, simply create a file called `no_analytics` in your `datapane` config directory, e.g.\n\n### Linux\n\n```bash\n$ mkdir -p ~/.config/datapane && touch ~/.config/datapane/no_analytics\n```\n\n### macOS\n\n```bash\n$ mkdir -p ~/Library/Application\\ Data/datapane && touch ~/Library/Application\\ Data/no_analytics\n```\n\n### Windows (PowerShell)\n\n```powershell\nPS> mkdir ~/AppData/Roaming/datapane -ea 0\nPS> ni ~/AppData/Roaming/datapane/no_analytics -ea 0\n```\n\nYou may need to try `~/AppData/Local` instead of `~/AppData/Roaming` on certain Windows configurations depending on the type of your user-account.\n\n## Joining the community\n\nLooking to get answers to questions or engage with us and the wider community? Check out our [GitHub Discussions](https://github.com/datapane/datapane/discussions) board.\n\nSubmit feature requests, issues, and bug reports on this GitHub repo.\n\n## Open-source, not open-contribution\n\nDatapane is currently closed to external code contributions. However, we are tremendously grateful to the community for any feature requests, ideas, discussions, and bug reports.\n',
    'author': 'Datapane Team',
    'author_email': 'dev@datapane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.datapane.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11.0',
}


setup(**setup_kwargs)
