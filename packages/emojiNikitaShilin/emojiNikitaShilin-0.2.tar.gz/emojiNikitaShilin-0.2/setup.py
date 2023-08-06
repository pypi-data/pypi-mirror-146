from setuptools import setup, find_packages

setup(name='emojiNikitaShilin',
      version='0.2',
      description='The first emoji library for Python',
      long_description='kek.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='emoji',
      url='http://github.com/4il612/emojiNS',
      author='Nikita Shilin',
      author_email='shilin.nick@yandex.ru',
      license='Bauman University',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)