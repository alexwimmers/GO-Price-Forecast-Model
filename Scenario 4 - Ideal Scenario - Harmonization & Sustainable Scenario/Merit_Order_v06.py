import pandas as pd
import csv
from datetime import datetime


wtps = pd.read_csv('Data\sorted.csv', delimiter=';')
demand = pd.read_csv('Data\complete_demand.csv', delimiter=';')
supply = pd.read_csv('Data\issuedGoos.csv', delimiter=';')
country_list = pd.read_excel('Data/20201020_Input_Data.xlsx',sheet_name="Countries")
#price_list = '.\\Data\\sorted_test.csv'
sector_list = pd.read_excel('Data/20201020_Input_Data.xlsx',sheet_name="Sectors")
size_list = pd.read_excel('Data/20201020_Input_Data.xlsx',sheet_name="Sizes")
tec_list = pd.read_excel('Data/20201020_Input_Data.xlsx',sheet_name="Technologies")
origin_list=pd.read_excel('Data/20201020_Input_Data.xlsx',sheet_name="Origins")
lcoe_list = pd.read_excel('Data/20201020_Input_Data.xlsx',sheet_name="LCOE")
dates = ['2020-01-01','2030-12-01']

def define_periods_m(dates):
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    periods = []
    for tot_m in range(total_months(start)-1, total_months(end)):
        y, m = divmod(tot_m, 12)
        periods.append(datetime(y, m+1, 1).strftime("%b-%y"))
    return periods

def define_periods_y():
    periods = []
    for i in range(2020,2041):
        periods.append(i)
    return periods

def wtp_to_dict():
    wtp_dict={}
    for i in range(len(wtps)):
        wtp_dict[wtps.loc[i,'Land'],wtps.loc[i,'Sektor'],wtps.loc[i,'Größe'],wtps.loc[i,'Technologie']]=wtps.loc[i,'avg']
    #print(wtp_dict)
    return wtp_dict

def demand_to_dict(p):
    demand_dict={}
    for i in range(len(demand)):
        j=3
        for t in p:            
            demand_dict[demand.loc[i,'Land'],demand.loc[i,'Sektor'],demand.loc[i,'Größe'],t] = demand.iat[i,j]
            j+=1
        if i > 13192:
            break    
    #print(demand_dict)
    return demand_dict

def supply_to_dict(p):
    supply_dict={}
    for i in range(len(supply)):
        j = 2
        for t in p:
            supply_dict[supply.loc[i,'Land'],supply.loc[i,'Technologie'],t] = supply.iat[i,j]
            j +=1
    #print(supply_dict)
    return supply_dict

def read_countries(country_list,wtps):
    countries={}
    sorted_countries = wtps.merge(country_list, how='inner', on="Land")
    sorted_countries = sorted_countries['Land']
    sorted_countries = sorted_countries.drop_duplicates()    
    for i in range(len(sorted_countries)):
        countries[i]=sorted_countries.iloc[i]
    #print(countries)
    return countries

def read_sectors(sector_list,wtps):
    sectors={}
    sorted_sectors = wtps.merge(sector_list, how='inner', on="Sektor")
    sorted_sectors = sorted_sectors['Sektor']
    sorted_sectors = sorted_sectors.drop_duplicates()
    for i in range(len(sorted_sectors)):
        sectors[i]=sorted_sectors.iloc[i]
    #print(sectors)
    return sectors


def read_sizes(sizes_list,wtps):
    sizes={}
    sorted_sizes = wtps.merge(size_list, how='inner', on="Größe")
    sorted_sizes = sorted_sizes['Größe']
    sorted_sizes = sorted_sizes.drop_duplicates()
    for i in range(len(sorted_sizes)):
        sizes[i]=sorted_sizes.iloc[i]
    #print(sizes)      
    return sizes

def read_technologies(tec_list,wtps):
    technologies={}
    sorted_tec = wtps.merge(tec_list, how='inner', on="Technologie")
    sorted_tec = sorted_tec['Technologie']
    sorted_tec = sorted_tec.drop_duplicates()
    for i in range(len(sorted_tec)):
        technologies[i]=sorted_tec.iloc[i]
    #print(technologies) 
    return technologies

def read_origins(origin_list,wtps):
    origins={}
    sorted_tec = wtps.merge(origin_list, how='inner', on="Herkunft")
    sorted_tec = sorted_tec['Herkunft']
    sorted_tec = sorted_tec.drop_duplicates()
    for i in range(len(sorted_tec)):
        origins[i]=sorted_tec.iloc[i]
    #print(origins) 
    return origins

def read_lcoe(lcoe_list):
    lcoe = {}
    for i in range(len(lcoe_list)):        
        for p in range(2020,2041):
            if i == 0:
                lcoe[p] = lcoe_list.loc[i,p]
            else:
                if lcoe[p] > lcoe_list.loc[i,p]:
                    lcoe[p] = lcoe_list.loc[i,p]
    #print(lcoe)
    return lcoe

def merit_order(dem, sup, tec, cou, sec, siz,ori, per,wtps,lcoe):
    prices = {}
    #Initialize Price Dictionary
    for t in tec:
        for p in per:
            for o in ori:
                prices[tec[t],ori[o],p] = 100000   #Set maximum prices
    
              
    for p in per:
        for i in range(len(wtps)):
            

            wtp_val = wtps.loc[i,'avg']*0.15
            try:
                #print(wtps.loc[i,'Land']+wtps.loc[i,'Sektor']+wtps.loc[i,'Größe']+str(p))
                dem_val = float(dem[wtps.loc[i,'Land'],wtps.loc[i,'Sektor'],wtps.loc[i,'Größe'],p])
                #print(dem_val)
                sup_val = float(sup[wtps.loc[i,'Herkunft'],wtps.loc[i,'Technologie'],p])
                #print(sup_val)
                #print(prices[wtps.loc[i,'Technologie'],wtps.loc[i,'Herkunft'], p])
                if sup_val > 0: #Prices can change only when there is supply
                    new_sup = sup_val - dem_val
                    if new_sup < 0: #Check if demand exceeds supply
                        dem[wtps.loc[i,'Land'],wtps.loc[i,'Sektor'],wtps.loc[i,'Größe'],p] = new_sup * (-1) #If so, new demand is set
                        new_sup = 0
                    else:
                        dem[wtps.loc[i,'Land'],wtps.loc[i,'Sektor'],wtps.loc[i,'Größe'],p] = 0 #If demand can be satisfied, set to 0
                    sup[wtps.loc[i,'Herkunft'],wtps.loc[i,'Technologie'],p] = new_sup

                    if float(prices[wtps.loc[i,'Technologie'],wtps.loc[i,'Herkunft'], p]) > wtp_val: #Da WTP sortiert ist nach Größe, kann der Preis nur größer sein!
                        prices[wtps.loc[i,'Technologie'],wtps.loc[i,'Herkunft'], p] = wtp_val
            except KeyError:
                pass
                #print('KeyError bei'+"_"+wtps.loc[i,'Land']+"_"+wtps.loc[i,'Sektor']+"_"+wtps.loc[i,'Größe']+"_"+wtps.loc[i,'Technologie']+"_"+str(p))
        #with open('.\\Data\\Prices_'+str(p)+'.csv', 'w') as csv_file:  
        #    writer = csv.writer(csv_file)
         #   for key, value in prices.items():
         #       writer.writerow([key, value])
    
    for p in per: 
        for t in tec:
            for o in ori:
                try:
                    if prices[tec[t],ori[o],p] > lcoe[p]: #and p > 2024:
                        prices[tec[t],ori[o],p] = lcoe[p]
                except KeyError:
                    pass
    return prices, dem, sup

def ausfuehren():
    per = define_periods_y()
    print("per")
    dem = demand_to_dict(per)
    print("dem")
    '''with open('.\\Data\\De.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in dem.items():
            writer.writerow([key, value])'''
    sup = supply_to_dict(per)
    print("sup")
    #wtp = wtp_to_dict()
    print("wtp")
    tec = read_technologies(tec_list,wtps)
    print("tec")
    sec = read_sectors(sector_list,wtps)
    print("sec")
    siz = read_sizes(size_list,wtps)
    print("siz")
    cou = read_countries(country_list,wtps)
    print("cou")
    ori = read_origins(origin_list, wtps)
    print('ori')
    lcoe = read_lcoe(lcoe_list)
    print("All data loaded")
    prices, dem_rem, sup_rem = merit_order(dem,sup,tec,cou,sec,siz,ori,per,wtps,lcoe)
    '''with open('.\\Data\\Remaining Demand.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in dem_rem.items():
            writer.writerow([key, value])        
    with open('.\\Data\\Remaining Supply.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in sup_rem.items():
            writer.writerow([key, value])
    with open('.\\Data\\Prices.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in prices.items():
            writer.writerow([key, value])'''
    price_DF = pd.DataFrame(prices.items())
    demand_df = pd.DataFrame(dem_rem.items())
    supply_df = pd.DataFrame(sup_rem.items())
    price_DF.to_excel('Data/price_DF.xls', sheet_name='Prices')
    demand_df.to_csv('Data/demand_df.csv', index = None, sep=";", mode="a")
    supply_df.to_csv('Data/supply_df.csv', index = None, sep=";", mode="a")

















       
