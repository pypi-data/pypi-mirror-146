# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib', 'xontrib_powerline3']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit', 'xonsh>=0.12']

setup_kwargs = {
    'name': 'xontrib-powerline3',
    'version': '0.3.17',
    'description': 'Yet another powerline theme for xonsh with async prompt support.',
    'long_description': '# Powerline3\nYet another powerline like prompt for xonsh with async prompt support. \n\n## Why another one?\n\n- It uses `$PROMPT_FIELDS` and no need to have a separate functions and renderer. \n  Since the addition of `$PROMPT_TOKENS_FORMATTER` it is possible to use the existing \n  set of functions to emulate powerline theme for xonsh prompts.\n- Async prompt mode works as well. \n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-powerline3\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-powerline3\n```\n\n## Usage\n\n``` xsh\nxontrib load powerline3 prompt_ret_code\n\n# the foreground/background colors of the prompt-fields can be configured as below. \n# This works for custom fields as well\n# The format is `<prompt-field-name>__pl_colors`. It can be a function returning `tuple[str, str]`\n# or set tuples directly as below.\n$PROMPT_FIELDS["cwd__pl_colors"] = ("WHITE", "CYAN")\n\n# choose the powerline glyph used\n$POWERLINE_MODE = "powerline" # if not set then it will choose random\n# available modes: round/down/up/flame/squares/ruiny/lego\n\n# define the prompts using the format style and you are good to go\n$PROMPT = "".join(\n    [\n        "{vte_new_tab_cwd}",\n        "{cwd:{}}",\n        "{gitstatus:\ue0a0{}}",\n        "{ret_code}",\n        "{background_jobs}",\n        os.linesep,\n        "{full_env_name: 🐍{}}",\n        "$",\n    ]\n)\n$RIGHT_PROMPT = "".join(\n    (\n        "{long_cmd_duration: ⌛{}}",\n        "{user: 🤖{}}",\n        "{hostname: 🖥{}}",\n        "{localtime: 🕰{}}",\n    )\n)\n```\n\n## Extra PROMPT_FIELDS\n\n### 1. `full_env_name`\n\n- When the `env_name` \n  - is `.venv` show the name of the parent folder\n  - contains `-py3.*` (when it is poetry created) shows the project name part alone\n  \n### 2. `background_jobs`\n- show number of running background jobs\n\n\n## Examples\n\n![screenshot.png](docs/screenshot.png)\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).\n- https://www.nerdfonts.com/cheat-sheet?set=nf-ple-\n- https://github.com/romkatv/powerlevel10k#meslo-nerd-font-patched-for-powerlevel10k\n\n## Similar Projects\n- https://github.com/vaaaaanquish/xontrib-powerline2\n- https://github.com/santagada/xontrib-powerline\n',
    'author': 'Noortheen Raja NJ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-powerline3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
