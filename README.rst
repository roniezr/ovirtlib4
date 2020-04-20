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

  $ pip install git+https://github.com/roniezr/ovirtlib4.git


**Introduction**
----------------
This lib design to simplify the use of OvirtSdk4.
The main class is the root for all oVirt components/entities,
by navigating the class path you can **quickly** find and set/get
any oVirt feature/information.


**Why this lib is required**
-----------------------------
The main ovirtsdk4 include basic REST API commands, it still needs
to create simple methods to execute complex operations.
So instead of "inventing the wheel" again and again by different developer/teams,
you can use this library and contribute to the community by extending it
to support as much as possible simple oVirt methods.


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

- **CollectionEntity.entity** hold the Entity type, (e.g.: ovirtsdk4.types.Vm) include the Entity properties.

- **CollectionEntity.service** hold the Entity service, that holds the Entiry 'actions' and 'links'.

|
**follow_link():**
 To retreive a link you can use the **CollectionEntity.follow_link()** method
|     **Note:** It is recommended to integrate it inside the CollectionEntity object so it can be called through class-path navigation

  *As followed e.g.:*:

 .. code-block:: python

	class VmEntity(CollectionEntity):
	    def get_nics(self):
		return self.follow_link(link=self.service.nics)

	engine.vms.list()[0].get_nics()
|
|     The above follow_link() command will return the "CollectionEntiry.entiry" field only,
|     to retreive the Entiry service as well, it require to pass the CollectionClass object as well. see following example:

 .. code-block:: python

   from . import disks

   class VmEntity(CollectionEntity):

      def get_disk_attachments(self):
          """ Return list of all VM disks: [CollectionEntity] """
          return self.follow_link(
              # We want to retrieve VM disk so a disk Collection should be pass
              collection_service=disks.Disks(self.connection),
              link=self.service.disk_attachments
          )

- Functions starts with **'get*()'** or **list()** are retrieving data from the remote oVirt Engine.

**OvirtSdk4 vs. OvirtLib**
---------------------------
 *Retrieving VMs via OvirtSdk4*:

 .. code-block:: python

  ovirtsdk4.system_service().vms_service().list()


 *Is equivalent for the following OvirtLib4 command*:

 .. code-block:: python

  ovirtlib.vms.list()

list() and get()
-----------------
| *list()* and *get()* are fully integrated with OvirtSdk4
| so you can use vms.list(search="name=VM_name") to retrieve a special VM
|
  *e.g.: the following will return all VM except the HostedEngine VM*:

 .. code-block:: python

  vms.list(search="name!=HostedEngine")

CollectionEntiry
------------------
  .. code-block:: python

   vm = ovirtlib.vms.list()[0]      # List() return CollectionEntiry() class
   vm.entity                        # entity, hold the Entity fields
   vm.service                       # service, hold the Entity actions and links

  At the above commands **vm.entity** is equivalent to:

  .. code-block:: python

    vm = ovirtsdk4.system_service().vms_service().list()[0]

  And **vm.service** is equivalent to:

  .. code-block:: python

   vm_service = ovirtsdk4.system_service().vms_service().vm_service(id=vm.id).get()


**Examples**
------------------

 *Initialize the class*:

 .. code-block:: python

  from ovirtlib4 import ovirtlib
  engine = ovirtlib.OvirtLib(host="192.168.1.100", password="engine_admin_password")

 *Get and start all VMs*:

 .. code-block:: python

  vms = engine.vms.list()
  for vm in vms:
    print("Starting VM {name}".format(name=vm.entity.name))
    vm.service.start()

 *Get all hosts*:

 .. code-block:: python

  hosts = engine.hosts.list()

 *You can use the get_names() CollectionService method to get a list of all entities*:

 .. code-block:: python

  engine.hosts.get_names()



**Contribute**
------------------
git clone https://github.com/roniezr/ovirtlib4.git

It is recommended to read ovirtsdk4 documentation before starting to contribute to this project
https://access.redhat.com/documentation/en-us/red_hat_virtualization/4.3/pdf/python_sdk_guide/Red_Hat_Virtualization-4.3-Python_SDK_Guide-en-US.pdf

