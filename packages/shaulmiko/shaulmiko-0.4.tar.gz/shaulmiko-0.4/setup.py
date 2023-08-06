from distutils.core import setup
setup(
  name = 'shaulmiko',         # How you named your package folder (shaulmiko)
  packages = ['shaulmiko'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Makes SSH sessions easier',   # Give a short description about your library
  author = 'Jakored and Ashal148148 on github',                   # Type in your name
  author_email = 'benja.bzness@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jakored1/ShaulMiko',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jakored1/pypi-shaulmiko/archive/refs/tags/v0.4.tar.gz',    # I explain this later on
  keywords = ['ShaulMiko', 'SSH', 'ssh', 'session', 'telnetlib', 'tty', 'cisco', 'router', 'switch', 'jakored', 'Ashal', 'paramiko', 'netmiko'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'paramiko',
          'typing',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
