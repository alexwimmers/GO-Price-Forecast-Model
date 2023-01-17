import pandas as pd
import numpy as np
#from pandas import Series, DataFrame
#from datetime import datetime


def ausführen():
    wtp_Matching()
    """
    print("wtp matched")
    df2 = max_wtp_Calculation(df)
    print("max wtp calculated")
    df3=derated_wtp_calculation(df2)
    print("Derated test")
    df4=wtp_sorting(df3)
    print("sorted")
   # goo_issuance()
    #print("Goos issued")
    df5=assume_industry_demand()
    print('demand assumed')
    merge_sorted_wtp_and_demand(df4,df5)
    print("ich habe fertig")
    """
    
#Funktionen
def wtp_Matching():
    abt_table = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw.xlsx', sheet_name = 'Zahlungsfähigkeit_Bereinigt')
    cons_aware = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw.xlsx', sheet_name = 'Konsumentennähe')
    wtp_list = abt_table[['Land','Sektor','Größe']].copy()
    wtp_val_list = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw.xlsx', sheet_name = 'Zahlungsbereitschaften')
    
    abt_table_merged = abt_table.merge(cons_aware, how='left', on=['Sektor', 'Kode'])
    
    print(abt_table_merged.head(5))
    
    for year in range(2008, 2018):
        wtp_ind = abt_table_merged[['Land', 'Sektor','Größe', 'Konsumentennähe', year]]
        print(wtp_ind.head(5))
        wtp_ind.rename(columns={'Konsumentennähe':'kons', year : 'Y_Column'}, inplace=True)
        print(wtp_ind.head(5))
        #print(wtp_ind['Land'])
        #print(wtp_val_list.at[1,'Konsumentennähe'])
        for apt in range(0,5):
            for cons in range(0,5):
        #print(wtp_ind['kons'])                
                if apt*5+cons == 25:                    
                    break
                elif cons == 0:
                    wtp_ind_2 = wtp_ind.loc[(wtp_ind.kons<wtp_val_list.at[1,'Konsumentennähe']), ['Land', 'Sektor','Größe','Y_Column']]                    
                    wtp_ind_3 = wtp_ind_2.loc[(wtp_ind.Y_Column<wtp_val_list.at[apt*5+cons,'Zahlungsbereitschaft']), ['Land', 'Sektor','Größe','Y_Column']]
                    wtp_ind_3.rename(columns={'Y_Column':year}, inplace=True)
                    wtp_ind_3[year]=wtp_val_list.at[apt*5+cons,'Zahlungsbereitschaft']
                    wtp_list = wtp_list.merge(wtp_ind_3, how='left', on=['Land', 'Größe', 'Sektor'])
                else:
                    wtp_ind_2 = wtp_ind.loc[(wtp_ind.kons<wtp_val_list.at[apt*5+cons,'Konsumentennähe'])&(wtp_ind.kons>wtp_val_list.at[(apt*5+cons)-1,'Konsumentennähe']), ['Land', 'Sektor','Größe','Y_Column']]
                    #print(wtp_ind_2.head(5))
                    if apt == 0:
                        wtp_ind_3 = wtp_ind_2.loc[(wtp_ind.Y_Column<wtp_val_list.at[(apt*5+cons),'Zahlungsbereitschaft']), ['Land', 'Sektor','Größe','Y_Column']]
                        #wtp_ind=wtp_ind.loc[wtp_ind[year]<=wtp_val_list.iat[atp,1],['Land', "Sektor",'Größe']]
                    else:
                        wtp_ind_3 = wtp_ind_2.loc[(wtp_ind.Y_Column<wtp_val_list.at[(apt*5+cons),'Zahlungsbereitschaft'])&(wtp_ind.Y_Column>wtp_val_list.at[((apt-1)*5+cons),'Zahlungsbereitschaft']), ['Land', 'Sektor','Größe','Y_Column']]

                    wtp_ind_3.rename(columns={'Y_Column':year}, inplace=True)
                    #print(wtp_ind_3.head(5))
                    #wtp_ind_2.rename(columns={'Y_Column':year}, inplace=True)
                    #wtp_ind_2[year]=wtp_val_list.at[apt*5+cons,'Zahlungsbereitschaft']
                    wtp_ind_3[year]=wtp_val_list.at[apt*5+cons,'Zahlungsbereitschaft']
                    
                    #print('Zweite Runde')
                    #print(wtp_ind_3.head(5))
                    wtp_list = wtp_list.merge(wtp_ind_3, how='left', on=['Land', 'Größe', 'Sektor'])     
                    #wtp_list = pd.concat([wtp_list,wtp_ind_3], axis=1, ignore_index=True)
                    
    for i in range(1,11):
        #print(wtp_list.columns[(len(wtp_list.columns)-i)])
        #print((len(wtp_list.columns)-i))
        wtp_list.columns.values[[(len(wtp_list.columns)-i)]] =[2018-i]
    
    wtp_list.to_csv('Data\wtplist.csv', index = None, sep=";", mode="a")    
    wtp_list_done=wtp_list[['Land', 'Sektor','Größe',2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]].copy()
    wtp_list_done.to_csv('Data\wtplist_done.csv', index = None, sep=";", mode="a")      
    wtp_ind.to_csv('Data\wtpind.csv', index = None, sep=";", mode="a")
    wtp_ind_2.to_csv('Data\wtpind_2.csv', index = None, sep=";", mode="a")
    wtp_ind_3.to_csv('Data\wtpind_3.csv', index = None, sep=";", mode="a")
                 
    #abt_table_merged.to_csv('Data\abttabe.csv', index = None, sep=";", mode="a")
    

            
def max_wtp_Calculation(wtp_list):
    
    el_cost = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v01_aw_KURZ.xlsx', sheet_name = 'Stromkosten')
   # el_cost = el_cost.drop(columns=['Energiesektor','Kode'])
    max_wtp_list = el_cost.merge(wtp_list, on=['Land','Sektor','Größe'])
    
    for year in range(2008, 2018):
         max_wtp_list[year]=max_wtp_list[year]*max_wtp_list["WTP"]
         
    max_wtp_list.drop('Jahr', axis=1,inplace=True)
    max_wtp_list.drop('WTP', axis = 1,inplace=True)
   
    max_wtp_list.to_csv('Data\maxWTP.txt', index = None, sep=";", mode="a")    
    
    return max_wtp_list            
                  

def derated_wtp_calculation(wtp_list):
    #print('line79')
    derated_wtp_list = pd.DataFrame(columns=['Land', 'Größe', 'Sektor', 'Technologie', 'Derated WTP'])
    derating_factors = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Derating_Factors')
    derated_wtp_list_compl = derating_factors.merge(wtp_list, on='Land')
    #print('line82')
    for t in range(1,7):
        tec = derated_wtp_list_compl.columns[t]
       # print(tec)
        derated_wtp_list_tec = derated_wtp_list_compl[['Land','Größe','Sektor',tec,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]]
        #derated_wtp_list_tec.to_csv('Data\deratedWTP_tec.txt', index = None, sep=";", mode="a")

        for year in range(2008,2018):      
            derated_wtp_list_tec[year] = derated_wtp_list_tec[year]*derated_wtp_list_tec[tec]                                  
            #print(derated_wtp_list_tec)
        derated_wtp_list_tec.rename(columns={tec : 'Technologie'}, inplace=True)
        derated_wtp_list_tec['Technologie']=tec
        #derated_wtp_list_tec.to_csv('Data\deratedWTP_tec2.txt', index = None, sep=";", mode="a")                
        derated_wtp_list=derated_wtp_list.append(derated_wtp_list_tec, ignore_index=True)
        
    derated_wtp_list.to_csv('Data\deratedWTP.txt', index = None, sep=";", mode="a")
    return derated_wtp_list




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



def getGoovalues(goo):
    origin = goo.get_origin()
    tec = goo.get_technology()
    date = goo.get_date()
    return origin + tec + str(date)
    #print(origin, tec, date)


def goo_issuance():
    fu_data = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'FU-Data')
    issue_rates = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Issue Rates')
       
    
    
    merged_data = fu_data.merge(issue_rates, how='left', on=['Land', 'Technologie'])
    #merged_data.drop(columns=['Country'])
    issued_goo = merged_data[['Land', 'Technologie']].copy()
    issue_len = len(issue_rates.columns)
    columns_list = merged_data.columns.values.tolist()
    print(columns_list.values.year)
    #for year in range(2020,2051):
    #    columns_list = merged_data.columns.values.tolist().year
     #   new_goos = np.where(merged_data.columns[:].year == year, merged_data.columns)
        
goo_issuance()       
'''
    for fu_len in range(len(fu_data)):
        fu_cou = fu_data.iat[fu_len, 1]
        fu_tec=fu_data.iat[fu_len,2]
      #  print("30")
        for iss_len in range(len(issue_rates)):
            iss_cou = issue_rates.iat[iss_len, 1]
            iss_tec = issue_rates.iat[iss_len,2]
            if fu_cou == iss_cou and fu_tec == iss_tec:
                for fu_time in range(3, len(fu_data.columns)):
                    fu_val = fu_data.iat[fu_len, fu_time]
                    fu_year = fu_data.columns[fu_time].year
             #       print("38")            
                    for iss_time in range(8, len(issue_rates.columns)):
                        iss_val = issue_rates.iat[iss_len, iss_time]
                        iss_year = issue_rates.columns[iss_time]
                       # print("42")
                      #  print(iss_cou, iss_tec, fu_cou, fu_tec)
                        if iss_year == fu_year:
                            new_goo = GoO(fu_cou, fu_tec, fu_data.columns[fu_time])
                            num = int(iss_val * fu_val * 1000000) #TWh zu MWh
                            
                            new_Row = pd.Series(data={'GOO': new_goo, 'Anzahl':num})
                            #print("47")
                            issued_goos = issued_goos.append(new_Row, ignore_index = True)                            
                            #x = issued_goos.loc([new_goo_len])
                            #getGoovalues(x)
    issued_goos.to_csv('Data\issuedGOOS.txt', index = None, sep=";", mode="a")                   
    return issued_goos                   
'''

def findGoo(goolist, ori, tec, date):
     
     o = ori
     t = tec
     d = date
     search = GoO(o, t, d)
     for i in range(len(goolist)):
         x = getGoovalues(goolist.iat[i,0])
         #print(x)
         if x == getGoovalues(search):
            return i
     #print(goolist.query('goolist.GOO == search'))
     #print(goolist[goolist['GOO']==search]['Anzahl'])
     

#Vergangene Daten werden erstmal nicht berücksichtigt. Das heißt interessant wird es ab 2025
'''def goo_availability(goo_list):
    available_goos = pd.DataFrame(columns=['Goo','Anzahl'])
    country_tec_combi = pd.read_Excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Land_Tec_Kombinationen')
    issuance_2019 = pd.read_Excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Past Cancellation Data')
    cancellation_2019 = pd.read_Excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Past Issuance Data')
    for goo_range in range(len(goo_list)):
        for cou_tec_num in range(len(country_tec_combi)):
            combi_cou = country_tec_combi.iat[cou_tec_num,0]
            combi_tec = country_tec_combi.iat[cou_tec_num, 1]
            for d in range(2020,2025):
                for m in range(1,13):
                    date = datetime(d, m, 1)
                    location_in_goo_list = findGoo(goo_list, combi_cou, combi_tec, date)
'''                        

def wtp_sorting(derated_wtp):
    derated_wtp['avg'] = derated_wtp.mean(axis=1)
    sorted_wtp = derated_wtp.sort_values('avg', ascending=False)
    for year in range(2008,2018):
        sorted_wtp.drop([year],axis=1, inplace=True)
    sorted_wtp.to_csv('Data\sorted.txt', index = None, sep=";", mode="a")
    return sorted_wtp
    #Durchschnittliche WTP eines Unternehmens eines Sektors eines Landes für eine bestimmte Technologie *pro Jahr* -> Durchschnitt aus 2008-2017

def assume_industry_demand():
    ind_dem = pd.read_excel('Data/20200917_Stromverbräuche_v01_aw.xlsx', sheet_name = 'Industrie')
    ind_dev = pd.read_excel('Data/20200917_Stromverbräuche_v01_aw.xlsx', sheet_name = 'Development of industry demand')
    ind_dem_nozero = ind_dem[~(ind_dem==0).any(axis=1)]
    ind_dem_nozero.to_csv('Data\inddem_1pre.txt', index = None, sep=";", mode="a") 
    merged = pd.merge(ind_dem_nozero,ind_dev, how="left", on=['Sektor'])
  #  ind_dem_assum = pd.DataFrame(columns=["Land","Sektor", "Größe"])
    merged.to_csv('Data\inddem_pre.txt', index = None, sep=";", mode="a")    
    for year in range(2020, 2051):
        if year == 2020:
            new_Column = pd.DataFrame(data={year: merged[2017]*merged[2020]*1000})           
            merged[2020] = new_Column[2020]
        else:
           new_Column = pd.DataFrame(data={year: merged[year-1]*merged[year]*1000})           
           merged[year] = new_Column[year]
    merged.drop(['Kode', 'Energiesektor', 2017], axis=1, inplace=True)
    merged.to_csv('Data\inddem.txt', index = None, sep=";", mode="a")                   
    return merged 
    #Industry demand per Country & Sektor für 2020-2050        
            

def merge_sorted_wtp_and_demand(sorted_wtp,ind_dem):
    #industry_demand_pc = pd.read_excel('Data/20200917_Stromverbräuche_v01_aw.xlsx', sheet_name = 'Industrie')
    industry_amount = pd.read_excel('Data/20200917_Stromverbräuche_v01_aw.xlsx', sheet_name = 'Anzahl Unternehmen')
    #industry_demand_pc["2017"] = 1000*industry_demand_pc["2017"] #GWh to MWh
    ind_dem_compl= pd.merge(ind_dem, industry_amount, how='left',on=['Land', 'Sektor', 'Größe'])
    
    merged_data=pd.merge(ind_dem_compl,sorted_wtp, how='left',on=['Land', 'Sektor', 'Größe'])
    merged_data.to_csv('Data\merged.txt', index = None, sep=";", mode="a")                   

    return merged_data

#ausführen()


