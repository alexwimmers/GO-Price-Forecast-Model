import pandas as pd
import numpy as np
#from pandas import Series, DataFrame
from datetime import datetime

# =============================================================================
#  Modell zur Bestimmung von Zahlungsbereitschaft, Nachfrage und Angebot
# =============================================================================
def ausführen():
    df=wtp_Matching_alt()    
    print("wtp matched")
    df2 = max_wtp_Calculation(df)
    print("max wtp calculated")
    df3=derated_wtp_calculation(df2)
    print("Derated test")
    wtp_sorting(df3)
    print("sorted")
    goo_issuance()
    print("Goos issued")
    assume_industry_demand()
    print('demand assumed')
    get_monthly_demand()
    print("ich habe fertig")
    
    
#Funktionen

# =============================================================================
#  Ermittlung der Zahlungsbereitschaften (in Prozent) in Abhängigkeit der Zahlungsfähigkeit und der Konsumentennähe
# =============================================================================
def wtp_Matching():
    abt_table = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v02_aw.xlsx', sheet_name = 'Zahlungsfähigkeit_Bereinigt')
    cons_aware = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v02_aw.xlsx', sheet_name = 'Konsumentennähe')
    wtp_list = abt_table[['Land','Sektor','Größe']].copy()
    wtp_val_list = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v02_aw.xlsx', sheet_name = 'Zahlungsbereitschaften')
    
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
    
def wtp_Matching_alt():
    abt_table = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v02_aw.xlsx', sheet_name = 'Zahlungsfähigkeit')
    cons_aware = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v02_aw.xlsx', sheet_name = 'Konsumentennähe')
    wtp_val_list = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v02_aw.xlsx', sheet_name = 'Zahlungsbereitschaften_ALT')
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
                        
    wtp_list.to_csv('Data\WTP.csv', header = None, index = None, sep=";", mode="a") 
    return wtp_list 
 

# =============================================================================
#  Ermittlung der Zahlungsbereitschaft in €/MWh durch Multiplikation der oben berechneten Werte mit den durchn. Strompreisen (Hier: exkl. VAT) = Preise
# =============================================================================           
def max_wtp_Calculation(wtp_list):
    
    el_cost = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v02_aw.xlsx', sheet_name = 'Strompreise')
   # el_cost = el_cost.drop(columns=['Energiesektor','Kode'])
    max_wtp_list = el_cost.merge(wtp_list, on=['Land','Sektor','Größe'])
    
    for year in range(2008, 2018):
         max_wtp_list[year]=max_wtp_list[year]*max_wtp_list["WTP"]*1000
         
    max_wtp_list.drop('Jahr', axis=1,inplace=True)
    max_wtp_list.drop('WTP', axis = 1,inplace=True)
   
    max_wtp_list.to_csv('Data\maxWTP.csv', index = None, sep=";", mode="a")    
    
    return max_wtp_list            
                  
# =============================================================================
#  Ermittlung der Zahlungsbereitschaften für einzelne Technologie-Herkunft-obminationen von GoOs (Oben nur Maxe Berechnet) [Herkunft noch nicht einbezogen]
# =============================================================================
def derated_wtp_calculation(wtp_list):
    #print('line79')
    derated_wtp_list = pd.DataFrame(columns=['Land', 'Größe', 'Sektor', 'Technologie', 'Derated WTP'])
    derating_factors = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Derating_Factors')
    derated_wtp_list_compl = derating_factors.merge(wtp_list, on='Land')
    #print('line82')
    for t in range(1,7):
        tec = derated_wtp_list_compl.columns[t]
        print(tec)
        derated_wtp_list_tec = derated_wtp_list_compl[['Land','Größe','Sektor',tec,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]]
        derated_wtp_list_tec.to_csv('Data\deratedWTP_tec.txt', index = None, sep=";", mode="a")

        for year in range(2008,2018):      
            derated_wtp_list_tec[year] = derated_wtp_list_tec[year]*derated_wtp_list_tec[tec]                                  
            
        derated_wtp_list_tec.rename(columns={tec : 'Technologie'}, inplace=True)
        derated_wtp_list_tec['Technologie']=tec
        derated_wtp_list=derated_wtp_list.append(derated_wtp_list_tec, ignore_index=True)
    derated_wtp_list.drop_duplicates(subset=['Land','Größe','Sektor','Technologie','Derated WTP'], keep = 'first', inplace = True)    
    derated_wtp_list.to_csv('Data\deratedWTP.csv', index = None, sep=";", mode="a")
    return derated_wtp_list

# =============================================================================
#  GoO Herausgabe i.A. von FU-Daten und vergangenen GO-Herausgabe-Quoten = Angebot
# =============================================================================
def goo_issuance():
    fu_data = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'FU-Data')
    issue_rates = pd.read_excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Issue Rates') 
    merged_data = fu_data.merge(issue_rates, how='left', on=['Land', 'Technologie','Country'])
    merged_data.drop(columns=['Country'])
    issued_goo = merged_data[['Land', 'Technologie']].copy()
    merged_data_sel =  merged_data.iloc[:,0:375]
    
    for year in range(2020,2051):
       for fu_len in range(3,len(merged_data_sel.columns)):
           if merged_data_sel.columns[fu_len].year == year:
               fu_time = merged_data_sel.columns[fu_len]               
               num = merged_data[year]*merged_data_sel[fu_time]*1000000 #TWh zu MWh
               new_goos = pd.DataFrame(data={'Land':merged_data_sel['Land'], 'Technologie': merged_data_sel['Technologie'], fu_time:num})
               issued_goo = issued_goo.merge(new_goos, how='left', on=['Land', 'Technologie'])
    issued_goo.to_csv('Data/issuedGoos.csv', index = None, sep=';', mode='a')
    
    return issued_goo          
      

     

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
# =============================================================================
#  Sortierung der Zahlungsbereitschaften (ggf. nicht notwendig?)
# =============================================================================
def wtp_sorting(derated_wtp):
    derated_wtp['avg'] = derated_wtp.mean(axis=1)
    sorted_wtp = derated_wtp.sort_values('avg', ascending=False)
    for year in range(2008,2018):
        sorted_wtp.drop([year],axis=1, inplace=True)
    sorted_wtp.to_csv('Data\sorted.csv', index = None, sep=";", mode="a")
    return sorted_wtp
    #Durchschnittliche WTP eines Unternehmens eines Sektors eines Landes für eine bestimmte Technologie *pro Jahr* -> Durchschnitt aus 2008-2017


# =============================================================================
#  Annahme des Industriebedarfs
# =============================================================================
def assume_industry_demand():
    ind_dem = pd.read_excel('Data/20200917_Stromverbräuche_v02_aw.xlsx', sheet_name = 'Industrie') #Nachfrage eines Durchschnittsunternehmens!
    ind_no = pd.read_excel('Data/20200917_Stromverbräuche_v02_aw.xlsx', sheet_name = 'Anzahl Unternehmen')
    ind_dev = pd.read_excel('Data/20200917_Stromverbräuche_v02_aw.xlsx', sheet_name = 'Development of industry demand')
    ind_dem_nozero = ind_dem[~(ind_dem==0).any(axis=1)]
    #ind_dem_nozero.to_csv('Data\inddem_1pre.txt', index = None, sep=";", mode="a") 
    merged = pd.merge(ind_dem_nozero,ind_dev, how="left", on=['Sektor'])
  #  ind_dem_assum = pd.DataFrame(columns=["Land","Sektor", "Größe"])
    #merged.to_csv('Data\inddem_pre.txt', index = None, sep=";", mode="a")    
    for year in range(2020, 2051):
        if year == 2020:
            new_Column = pd.DataFrame(data={year: merged[2017]*merged[2020]*1000}) #GWh zu MWh          
            merged[2020] = new_Column[2020]
        else:
            #print(merged[year].head(5))
            #print(merged[year-1].head(5))
            new_Column = pd.DataFrame(data={year: merged[year-1]*merged[year]})        
            merged[year] = new_Column[year]    
    complete_sector = pd.merge(merged, ind_no, how='left', on=['Land', 'Sektor', 'Größe'])    
    for year in range(2020, 2051):
        complete_sector[year] = complete_sector[year]*complete_sector['Anzahl 2017']       
    merged.drop(['Kode', 'Energiesektor', 2017], axis=1, inplace=True)
    merged.to_csv('Data\inddem_einzeln.csv', index = None, sep=";", mode="a")
    complete_sector.to_excel('Data\inddem_complete.xls', sheet_name='industry demand')                   
    return merged 
    #Industry demand per Country & Sektor für 2020-2050        
            
# =============================================================================
#  Zusammenführung der Bedarfsinformationen (Nachfrage) und der Zahlungsbereitschaften = Preis
# =============================================================================
def merge_sorted_wtp_and_demand(sorted_wtp,ind_dem):
    #industry_demand_pc = pd.read_excel('Data/20200917_Stromverbräuche_v01_aw.xlsx', sheet_name = 'Industrie')
    industry_amount = pd.read_excel('Data/20200917_Stromverbräuche_v02_aw.xlsx', sheet_name = 'Anzahl Unternehmen')
    #industry_demand_pc["2017"] = 1000*industry_demand_pc["2017"] #GWh to MWh
    ind_dem_compl= pd.merge(ind_dem, industry_amount, how='left',on=['Land', 'Sektor', 'Größe'])
    
    merged_data=pd.merge(ind_dem_compl,sorted_wtp, how='left',on=['Land', 'Sektor', 'Größe'])
    merged_data.to_csv('Data\merged_wtp_demand.csv', index = None, sep=";", mode="a")                   

    return merged_data

def get_monthly_demand():
    ind_dem = pd.read_excel('Data/inddem_complete.xls', sheet_name='industry demand')
    output = ind_dem[['Land','Sektor','Größe']].copy()
    for year in range(2020,2051):               
        periods = ind_dem[['Land','Sektor','Größe',year]].copy()
        #print(periods)        
        for m in range(0,12):           
            month = datetime(year, m+1, 1).strftime("%d-%m-%y")
            new_Column = pd.DataFrame(data={month: periods[year]/12})
            periods[month] = new_Column
        periods.drop([year],axis=1, inplace=True)
        output = output.merge(periods, how='left',on=['Land','Sektor','Größe'])
    output.to_csv('Data\monthly_demand.csv', index = None, sep=";", mode="a")                
    return output
  

ausführen()