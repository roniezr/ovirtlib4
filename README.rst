==============================
**Ovirtlib4 Project Overview**
==============================

  The **Ovirtlib4 Project** is a wrapper for the OvirtSdk4 project,
  It fully integrated with OvirtSdk4.
  You can use the benefits of this wrapper without losing
  any OvirtSdk4 abilities


**Requirements**
----------------
- Python 2.7, 3.6
- ovirtsdk4


**Installation**
----------------

 .. code-block:: bash

  $ export PYCURL_SSL_LIBRARY=openssl
  $ pip install git+https://github.com/roniezr/ovirtlib4.git

 PYCURL_SSL_LIBRARY is required to install "pycurl" that required by ovirtsdk4,
 If you encounter the following error while import ovirtsdk4 or ovirtlib4

 .. code-block:: bash

  ImportError: pycurl: libcurl link-time ssl backend (openssl) is different from compile-time ssl backend (nss)

 Then run the following commands to fix it:

 .. code-block:: bash

  $ export PYCURL_SSL_LIBRARY=openssl
  $ pip uninstall pycurl
  $ pip install pycurl --no-cache-dir


**Introduction**
----------------
  This lib design to simplify the use of OvirtSdk4.
  The main class is the root for all oVirt components/entities,
  by navigating the class-path you can **quickly** find and set/get
  any oVirt feature/information.


**Why this lib is required**
-----------------------------
  The main ovirtsdk4 include basic REST API commands, it still needs
  to create simple methods to execute complex operations.
  So instead of "inventing the wheel" again and again by different developer/teams,
  you can use this library and contribute to the community by extending it
  with your added methods


**Project Vision**
----------------------
1. Fully integrated with the parent ovirtsdk4
2. Quickly and simply use of oVirt REST commands


**Main Concept**
----------------
  It all starts with the OvirtLib() main class
  This class holds the oVirt Collections and it used as
  the root point accessing any oVirt entity, only by using
  class-path navigation.

  | Each collection return a list of **CollectionEntity()** classes
  | Each CollectionEntity() class include two fields

  - **CollectionEntity.entity** hold the Entity type, (e.g.: ovirtsdk4.types.Vm) include the Entity properties and 'links'.

  - **CollectionEntity.service** hold the Entity service, that holds the Entity 'actions'.

  |
  | **Sub collections**
  | -----------------------
  | See example below, how to define new sub-collection.
  | Once it added user can use it as follows:
  | *engine.vms.list()[0].nics.list()*

   .. code-block:: python

    class VmEntity(CollectionEntity):
        """
        Put VM custom functions here
        """
        @property
        def nics(self):
            # Initialize the sub-collection with its parent service
            # Integrate VmNics inside VmEntity, so it can be accessed by class-path navigation
            return VmNics(connection=self.service)

    class VmNics(CollectionService):
        """
        Gives access to all VM NICs
        """
        def service(self):
            """ Overwrite abstract parent method """
            return self.connection.nics_service()  # Define the sub-collection service

        def _entity_service(self, id):
            """ Overwrite abstract parent method """
            return self.service().nic_service(id=id) # Define the sub-collection sub service

        def get_entity_type(self):
            """ Overwrite abstract parent method """
            return types.Nic

        def _get_collection_entity(self):
            """ Overwrite abstract parent method """
            return VmNic(connection=self.connection)  # Define the CollectioEntity for the

    class VmNic(CollectionEntity):   # Create the CollectioEntity
        """
        Put VmNic custom functions here
        """
        def __init__(self, *args, **kwargs):
            CollectionEntity. __init__(self, *args, **kwargs)

  |
  | **follow_link()**
  | ------------------
  | To retrieve an Entity link you can use the **CollectionEntity.follow_link()** method.
  | **Note:** It is recommended to integrate it inside the CollectionEntity object so it can be called through class-path navigation,
  | To retrieve the Entity service, it requires to pass the related *CollectionService* object as well.
  | You will not need to use follow_link() if a sub-collection was implemented as the above example.

- Functions starts with **'get*()'** or **list()** are retrieving data from the remote oVirt Engine.

***************************
**OvirtSdk vs. OvirtLib**
***************************
 *Retrieving VMs via OvirtSdk4*:

 .. code-block:: python

  ovirtsdk4.system_service().vms_service().list()


 *Is equivalent for the following OvirtLib4 command*:

 .. code-block:: python

  ovirtlib.vms.list()

list() and get()
*****************
 | *list()* and *get()* are fully integrated with OvirtSdk4
 | The list methods of some services support additional parameters.
 | For more information please refer to the OvirtSdk4 documentation
 |
 | For example you can use vms.list(search="name=VM_name") to retrieve a special VM
 | Or use the 'max' parameter to limit the retrieving events
 |
 | *e.g.: the following will return all VM except the HostedEngine VM*:

 .. code-block:: python

  engine.vms.list(search="name!=HostedEngine")

 | *e.g.: the following will return 10 events*:

 .. code-block:: python

  engine.events.list(max=10)


CollectionEntiry
****************
  .. code-block:: python

   vm = ovirtlib.vms.list()[0] # list() return list of CollectionEntiry() classes
   vm.entity                   # entity, hold the Entity fields and links
   vm.service                  # service, hold the Entity actions

  At the above commands **vm.entity** is equivalent to:

  .. code-block:: python

    vm = ovirtsdk4.system_service().vms_service().list()[0]

  And **vm.service** is equivalent to:

  .. code-block:: python

   vm_service = ovirtsdk4.system_service().vms_service().vm_service(id=vm.id)


**Examples**
------------------

 Initialize the OvirtLib class e.g.:

 .. code-block:: python

  from ovirtlib4 import ovirtlib
  engine = ovirtlib.OvirtLib(host="192.168.1.100", password="engine_admin_password")

 Get and start all VMs:

 .. code-block:: python

  vms = engine.vms.list()
  for vm in vms:
    print("Starting VM {name}".format(name=vm.entity.name))
    vm.service.start()

 Get all hosts:

 .. code-block:: python

  hosts = engine.hosts.list()

 You can use the get_names() CollectionService method to retrieve the names of all entities at the collection:

 .. code-block:: python

  engine.hosts.get_names()



**Contribute**
------------------
  - git clone https://github.com/roniezr/ovirtlib4.git

  - It is recommended to read ovirtsdk4 documentation before starting to contribute to this project https://access.redhat.com/documentation/en-us/red_hat_virtualization/4.3/pdf/python_sdk_guide/Red_Hat_Virtualization-4.3-Python_SDK_Guide-en-US.pdf
