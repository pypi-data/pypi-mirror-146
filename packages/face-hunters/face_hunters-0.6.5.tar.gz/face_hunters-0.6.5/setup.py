from setuptools import setup
from setuptools import find_packages

setup(
  name = 'face_hunters',         # How you named your package folder (MyLib)
  packages = find_packages(),   # Chose the same as "name"
  version = '0.6.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is an application developped by 4BIM INSA students to help you create a robot portait of your agressor.',   # Give a short description about your library
  author = 'G3',                   # Type in your name
  author_email = 'lucieschw@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/lucieschwoertzig/face_hunters',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/lucieschwoertzig/face_hunters/archive/refs/tags/v_4.tar.gz',    # I explain this later on
  keywords = ['PORTRAITS', 'AUTOENCODER', 'GENETIC'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'pillow',
          'keras',
          'tensorflow',
          'matplotlib',
          'scikit-image',
          'sklearn',
          'scipy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  package_data={'face_hunters':['*.png', '*.jpg', '*.h5', '*.npy'], 'build':['doctrees/*.doctree', 'doctrees/*.pickle', 'html/*.html', 'html/*.js', 'html/*.inv']},
)
