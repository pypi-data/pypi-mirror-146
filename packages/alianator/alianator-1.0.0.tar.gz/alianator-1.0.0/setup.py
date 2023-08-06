# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['alianator']
install_requires = \
['titlecase>=2.3,<3.0']

setup_kwargs = {
    'name': 'alianator',
    'version': '1.0.0',
    'description': 'alianator is a tool to help Pycord and discord.py users easily resolve user-facing aliases for Discord permission flags.',
    'long_description': '# alianator\n\nalianator is a tool that helps [Pycord](https://github.com/Pycord-Development/pycord) and\n[discord.py](https://github.com/Rapptz/discord.py) users easily resolve user-facing aliases for Discord permission\nflags.\n\n## Installation\n\n```bash\n$ pip install alianator\n```\n\nalianator doesn\'t include either Pycord or discord.py as a dependency; instead, it allows you to use whichever of the \ntwo libraries you prefer. alianator **does not and will not** support other Discord API wrappers, such as\n[Nextcord](https://github.com/nextcord/nextcord), [Hikari](https://github.com/hikari-py/hikari), or\n[disnake](https://github.com/DisnakeDev/disnake).\n\n## Usage\n\nalianator can resolve aliases from `discord.Permissions` objects, integers, strings, tuples, lists of strings, and lists\nof tuples.\n\n```python\nimport alianator\n\nalianator.resolve(arg, mode=mode)\n```\n\nThe optional `mode` flag can be used to specify which permission should be resolved. If `mode` is `True`, only granted\npermissions will be resolved; if `mode` is `False`, only denied permissions will be resolved; if `mode` is `None`, all\npermissions will be resolved. If `mode` is not explicitly specified, it will default to `None`.\n\n```python\nimport alianator\nimport discord\n\n# Resolving from a discord.Permissions object\nperms = discord.Permissions.general()\naliases = alianator.resolve(perms, mode=True)\nprint(aliases)\n# [\'Manage Channels\', \'Manage Server\', \'View Audit Log\', \'Read Messages\', \'View Guild Insights\', \'Manage Roles\', \'Manage Webhooks\', \'Manage Emojis and Stickers\']\n\n\n# Resolving from an integer\nperms = 3072\naliases = alianator.resolve(perms, mode=True)\nprint(aliases)\n# [\'Read Messages\', \'Send Messages\']\n\n\n# Resolving from a string\nperms = "send_tts_messages"\naliases = alianator.resolve(perms, mode=True)\nprint(aliases)\n# [\'Send Text-To-Speech Messages\']\n\n\n# Resolving from a tuple\nperms = ("moderate_members", True)\naliases = alianator.resolve(perms, mode=True)\nprint(aliases)\n# [\'Timeout Members\']\n\n\n# Resolving from a list of strings\nperms = ["manage_guild", "manage_emojis"]\naliases = alianator.resolve(perms, mode=True)\nprint(aliases)\n# [\'Manage Server\', \'Manage Emojis and Stickers\']\n\n\n# Resolving from a list of tuples\nperms = [("use_slash_commands", True), ("use_voice_activation", True)]\naliases = alianator.resolve(perms, mode=True)\nprint(aliases)\n# [\'Use Application Commands\', \'Use Voice Activity\']\n```\n\nThat\'s about all there is to it. alianator does one thing and does it well.\n\n## License\n\nalianator is released under the [MIT License](https://github.com/celsiusnarhwal/alianator/blob/master/LICENSE.md).',
    'author': 'celsius narhwal',
    'author_email': 'celsiusnarhwal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/celsiusnarhwal/alianator',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
