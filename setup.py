from distutils.core import setup
setup(
  name='ovirtlib4',
  packages=['ovirtlib4', 'ovirtlib4.utils'],
  license='Apache License 2.0',
  version='1.1.0',
  description='Ovirtsdk4 wrapper',
  long_description=open('README.rst').read(),
  author='Roni Eliezer',
  author_email='reliezer@redhat.com',
  url='https://github.com/rhevm-qe-automation/ovirtlib4',
  download_url='https://github.com/rhevm-qe-automation/ovirtlib4-1.1.0.tar.gz',
  keywords=['red hat', 'virtualization', 'ovirt', 'ovirtsdk'],
  classifiers=[],
  install_requires=['pycurl', 'ovirt-engine-sdk-python'],
)
