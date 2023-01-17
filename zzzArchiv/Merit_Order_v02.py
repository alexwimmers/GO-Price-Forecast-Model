import pandas as pd
import csv
from datetime import datetime


wtps = pd.read_csv('Data\sorted.csv', delimiter=';')
demand = pd.read_csv('Data\monthly_demand.csv', delimiter=';')
supply = pd.read_csv('Data\issuedGoos.csv', delimiter=';')
country_list = '.\\Data\\Countries.csv'
#price_list = '.\\Data\\sorted_test.csv'
sector_list = '.\\Data\\Sectors.csv'
size_list = '.\\Data\\Sizes.csv'
tec_list = '.\\Data\\Technologies.csv'
dates = ['2020-01-01','2050-12-01']

def define_periods(dates):
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    periods = []
    for tot_m in range(total_months(start)-1, total_months(end)):
        y, m = divmod(tot_m, 12)
        periods.append(datetime(y, m+1, 1).strftime("%b-%y"))
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
            demand_dict[demand.loc[i,'Land'],demand.loc[i,'Sektor'],demand.loc[i,'Größe'],str(t)] = demand.iat[i,j]
            j+=1
        if i > 54:
            break    
    #print(demand_dict)
    return demand_dict

def supply_to_dict(p):
    supply_dict={}
    for i in range(len(supply)):
        j = 2
        for t in p:
            supply_dict[supply.loc[i,'Technologie'],str(t)] = supply.iat[i,j]
            j +=1
    #print(supply_dict)
    return supply_dict

def read_countries(country_list):
    countries={}
    with open(country_list, encoding = 'iso-8859-1') as country:
        country_reader = csv.reader(country, delimiter=';')
        next(country_reader)
        i=0             
        for line in country_reader:
          countries[i]=(line[0])     
          i +=1
    #print(countries)
    return countries

def read_sectors(sector_list):
    sectors={}
    with open(sector_list, encoding = 'iso-8859-1') as sector:
        sector_reader = csv.reader(sector, delimiter=';')
        next(sector_reader)
        i=0             
        for line in sector_reader:
          sectors[i]=(line[0])     
          i +=1
    #print(sectors)
    return sectors


def read_sizes(sizes_list):
    sizes={}
    with open(sizes_list, encoding = 'iso-8859-1') as size:
        size_reader = csv.reader(size, delimiter=';')
        next(size_reader)
        i=0             
        for line in size_reader:
          sizes[i]=(line[0])     
          i +=1
    #print(sizes)      
    return sizes

def read_technologies(tec_list):
    technologies={}
    with open(tec_list, encoding = 'iso-8859-1') as technology:
        tec_reader = csv.reader(technology, delimiter=';')
        next(tec_reader)
        i=0             
        for line in tec_reader:
          technologies[i]=(line[0])     
          i +=1
    #print(technologies)
    return technologies

def merit_order(dem, sup, wtp, tec, cou, sec, siz, per):
    prices = {}
    #Initialize Price List
    for t in tec:
        for p in per:
            prices[tec[t],str(p)] = 100000            
    for c in cou:
        for s in sec:
            for g in siz:
                for t in tec:
                    try:                    
                        wtp_val = wtp[(cou[c],sec[s],siz[g],tec[t])]
                        #print(wtp_val)
                        for p in per:
                            #print(p)
                            #while(dem[cou[c],sec[s],siz[g],str(p)]!=0):
                            dem_val = float(dem[cou[c],sec[s],siz[g],p])
                            sup_val = float(sup[tec[t],p])
                            if sup_val > 0:
                                new_sup = sup_val - dem_val
                                if new_sup < 0:
                                    dem[cou[c],sec[s],siz[g],str(p)] = (-1)*new_sup
                                else:
                                    dem[cou[c],sec[s],siz[g],str(p)] = 0
                                sup[tec[t],str(p)]= new_sup                     
                            if prices[tec[t],str(p)] > wtp_val:
                                prices[tec[t],str(p)]=wtp_val
                    except KeyError:
                        pass
    
    return prices, dem, sup

def ausfuehren():
    per = define_periods(dates)
    dem = demand_to_dict(per)
    #print(dem)
    sup = supply_to_dict(per)
    wtp = wtp_to_dict()
    tec = read_technologies(tec_list)
    sec = read_sectors(sector_list)
    siz = read_sizes(size_list)
    cou = read_countries(country_list)
    prices, dem_rem, sup_dem = merit_order(dem,sup,wtp,tec,cou,sec,siz,per)
    with open('.\\Data\\Prices.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in prices.items():
            writer.writerow([key, value])
    with open('.\\Data\\Remaining Demand.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in dem_rem.items():
            writer.writerow([key, value])        
    with open('.\\Data\\Remaining Supply.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in sup_dem.items():
            writer.writerow([key, value])        
ausfuehren()





























       
