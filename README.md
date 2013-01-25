easy-stats-113
==============

Data from the census bureau's "easy stats" site--the first available on the 113th Congress. 

The data in this file comes from the census bureau's [easy stats page](http://www.census.gov/easystats/) on the redistricted 113th Congress. Because the site--on the date of it's launch--didn't have a bulk file this information was gathered by making API calls--see get_data.py. 

The variables in this file are the ones that appear on the site--MOE means "margin of error". For readibility, the category has been prepended to the variable name. 

Variables available
-----------------

These are the variables available. Each variable also comes with a margin of error estimate.

	Population	
		Total Population
		
	Sex
		Total Population	
		Male	
		Female	
	
	Age	
		Total Population	
		Under 5 years	
		5 to 9 years	
		10 to 14 years	
		15 to 19 years	
		20 to 24 years	
		25 to 34 years	
		35 to 44 years	
		45 to 54 years	
		55 to 59 years	
		60 to 64 years	
		65 years and over	
		
	Race
		Total Population	
		One Race	
		White	
		Black or African American	
		American Indian and Alaska Native	
		Asian	
		Native Hawaiian and Other Pacific Islander
		Some Other Race	
		Two or More Races	
	
	Hispanic or Latino Origin
		Total Population	
		Hispanic or Latino (of any race)	
		Not Hispanic or Latino	
	
	Income (In 2011 Inflation-Adjusted Dollars)
		Median Household Income
	
	Housing Occupancy
		Total Housing Units	
		Occupied Housing Units	
		Vacant Housing Units
		
	Housing Tenure
		Occupied Housing Units	
		Owner-Occupied Housing Units	
		Renter-Occupied Housing Units	
	
	Educational Attainment
		Population 25 Years and Over	
		Less than 9th Grade	
		9th to 12th Grade, No Diploma	
		High School Graduate (Includes Equivalency)	
		Some College, No Degree	
		Associate's Degree	
		Bachelor's Degree	
		Graduate or Professional Degree	
		Percent High School Graduate or Higher
		Percent Bachelor's Degree or Higher

	Veteran Status
		Civilian Population 18 Years and Over	
		Civilian Veterans	

