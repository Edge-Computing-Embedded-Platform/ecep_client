import container as container

"""
temp = {"all":"all"}
templist = container.list_containers(temp)
print templist

tempvar1 = {'name':'hirambbb','image':'training/webapp'}
tempCCN = container.create_containers(tempvar1)
print tempCCN
s
tempvar2 = {'container':'nostalgic_bhabha'}
tempCC = container.run_container(tempvar2)
print tempCC

tempvar3 = {'container':'romantic_easley','name':'chin'}
tempRN = container.rename_container(tempvar3)
print tempRN	

tempvar4 = {'force':'force','image':'hello-world'}
tempDI = container.delete_image(tempvar4)
print tempDI
"""
tempvar1 = {'name':'hirambbb','image':'training/webapp'}
tempCCN = container.create_containers(tempvar1)
print tempCCN

tempvar6 = {'container': 'hirambbb'}
tempCC = container.stop_container(tempvar6)
print tempCC

tempvar6 = {'container': 'hirambbb'}
tempCC = container.stop_container(tempvar6)
print tempCC

"""
tempvar5 = {'container':'hirambbb'}
tempCI = container.delete_container(tempvar5)
print tempCI 


tempvar6 = {'container': 'nostalgic_bhabha'}
tempCC = container.stop_container(tempvar6)
print tempCC
"""
