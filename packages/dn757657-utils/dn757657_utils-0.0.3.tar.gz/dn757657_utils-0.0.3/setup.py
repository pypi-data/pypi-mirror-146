from distutils.core import setup

version = '0.0.3'

setup(name='dn757657_utils',
      version=version,
      packages=['dn_docoptutils', 'dn_fileutils'],
      license='MIT',
      description='personal utility funcs',
      author='Dan',
      author_email='daniel.js.campbell@gmail.com',
      url='https://github.com/dn757657/dn_utils.git',
      download_url='https://github.com/dn757657/dnutils/archive/refs/tags/' + version + '.tar.gz',
      keywords=['utility'],
      install_requires=[
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
