import requests
import urllib, urllib2
from time import sleep
import us
import json
import csv
from time import sleep 


headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'

top_level = [
    "Income (In 2011 Inflation-Adjusted Dollars)",
    "Housing Occupancy",
    "Age",
    "Veteran Status",
    "Sex",
    "Educational Attainment",
    "Race",
    "Hispanic or Latino Origin",
    "Housing Tenure",
    "Population"
]
structure = {
    "Income (In 2011 Inflation-Adjusted Dollars)":["Median Household Income","Median Household IncomeMOE"],
    "Housing Occupancy":["Occupied Housing UnitsMOE","Vacant Housing UnitsMOE","Vacant Housing Units","Total Housing Units","Occupied Housing Units","Total Housing UnitsMOE"],
    "Age":["Total Population","55 to 59 yearsMOE","65 years and overMOE","20 to 24 years","25 to 34 yearsMOE","55 to 59 years","5 to 9 years","60 to 64 yearsMOE","45 to 54 years","15 to 19 yearsMOE","45 to 54 yearsMOE","20 to 24 yearsMOE","60 to 64 years","65 years and over","10 to 14 years","25 to 34 years","15 to 19 years","35 to 44 yearsMOE","Under 5 yearsMOE","5 to 9 yearsMOE","10 to 14 yearsMOE","Total PopulationMOE","Under 5 years","35 to 44 years"],
    "Veteran Status":["Civilian VeteransMOE","Civilian Veterans","Civilian Population 18 Years and Over","Civilian Population 18 Years and OverMOE"],
    "Sex":["Total Population","FemaleMOE","Total PopulationMOE","Female","Male","MaleMOE"],
    "Educational Attainment":["Percent High School Graduate or Higher","Some College, No DegreeMOE","Percent Bachelor's Degree or HigherMOE","Population 25 Years and Over","Percent Bachelor's Degree or Higher","Graduate or Professional DegreeMOE","Bachelor's Degree","Less than 9th Grade","Population 25 Years and OverMOE","9th to 12th Grade, No Diploma","Some College, No Degree","Bachelor's DegreeMOE","Less than 9th GradeMOE","High School Graduate (Includes Equivalency)MOE","Associate's Degree","Associate's DegreeMOE","High School Graduate (Includes Equivalency)","9th to 12th Grade, No DiplomaMOE","Percent High School Graduate or HigherMOE","Graduate or Professional Degree"],
    "Race":["Native Hawaiian and Other Pacific IslanderMOE","Native Hawaiian and Other Pacific Islander","Total Population","AsianMOE","Some Other RaceMOE","Black or African AmericanMOE","American Indian and Alaska NativeMOE","Two or More RacesMOE","Total PopulationMOE","WhiteMOE","Black or African American","Asian","One RaceMOE","White","One Race","American Indian and Alaska Native","Some Other Race","Two or More Races"],
    "Hispanic or Latino Origin":["Total Population","Not Hispanic or Latino","Total PopulationMOE","Not Hispanic or LatinoMOE","Hispanic or Latino (of any race)MOE","Hispanic or Latino (of any race)"],
    "Housing Tenure":["Renter-Occupied Housing UnitsMOE","Occupied Housing UnitsMOE","Owner-Occupied Housing UnitsMOE","Renter-Occupied Housing Units","Occupied Housing Units","Owner-Occupied Housing Units"],
    "Population":["Total Population","Total PopulationMOE"]
    }

def get_page(state_fips, district):
    # for single district states, the only district is "00"
    # if there are multiple districs, it starts at 1. 
    call='get_data'
    geo='{"state_fips":"' + state_fips + '","geography":"CONGRESSIONAL_DISTRICT","secondary_geo":"' + district + '"}'
    table_id='99'

    params = {'call':call,'geo':geo,'table_id':table_id}
    url = "http://www.census.gov/cnmp/easystats/bin/functs_API.php"

    #test_page = slurp(url, params)
    encoded_params = urllib.urlencode(params)
    #print "params are: " + encoded_params
    fixed_url = "%s?%s" % (url, encoded_params)
    #print "call is %s" % (fixed_url)

    response = urllib2.urlopen(fixed_url)
    html = response.read()
    #print "Response is: " + html
    return html

def read_api_page(json_read):
    rowdata = {}
    for a in top_level:
        #print a
        top_level_data = json_read[a]
        child_data_keys = structure[a]
        child_data_keys.sort()
        #print top_level_data
        for child_data_key in child_data_keys:
            keyname = a + ":" + child_data_key
            keyname = keyname.replace(",","")    
            #print keyname
            #print top_level_data[child_data_key]['value']
            rowdata[keyname]= top_level_data[child_data_key]['value']
            
    return rowdata

def run_scrape():
    
    dumpfilename = "easy_stats_113.csv"
    outfile = open(dumpfilename, 'w')
    
    headers = ['state', 'fips', 'district']
    for a in top_level:
        child_data_keys = structure[a]
        child_data_keys.sort()
        for child_data_key in child_data_keys:
            keyname = a + ":" + child_data_key
            keyname = keyname.replace(",","")
            headers.append(keyname)

    header_row = ",".join(headers)
    outfile.write(header_row + "\n")
    
    csvwriter = csv.DictWriter(outfile, headers, restval='', extrasaction='ignore')
    
    for state in us.states.STATES:
        fips = state.fips
        name = state.name
        print "Starting %s fips=%s" % (name, fips)
        
        # first look for a 00th district
        district = '00'
        result = get_page(fips, district)
    
        if result:
            print "At large state!"
            json_read = json.loads(result)
            rowdata = read_api_page(json_read)
            rowdata['state']=state
            rowdata['fips']=fips
            rowdata['district']=district
            csvwriter.writerow(rowdata)
        else:
            print "not an at-large state--looking for districts"
            has_next=True
            district_num=0
            while(has_next):
                district_num += 1
                dist = str(district_num).zfill(2)
                result = get_page(fips, dist)
                if result:
                    json_read = json.loads(result)
                    rowdata = read_api_page(json_read)
                    rowdata['state']=state
                    rowdata['fips']=fips
                    rowdata['district']=dist
                    csvwriter.writerow(rowdata)
                    print "writing district: %s" % dist
                    sleep(1)
                else:
                    has_next = False
                    print "done with state: %s" % state
                

run_scrape()     
