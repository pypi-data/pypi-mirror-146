from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='Inline-input',
      author="NeuralTeam",
      version='0.4',
      description='Rethinking input() with inline auto-completion, minimum character requirement, and more.',
      packages=['inline'],
      author_email='NeuralTeam@mail.ru',
      zip_safe=False,
      install_requires=["thefuzz", "colorama"],
      classifiers=['Operating System :: Microsoft :: Windows', 'Programming Language :: Python'],
      long_description=long_description,
      long_description_content_type='text/markdown'
      )
