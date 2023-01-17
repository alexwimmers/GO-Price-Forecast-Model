import pandas as pd
import numpy as np
from pandas import Series, DataFrame
abt_table = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw_KURZ.xlsx', sheet_name = 'Zahlungsfähigkeit')
el_cost = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw_KURZ.xlsx', sheet_name = 'Stromkosten')
country_list = pd.read_excel('Data/Countries.xlsx')
cons_aware = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw.xlsx', sheet_name = 'Konsumentennähe')

for abt_len in range(len(country_list)):
    for cons_len in range(len(cons_aware)):
        abt_cou = abt_table.iat[0,abt_len]
        abt_sek = abt_table.iat[0,abt_len]
        abt_siz = abt_table.iat[0,abt_len]
        cons_sek = cons_aware.iat[0,cons_len]
        print(cons_sek+" "+abt_siz)        


