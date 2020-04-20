from distutils.core import setup
setup(
  name='ovirtlib4',
  packages=['ovirtlib4'],  # this must be the same as the name above
  license='Apache License 2.0',
  version='1.0.0',
  description='Ovirtsdk4 wrapper',
  long_description=open('README.rst').read(),
  author='Roni Eliezer',
  author_email='reliezer@redhat.com',
  url='https://github.com/roniezr/ovirtlib4',  # use the URL to the github repo
  download_url='https://github.com/roniezr/ovirtlib4-1.0.0.tar.gz',
  keywords=['red hat', 'virtualization', 'ovirt', 'ovirtsdk'],
  classifiers=[],
  install_requires=['pycurl', 'ovirt-engine-sdk-python'],
)
