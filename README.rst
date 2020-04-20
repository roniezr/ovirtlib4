==============================
**Ovirtlib4 Project Overview**
==============================

The **Ovirtlib4 Project** is a wrapper for the ovirtsdk4 project, 
It fully integrated with ovirtsdk4. 
You can use the benefits of this wrapper without losing 
any ability exists at the ovirtsdk4


**Requirements**
----------------
- Python 2.7, 3.6
- ovirtsdk4


**Installation**
----------------
 .. code-block:: python

  $ pip install git+https://github.com/roniezr/ovirtlib4.git


**Introduction**
----------------
This lib design to simplify the use of ovirtsdk4
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


**Project Requirments**
---------------------- 
1. Fully integrated with the parent ovirtsdk4
2. Quickly and simlply use of oVirt REST commands


**Main Concept**
----------------
It all starts with the OvirtLib() main class
This class holds the oVirt Collections and it's used as
the root point accessing any oVirt entity, only by using 
class-path navigation.

Each collection return a list of CollectionEntity() classes
Each CollectionEntity() class include two fields
- CollectionEntity.entity that hold the Entity type, e.g.: ovirtsdk4.types.Vm
- CollectionEntity.service that hold the Entity service, e.g.: ovirtsdk4.system_service().vms_service().vm_service()  

Any function that starts with the word 'get*()' or list() is retrieving data from the remote oVirt Engine


**OvirtSdk4 vs. OvirtLib examples**
------------------------------------
 *Retreive VMs*:

 .. code-block:: python

 ovirtsdk4.system_service().vms_service().list()
 eqvivalent to:
 ovirtlib.vms.list() or ovirtlib.vms.get()
 
 list() & get() fully integrated with ovirtsdk4
 so you can use vms.list(search="name=VM_name") to retreive a special VM 
 e.g.: vms.list(search="name!=HostedEngine") will return all VM except the HostedEngine VM
 
 vm = ovirtlib.vms.list()[0] 
 vm.entity
 vm.service

 vm.entity
 eqvivalent to: 
 vm = ovirtsdk4.system_service().vms_service().list()[0]
 
 vm.service
 eqvivalent to:
 vm_service = ovirtsdk4.system_service().vms_service().vm_service(id=vm.id).get()  


**Examples**
------------------

 *Initialaize the class*:

 .. code-block:: python
  
  from ovirtlib4 import ovirtlib
  engine = ovirtlib.OvirtLib(host="192.168.1.100", password="engine_admin_password") 

 *Get and start all VMs*:
  
  vms = engine.vms.list()
  for vm in vms:
    print("Starting VM {name}".format(name=vm.entity.name))
    vm.entity.service.start()  
 
 *Get all hosts*:
 
  hosts = engine.hosts.list()

 *You can use the get_names() CollectionService method to get a list of all entities*:

  engine.hosts.get_names()

 
