import pandas as pd
#import numpy as np
from pandas import Series, DataFrame
"""
abt_table = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw_DUMMY.xlsx', sheet_name = 'Zahlungsfähigkeit_Bereinigt')
el_cost = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw_DUMMY.xlsx', sheet_name = 'Stromkosten')
country_list = pd.read_excel('Data/Countries.xlsx')
wtp_val_list = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw_DUMMY.xlsx', sheet_name = 'Zahlungsbereitschaften')
cons_aware = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw_DUMMY.xlsx', sheet_name = 'Konsumentennähe')
derating_factors = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Derating_Factors')
test_list = pd.DataFrame(columns=['Land','Größe','Sektor1','Sektor2','jahr','abt_val','cons_val'])
#goo_list = pd.read_excel("Data/20200921_GoO Information_v01_aw.xlsx", sheet_name="Technologieaufteilung")


def ausführen():
    df = wtp_Matching()
    print("wtp matched")
    df2 = max_wtp_Calculation(df)
    print("max wtp calculated")
    derated_wtp_calculation(df2)
    print("ich habe fertig")

#Funktionen
def wtp_Matching():
    
    wtp_list = pd.DataFrame(columns=['Land','Größe','Sektor','Jahr', 'WTP'])
    
    for abt_pos in range(len(abt_table)):        
        for cons_pos in range(len(cons_aware)):    
            
            abt_sek = abt_table.iat[abt_pos,1]
            cons_sek = cons_aware.iat[cons_pos,0]
            
            if cons_sek == abt_sek:
                
                for i in range(4,13):
                    abt_year = abt_table.columns[i]
                    abt_cou = abt_table.iat[abt_pos,0]
                    abt_val = abt_table.iat[abt_pos,i]
                    abt_siz = abt_table.iat[abt_pos,3]
                    cons_val = cons_aware.iat[cons_pos,2]
                    
                   # print(abt_year)
                    
                    for wtp_abt in range(2, 7):  
                        
                        for wtp_cons in range(1, 6):  
                            #print(wtp_val_list.iat[wtp_cons, 0], wtp_val_list.columns[wtp_abt], abt_year)
                           
                             if wtp_val_list.iat[wtp_cons, 0] >= cons_val and wtp_val_list.columns[wtp_abt] >= abt_val:                                                     
                                wtp_val = wtp_val_list.iat[wtp_cons, wtp_abt]                                                 
                                wtp_Row = pd.Series(data={'Land':abt_cou,'Größe':abt_siz,'Sektor': abt_sek, 'Jahr':abt_year, 'WTP':wtp_val})                                
                                wtp_list = wtp_list.append(wtp_Row, ignore_index=True)
                                break
                        else:                                
                             continue
                        break
                        
    wtp_list.to_csv('Data\WTP.txt', header = None, index = None, sep=";", mode="a") 
    return wtp_list    

            
def max_wtp_Calculation(wtp_list):
    
    max_wtp_list = pd.DataFrame(columns=['Land','Größe','Sektor','Jahr', 'maxWTP'])
    
    for wtp_len in range(len(wtp_list)):
        calc_cou = wtp_list.iat[wtp_len,0]
        calc_siz = wtp_list.iat[wtp_len,1]
        calc_sek = wtp_list.iat[wtp_len,2]
        calc_year = wtp_list.iat[wtp_len,3]
      
        for el_len in range(len(el_cost)):
            for i in range(4,13):
                el_cou = el_cost.iat[el_len,0]
                el_siz = el_cost.iat[el_len,3]
                el_sek = el_cost.iat[el_len,1]
                el_year = el_cost.columns[i]
                
                #print("Calculation",calc_cou, calc_siz, calc_sek, calc_year)
                #print("Electricatione", el_cou, el_siz, el_sek, el_year)
                if el_cou == calc_cou and calc_siz == el_siz and calc_sek == el_sek and calc_year == el_year:
                    max_wtp = wtp_list.iat[wtp_len, 4] * el_cost.iat[el_len, i]
                    #print("El",el_year)
                    #print("Cal",calc_year)
                    new_Row = pd.Series(data={'Land':calc_cou,'Größe':calc_siz,'Sektor': calc_sek, 'Jahr':calc_year, 'maxWTP':max_wtp})
                    max_wtp_list = max_wtp_list.append(new_Row, ignore_index = True)
            
    max_wtp_list.to_csv('Data\maxWTP.txt', header = None, index = None, sep=";", mode="a")
    return max_wtp_list            
                  

def derated_wtp_calculation(wtp_list):
    derated_wtp_list = pd.DataFrame(columns=['Land', 'Größe', 'Sektor', 'Jahr', 'Technologie', 'Derated WTP'])
    for der_cou_len in range(len(derating_factors)):
        for der_tec_len in range(1, 6):
            for wtp_len in range(len(wtp_list)):
                
                if wtp_list.at[wtp_len,'Land'] == derating_factors.iat[der_cou_len,0]:
                    der_val= derating_factors.iat[der_cou_len,der_tec_len] * wtp_list.at[wtp_len,'maxWTP']
                    new_Row = pd.Series(data={'Land':wtp_list.at[wtp_len,'Land'], 'Größe':wtp_list.at[wtp_len,'Größe'], 'Sektor':wtp_list.at[wtp_len,'Sektor'], 'Jahr':wtp_list.at[wtp_len,'Jahr'], 'Technologie':derating_factors.columns[der_tec_len], 'Derated WTP':der_val})
                    derated_wtp_list = derated_wtp_list.append(new_Row, ignore_index = True)
    derated_wtp_list.to_csv('Data\deratedWTP.txt', header = None, index = None, sep=";", mode="a")
    return derated_wtp_list


"""

class GoO:
    def __init__(self, origin, technology, date):
        self.origin=origin
        self.technology = technology
        self.date = date
        
    def get_origin(self):
        return self.origin

    def get_technology(self):
        return self.technology
    
    def get_date(self):
        return self.date



def goo_issuance():
    fu_data = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'FU-Data')
    issue_rates = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Issue Rates')
    
    
    issued_goos = pd.DataFrame(columns=["GOO"])
    
    for fu_len in range(len(fu_data)):
        fu_cou = fu_data.iat[fu_len, 1]
        fu_tec=fu_data.iat[fu_len,2]
        for fu_time in range(3, len(fu_data.columns)):
            fu_val = fu_data.iat[fu_len, fu_time]
            fu_year = fu_data.columns[fu_time].year
            for iss_len in range(len(issue_rates)):
                iss_cou = issue_rates.iat[iss_len, 1]
                iss_tec = issue_rates.iat[iss_len,2]
                for iss_time in range(8, len(issue_rates.columns)):
                    iss_val = issue_rates.iat[iss_len, iss_time]
                    iss_year = issue_rates.columns[iss_time]
                    if fu_cou == iss_cou and fu_tec == iss_tec and fu_year == iss_year:
                       for new_goo_len in range(int(iss_val * fu_val * 1000000)): #TWh zu MWh
                           new_goo = GoO(fu_cou, fu_tec, fu_data.columns[fu_time])
                           new_Row = pd.Series(data={'GOO': new_goo})
                           issued_goos = issued_goos.append(new_Row, ignore_index = True)
    issued_goos.to_csv('Data\issuedGOOS.txt', header = None, index = None, sep=";", mode="a")                   
    return issued_goos                   
                       
                       
def goo_availability(issued_goos):
    past_issuance = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Past Issuance Data')
    past_cancellation = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Past Cancellation Data')
    month_num = (2050-2019)*12
    available_goos = pd.DataFrame(columns=["Herkunft", "Technologie", "Zeitpunkt", "Anzahl"])
    
    for timestamp in range(month_num):
        if timestamp <= 12*5: #Erst ab 2025 keine Cancellation basierend auf vergangenen Daten -> Ab dann Annahmen, dass Nachfrageüberschuss besteht
            if timestamp < 12:    
                for past_len in range(len(past_issuance)):
                    past_tec_i = past_issuance.iat[past_len, 2]
                    past_cou_i = past_issuance.iat[past_len, 1]
                    past_tec_c = past_cancellation.iat[past_len, 2]
                    past_cou_c = past_cancellation.iat[past_len, 1]
                    for past_time in range(40, len(past_issuance.columns)):
                        past_time_i = past_issuance.iat[past_len, past_time]
                        past_time_c=past_cancellation.iat[past_len, past_time]
                        if past_tec_i == past_tec_c and past_cou_i == past_cou_c and past_time_c == past_time_i:
                            if past_time < 43: #Shifted Cancellation -> does this make sense here?
                                available_goo_19 = past_issuance.iat[past_len, past_time] + available_goos.loc([past_len-1],["Anzahl"])
                            else:
                                available_goo_19 = past_issuance.iat[past_len, past_time] - past_cancellation.iat[past_len, past_time] + available_goos.loc([past_len-1],["Anzahl"])
                            new_Row = pd.Series(data={'Herkunft':past_cou_i, 'Technologie':past_tec_i, 'Zeitpunkt':past_time_i, 'Anzahl':available_goo_19})
                            available_goos = available_goos.append(new_Row, ignore_index = True)
            else:
                for before_2025 in range(len(issued_goos)):
                    for data_2019 in range(len(available_goos)):
                        bef_cou = issued_goos.loc([before_2025],["Herkunft"])
                        bef_tec = issued_goos.loc([before_2025],["Technologie"])
                        dat_cou = available_goos.loc([data_2019],["Technologie"])
                        dat_tec = available_goos.loc([data_2019],["Technologie"])
                        dat_val = available_goos.loc([data_2019]+12, ["Anzahl"])
                        if bef_cou == dat_cou and bef_tec == dat_tec:
                            bef_val = issued_goos.loc([before_2025],['Anzahl']) + dat_val - available_goos.loc([data_2019], ["Anzahl"]) #NEuer Wert = Neue GoOs + GoOs, die im vorhergehenden Monat aus 2019 vorhanden waren - GoOs, die im gleichen Monat vor einem Jahr herausgegeben wurden 
                            


goo_issuance()






















