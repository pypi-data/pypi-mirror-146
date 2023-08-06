from setuptools import setup

setup(name='nae-inference', # name of modul to use in pip install command
      version='0.1',
      description='A dummy repo for nae-inference',
      url='https://example.com/',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['nae_inference'], # name of subfolder with source code and used for import after install
      zip_safe=False)