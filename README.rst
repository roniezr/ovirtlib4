==============================
**Ovirtlib4 Project Overview**
==============================

  The **Ovirtlib4 Project** is a wrapper for the OvirtSdk4 project,
  It fully integrated with OvirtSdk4.
  You can use the benefits of this wrapper without losing
  any OvirtSdk4 abilities


**Requirements**
----------------
- Python 3.6
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
  $ pip install -I pycurl --no-cache-dir


**Introduction**
----------------
  This Lib file is intended to simplify the use of OvirtSdk4.
  The main class is the root of all the components/entities of oVirt,
  by navigating the classpath you can **quickly** find and set/get
  any oVirt feature/information.


**Why this lib is required**
-----------------------------
  The main ovirtsdk4 includes basic REST API commands, it still needs
  create simple methods for performing complex operations.
  So instead of "inventing the wheel" again and again by different developer/teams,
  you can use this library and contribute to the community by extending it
  with your added methods


**Project Vision**
----------------------
1. Fully integrated with the parent ovirtsdk4
2. Quick and easy use of oVirt REST commands


**Main Concept**
----------------
  It all starts with the **OvirtLib()** main class.
  This class holds the oVirt Collections and it used as
  the root point accessing any oVirt entity, only by using
  class-path navigation.

  | Each collection return a list of **CollectionEntity()** classes
  | Each CollectionEntity() class include two fields

  - **CollectionEntity.entity** hold the Entity type, (e.g.: ovirtsdk4.types.Vm) it includes the Entity properties and 'links'.

  - **CollectionEntity.service** hold the Entity service, that holds the Entity 'actions'.

  |
  | ** **Collection** **
  | --------------------------------
  | Each collection must inherit from **CollectionService()**
  | The new inherit class must define 3 parameters at the __init__() method:
  | 1. **self.service**: the collection service from the SDK
  | 2. **self.entity_service**: the entity service usually found under 'self.service' above
  | 3. **self.entity.type**: the entity type from the SDK
  |
  | The new inherit class must also overwrite the following method
  | 4. **_get_collection_entity()**:
  | This method must return a link to a new class inherit from **CollectionEntity()**.
  | This class represent an individual entity inside the collection,
  | It used to:
  | - Store custom functions related to the individual entity.
  | - Add links to its sub collections
  |
  | See the example below, how to define VMs collection that will return a list of VmEntitiy()'s

   .. code-block:: python

    class Vms(CollectionService):
    """
    Gives access to all Ovirt VMs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().vms_service()  # 1 above
        self.entity_service = self.service.vm_service                  # 2 above
        self.entity_type = types.Vm                                    # 3 above

        def _get_collection_entity(self):                # 4 above
        """ Overwrite abstract parent method """
        return VmEntity(connection=self.connection)

    class VmEntity(CollectionEntity):                    # 4 above
    """
    Put VM custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)

  |
  | ** **Sub-Collection** **
  | --------------------------------
  | Entity can include other collections, for example, VM can include collections of NICs or Disks, etc...
  |
  | At the example below, we define sub-collection for the VmEntitiy()

   .. code-block:: python

    class VmEntity(CollectionEntity):
    """
    Put VM custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)

    @property
    def nics(self):
        return VmNics(connection=self.service)  # self.service is the indevidual VM service

    class VmNics(CollectionService):
    """
    Gives access to all VM NICs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.nics_service()   # self.connection is the VM collection service
        self.entity_service = self.service.nic_service  # same as Collection above
        self.entity_type = types.Nic                    # same as Collection above

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmNic(connection=self.connection)


    class VmNic(CollectionEntity):
    """
    Put VmNic custom functions here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

  |

follow_link()
*****************
  | There are several options for retrieving entity links:
  |
  | 1. Through get() e.g.: **get(follow="link_name")**
  |    For more information about the 'follow' get() parameter see:
  |    https://www.ovirt.org/develop/release-management/features/infra/link-following.html
  | 2. Define the **'self.follows'** for a collection
  |    **self.follows**: If it sets, it will retrieve assigning links when calling get()
  | 3. Use the **ovirtlib.follow_link()** method
  | 4. Use the **CollectionEntity.follow_link()** method
  |
  | Sections 1..3 will retrieve the entity links, but they will not include the entity service
  | Option 4 will also include the application service if it initializes the 'collection_service' parameter
  | **Note** that you will not need to use *'follow_link()'* if a sub-collections is defined instead
  |

get()
*****************
 | **get()** is fully integrated with OvirtSdk4 **list()** method
 | The SDK list() methods of some services support additional parameters.
 | For more information please refer to the OvirtSdk4 documentation
 |
 | For example you can use vms.get(search="name=VM_name") to retrieve a special VM
 | Or use the 'max' parameter to limit the retrieving events

 .. code-block:: python

  *E.g.: the following will return the HostedEngine VM only*:

  engine.vms.list(search="name!=HostedEngine")


  *E.g.: the following will return 10 events*:

 .. code-block:: python

  engine.events.get(max=10)

 | From v1.1.0 'get()' will be executed when calling the collection class e.g.: vms()
 | So *'ovirtlib.vms.get()'* is eqvivalent to *'ovirtlib.vms()'*
 | Note that to be updated with the remote engine you must call 'get()'
 | e.g.:
 | *'vm.entity.status'* and *'vm().entity.status'* or *'vm.get().entity.status'* are not equivalent,
 | the first read the status of a local retrieved VM class and the second,
 | first retrieves the VM data from the remote engine and then display its status
 |
 | *E.g.: the following will return all VM except the HostedEngine VM*:
 |
 | **Note** that as a convention functions that starts with **'get*()'** or **list()**
 | are retrieving data from the remote Engine.
 |


CollectionEntiry
****************
  .. code-block:: python

   vms = ovirtlib.vms()      # Return list of CollectionEntiry() class
   vms = ovirtlib.vms.get()  # Same as above
   vms[0].entity             # entity holds the Entity fields and links
   vms[0].service            # service holds the Entity actions

  At the above commands **vm.entity** is equivalent to:

  .. code-block:: python

    vm = ovirtsdk4.system_service().vms_service().list()[0]

  And **vm.service** is equivalent to:

  .. code-block:: python

   vm_service = ovirtsdk4.system_service().vms_service().vm_service(id=vm.id)

***************************
**OvirtSdk vs. OvirtLib**
***************************
 *E.g: retrieving VM/s via OvirtSdk4, start it, and display its name*:

 .. code-block:: python

  vm = sdk_connection.system_service().vms_service().list()[0]
  vm_service = sdk_connection.system_service().vms_service().vm_service(id=vm.id)
  vm_sevice.start()
  print(vm.name)

 *Is equivalent for the following OvirtLib4 command*:

 .. code-block:: python

  vm = ovirtlib.vms()[0]
  vm.service.start()
  print(vm.entity.name)

**Examples**
------------------

 Initialize the OvirtLib class e.g.:

 .. code-block:: python

  from ovirtlib4 import ovirtlib
  engine = ovirtlib.OvirtLib(host="192.168.1.100", password="engine_admin_password")

 Get and start all VMs:

 .. code-block:: python

  vms = engine.vms.get()
  for vm in vms:
    print("Starting VM {name}".format(name=vm.entity.name))
    vm.service.start()

 Get all hosts:

 .. code-block:: python

  hosts = engine.hosts.get() or
  hosts = engine.hosts()

 You can use the get_names() CollectionService method to retrieve the names of all entities at the collection:

 .. code-block:: python

  engine.hosts.get_names()

 .. code-block:: python

  """ Add Example, use the 'entity_type()' of each collection to add new entities to a collection """
  vm1 = engine.vms()[0]  # Get the first VM
  vnic_profile = engine.vnic_profiles()[0]  # Get the first vNIC Profile

  new_nic = vm1.nics.entity_type(  # Use the entity_type to create the new NIC object
      name='new_nic_name',
      vnic_profile=engine.vnic_profiles.entity_type(id=vnic_profile.entity.id)
  )

  vm1.nics.service.add(new_nic)  # Add the new NIC to selected VM


**Contribute**
------------------
  - git clone https://github.com/roniezr/ovirtlib4.git

  - It is recommended to read ovirtsdk4 documentation before starting to contribute to this project https://access.redhat.com/documentation/en-us/red_hat_virtualization/4.3/pdf/python_sdk_guide/Red_Hat_Virtualization-4.3-Python_SDK_Guide-en-US.pdf

|