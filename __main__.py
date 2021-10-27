"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import resources
from pulumi_azure_native import network
from pulumi_azure_native.network import subnet
from pulumi_azure_native.network.get_subnet import get_subnet
from pulumi_azure_native import compute



#Create Resource Group

resource_group = resources.ResourceGroup(
    resource_name= "resource1",
    resource_group_name="rg1",
    location= "westus2"

)

virtual_network = network.VirtualNetwork(
    resource_name= "resource2",
    resource_group_name= resource_group.name,
    location= resource_group.location,
    address_space= network.AddressSpaceArgs(
                        address_prefixes= ["10.0.0.0/16"]
                   ),
    virtual_network_name="vnet1"
)

subnets = network.Subnet(
    resource_name="vnet_subnet1",
    subnet_name= "subnet1",
    address_prefix= "10.0.0.0/24",
    resource_group_name= resource_group.name,
    virtual_network_name= virtual_network.name
)

nic = network.NetworkInterface(
    resource_name= "nic1",
    resource_group_name= resource_group.name,
    location= resource_group.location,
    network_interface_name= "vm1-nic1",
    ip_configurations= [
        network.NetworkInterfaceIPConfigurationArgs(
            name= "ipconfig1",
            subnet= network.SubnetArgs(
                id= subnets.id
            ),
            
            
        ),
    ],
    enable_ip_forwarding=True
    
)

nic1 = network.NetworkInterface(
    resource_name= "nic2",
    resource_group_name= resource_group.name,
    location= resource_group.location,
    network_interface_name= "vm2-nic1",
    ip_configurations= [
        network.NetworkInterfaceIPConfigurationArgs(
            name= "ipconfig1",
            subnet= network.SubnetArgs(
                id= subnets.id
            ),
            
            
        ),
    ],
    enable_ip_forwarding=True
    
)

vm = compute.VirtualMachine(
    resource_name= "vmresource1",
    vm_name= "vm1",
    resource_group_name= resource_group.name,
    location=resource_group.location,
    os_profile= compute.OSProfileArgs(
        admin_username= "e360user",
        admin_password= "rit123ABC!@#$%^&*",
        computer_name= "vm1",
    ),
    hardware_profile= compute.HardwareProfileArgs(
        vm_size= "Standard_D2s_v3"

    
    ),
    network_profile=compute.NetworkProfileArgs(
        network_interfaces=[compute.NetworkInterfaceReferenceArgs(
            id= nic.id,
            primary= True,
        )],
    ),
    storage_profile= compute.StorageProfileArgs(
        image_reference= compute.ImageReferenceArgs(
            offer="UbuntuServer",
            publisher="Canonical",
            sku="16.04-LTS",
            version="latest",
        ),
        os_disk=compute.OSDiskArgs(
            caching="ReadWrite",
            create_option="FromImage",
            disk_size_gb=60,
            managed_disk=compute.ManagedDiskParametersArgs(
                storage_account_type="Premium_LRS",
            ),
            name="vm1-osdisk",
        )
    )

)

av = compute.AvailabilitySet(
    resource_name= "RESOURCEAV1",
    resource_group_name= resource_group.name,
    location= resource_group.location,
    availability_set_name= "av1",
    sku= compute.SkuArgs(
        name= "Aligned",
        

    ),
    platform_fault_domain_count=3
    

)

vm1 = compute.VirtualMachine(
    resource_name= "vmresource2",
    vm_name= "vm2",
    resource_group_name= resource_group.name,
    location=resource_group.location,
    availability_set= compute.SubResourceArgs(
        id= av.id
    ),
    os_profile= compute.OSProfileArgs(
        admin_username= "e360user",
        admin_password= "rit123ABC!@#$%^&*",
        computer_name= "vm2",
    ),
    hardware_profile= compute.HardwareProfileArgs(
        vm_size= "Standard_D2s_v3"

    
    ),
    network_profile=compute.NetworkProfileArgs(
        network_interfaces=[compute.NetworkInterfaceReferenceArgs(
            id= nic1.id,
            primary= True,
        )],
    ),
    storage_profile= compute.StorageProfileArgs(
        image_reference= compute.ImageReferenceArgs(
            offer="UbuntuServer",
            publisher="Canonical",
            sku="16.04-LTS",
            version="latest",
        ),
        os_disk=compute.OSDiskArgs(
            caching="ReadWrite",
            create_option="FromImage",
            disk_size_gb=60,
            managed_disk=compute.ManagedDiskParametersArgs(
                storage_account_type="Premium_LRS",
            ),
            name="vm2-osdisk",
        )
    )

)





pulumi.export("vnet", virtual_network.id)
pulumi.export("vm_name", vm.name)
pulumi.export("vm_ipaddress",vm)





# # Create an Azure Resource Group
# resource_group = resources.ResourceGroup('resource_group')


# # Create an Azure resource (Storage Account)
# account = storage.StorageAccount('sa',
#     resource_group_name=resource_group.name,
#     sku=storage.SkuArgs(
#         name=storage.SkuName.STANDARD_LRS,
#     ),
#     kind=storage.Kind.STORAGE_V2)

# # Export the primary key of the Storage Account
# primary_key = pulumi.Output.all(resource_group.name, account.name) \
#     .apply(lambda args: storage.list_storage_account_keys(
#         resource_group_name=args[0],
#         account_name=args[1]
#     )).apply(lambda accountKeys: accountKeys.keys[0].value)

# pulumi.export("primary_storage_key", primary_key)
