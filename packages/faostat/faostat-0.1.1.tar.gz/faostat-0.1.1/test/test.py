# -*- coding: utf-8 -*-
"""
@author: Noemi E. Cazzaniga - 2022
@email: noemi.cazzaniga@polimi.it
"""


## Examples in README.md


import faostat

ld = faostat.list_datasets()
print('list_datasets =')
for el in range(0,5):
	print(ld[el])

df = faostat.list_datasets_df()
print('list_datasets_df =')
for el in range(0,5):
	print(df.iloc[el,:])

a = faostat.get_areas('QCL')
print('get_areas =')
for el, k in enumerate(a.keys()):
	print(k, a[k])
	if el > 4:
		break

y = faostat.get_years('QCL')
print('get_years =')
for el, k in enumerate(y.keys()):
	print(k, y[k])
	if el > 4:
		break

i = faostat.get_items('QCL')
print('get_items =')
for el, k in enumerate(i.keys()):
	print(k, i[k])
	if el > 4:
		break

e = faostat.get_elements('QCL')
print('get_elements =')
for el, k in enumerate(e.keys()):
	print(k, e[k])
	if el > 4:
		break

data = faostat.get_data('QCL',pars={'elements':[2312, 2313],'items':'221'})
print('get_data =')
print(data[0])
for el in range(40,45):
	print(data[el])

data_df = faostat.get_data_df('QCL',pars={'elements':[2312, 2313],'items':'221'})
print('get_data_df =')
for el in range(39,44):
	print(data_df.iloc[el,:])
