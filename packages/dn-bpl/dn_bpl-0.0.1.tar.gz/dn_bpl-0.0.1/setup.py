from distutils.core import setup

version = '0.0.1'

setup(name='dn_bpl',
      version=version,
      packages=['dn_bpl'],
      license='MIT',
      description='sql banking pipeline',
      author='Dan',
      author_email='daniel.js.campbell@gmail.com',
      url='https://github.com/dn757657/dn_bpl.git',
      download_url='https://github.com/dn757657/dn_bpl/archive/refs/tags/' + version + '.tar.gz',
      keywords=['sql', 'banking'],
      install_requires=[
            'python-dateutil~=2.8.2',
            'pandas~=1.3.5',
            'textblob~=0.17.1',
            'colorama~=0.4.4',
            'tabulate~=0.8.9',
            'SQLAlchemy~=1.4.32',
            'docopt~=0.6.2',
      ],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],
      )
