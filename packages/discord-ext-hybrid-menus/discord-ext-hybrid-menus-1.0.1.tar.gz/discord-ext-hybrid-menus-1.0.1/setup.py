from setuptools import setup
import re

version = ''
with open('discord/ext/menus/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

if version.endswith(('a', 'b', 'rc')):
    # append version identifier based on commit count
    try:
        import subprocess
        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass

with open('README.md') as f:
    readme = f.read()

setup(name='discord-ext-hybrid-menus',
      author='regulad',
      url='https://github.com/regulad/discord-ext-hybrid-menus',
      version=version,
      packages=['discord.ext.menus'],
      license='MIT',
      long_description=readme,
      long_description_content_type='text/markdown',
      description='An extension module to make reaction based menus with discord.py',
#      extras_require={
#          "dev": ["discord.py@git+https://github.com/iDevision/enhanced-discord.py"]
#      },
      python_requires='>=3.8.0'
)
