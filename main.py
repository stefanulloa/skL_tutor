#from tutorial: https://www.dataquest.io/blog/pandas-python-tutorial/
# %%
import pandas as pd
import matplotlib.pyplot as plt

import math
import numpy as np

def pandasPart1():
    
    #read data on DataFrame type
    reviews = pd.read_csv(".\data\ign.csv")
    #shape of dataframe
    shape = reviews.shape
    #obtain certain rows and/or columns using iloc method (by position)
    reviews = reviews.iloc[:,1:]

    #obtain certain rows and/or columns using loc method (by label)
    reviewst2 = reviews.loc[0:4,"score"]
    reviewst3 = reviews.loc[0:4,["score","release_year"]]

    #obtain certain rows and/or columns (by label)
    #this is of type Series
    reviewst4 = reviews[["url", "release_day"]]

    #series type
    seriesTest1 = pd.Series([1,2])
    seriesTest2 = pd.Series(["juan","mario"])

    #making a dataframe from two series
    dftest1 = pd.DataFrame([seriesTest1,seriesTest2])

    #making a dataframe from scratch
    dftest2 = pd.DataFrame(
        [
            [1,2],
            ["juan","mario"]
        ],
        index=["row1","row2"],
        columns=["col1","col2"]
    )

    #making dataframe like dic
    dftest3 = pd.DataFrame(
        {
            "col1": [1,"juan"],
            "col2": [2,"mario"]
        }
    )

    #head can also be used for series type
    seriesTest3 = reviews["title"].head()

    #mean for direct mean calculation on column
    meanscore = reviews["score"].mean()

    #finds all numerical columns and computes mean for each
    allmeansCol = reviews.mean()

    #finds all numerical values on each row and computes mean for each
    allmeansRow = reviews.mean(axis=1)

    #corr computes correlation between numerical columns
    #corrtest = reviews.corr()
    #other methods: max, min, count, std, median
    maxtest = reviews.max()
    counttest = reviews.count()

    #math operations on series type
    #other operations: +, -, *, ^
    dividetest = reviews["score"] / 2

    #boolean filter
    booleantestFilter = reviews["score"] > 7

    filteredReview = reviews[booleantestFilter]

    #boolean filter with more conditions
    booleantestFilter2 = (reviews["score"] > 7) & (reviews["platform"]=="Xbox One")

    filteredReview2 = reviews[booleantestFilter2]

    #check histograms on column on condition to make visual comparisons
    reviews[reviews["platform"]=="Xbox One"]["score"].plot(kind="hist")
    reviews[reviews["platform"]=="PlayStation 4"]["score"].plot(kind="hist")


def pandasPart2():

    #scaping because \t produces error
    polling = pd.read_csv(".\\data\\thanksgiving-2015-poll-data.csv")

    #output only the different possible values for a given column
    uniqueValuesOfColumns = polling["Do you celebrate Thanksgiving?"].unique()

    #get the name of columns by position
    someColumnNames = polling.columns[50:]

    ##FUNCTIONS##

    #check how many values there of the unique values for a given column
    #dropna also counts nan values
    countValuesOfColumn = polling["What is your gender?"].value_counts(dropna=False)

    #apply transformation method to each row individually
    #new column added
    polling["new_gender"] = polling["What is your gender?"].apply(fromGenderToNumeric)
    #count values after transformation
    countValuesOfNGenderCol = polling["new_gender"].value_counts(dropna=False)

    #apply a lambda operation with apply. it will work on clumns by default
    #to work on row level, use axis=1 as argument
    #dtype will output the type of each column
    lambdaoperation = polling.apply(lambda x: x.dtype).head()

    #check unique values for given column
    moneyOfHouseholdLastYear = polling["How much total combined money did all members of your HOUSEHOLD earn last year?"].value_counts(dropna=False)

    #apply transformation on income and create new column
    polling["newIncomeCol"] = polling["How much total combined money did all members of your HOUSEHOLD earn last year?"].apply(clean_income)
    
    ##GROUPING##

    #check (and count) unique value of type of sauce column
    countValuesOnSauceCol = polling["What type of cranberry saucedo you typically have?"].value_counts()
    
    #new dataframes on condition of type of sauce
    homemade = polling[polling["What type of cranberry saucedo you typically have?"] == "Homemade"]
    canned = polling[polling["What type of cranberry saucedo you typically have?"] == "Canned"]
    #mean for each type of sauce
    meanHomemade = homemade["newIncomeCol"].mean()
    meanCanned = canned["newIncomeCol"].mean()

    #instead of the previous process, we can directly make groups of dataframes depending on sauce
    grouped = polling.groupby("What type of cranberry saucedo you typically have?")
    #to check set of row indices for each sauce case
    setOnSauceGroups = grouped.groups
    #how many rows for each group
    countRowsOnSauceGroups = grouped.size()

    #get info of groups
    for name, group in grouped:
        print(name,group.shape,type(group))

    #create groups of series (each series depeds on the sauce type)
    incomeOnSauceGroups = grouped["newIncomeCol"]

    ##AGREGATION##
    #IMPORTANT: agg() only works for functions that return one value, if it returns more we have to use apply()
    #agg() lets use many functions at the same time, apply() does not

    #agg applies the same function to a group of series in parallel
    avgForSauceGroupSeries = grouped["newIncomeCol"].agg(np.mean)

    #if no column specified, agg will perform on every column
    #in this case, mean only works on data with numeric values
    avgForSauceGroupDataFrames = grouped.agg(np.mean)
    #to visually compare
    avgForSauceGroupSeries.plot(kind="bar")

    #groups using two columns for groupby
    grouped2 = polling.groupby(["What type of cranberry saucedo you typically have?","What is typically the main dish at your Thanksgiving dinner?"])
    #mean depending on combinations of two types (from the two columns)
    meanGroups2Col = grouped2.agg(np.mean)

    #calculate mean, sum and std on income column for the grouped object
    operationsGroups2Col = grouped2["newIncomeCol"].agg([np.mean, np.sum, np.std])
    
    #apply is a different way of using methods on groups
    #we get groups by type of location, from those we choose just the dishes column for each group
    grouped3 = polling.groupby("How would you describe where you live?")["What is typically the main dish at your Thanksgiving dinner?"]
    #we will count every instance
    #because value_counts returns 2 or more values, we cannot use agg()
    #so we have to use apply which will combine the results
    countGroup3 = grouped3.apply(lambda x:x.value_counts())


#method transforms string values to 0 (male) or 1 (female), nan is the same
#each row will be applied this method individually
def fromGenderToNumeric(genderString):
    #isnan only works on numeric values, so we need to check first the type is float (nan is float)
    if isinstance(genderString, float):
        if math.isnan(genderString):
            return genderString
    #in case it is female, casting comparison to int transforms to 1. for male, it is 0
    return int(genderString == "Female")

#if 200000 on upwards: 200000
#if prefer not to answer or nan: nan
#if range: avg
def clean_income(value):
    if value == "$200,000 and up":
        return 200000
    elif value == "Prefer not to answer":
        return np.nan
    elif isinstance(value,float):
        if math.isnan(value):
            return np.nan

    #getting rid of commas and $
    value = value.replace(",", "").replace("$", "")
    low, high = value.split(" to ")
    #return avg value
    return (int(low)+int(high))/2

def haversineFormula(lon1, lat1, lon2, lat2):

    R_earth = 6371 #km

    lon1, lat1, lon2, lat2 = [float(lon1), float(lat1), float(lon2), float(lat2)]

    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2-lon1
    dlat = lat2-lat1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.asin(math.sqrt(a))
    d = R_earth*c
    return d

def calc_distance(row, airports):
    dist = 0

    try:
        
        #we get the airport data for a given route (source airport and dest airport)
        #we use iloc[0] to get rid of unnecessary info, otherwise we
        #would also get index, col name and type, we just need value
        source = airports[airports["id"] == row["source_id"]].iloc[0]
        dest = airports[airports["id"] == row["dest_id"]].iloc[0]

        dist = haversineFormula(dest["longitude"], dest["latitude"], source["longitude"], source["latitude"])

    #we need exception in case there is data that cannot be processed
    except (ValueError, IndexError):
        pass

    return dist


def dataVisualization():
    
    airports = pd.read_csv(".\data\\airports.csv", header=None, dtype=str)

    #the data doesnt have headers, so we need to add them
    airports.columns = ["id", "name", "city", "country", "code", "icao", "latitude", "longitude", "altitude", "offset", "dst", "timezone", "more1", "more2"]

    #skiprows to ignore the first row which doesnt have useful info
    airlines = pd.read_csv(".\data\\airlines.csv", skiprows=[0], header=None, dtype=str)
    airlines.columns = ["id", "name", "alias", "iata", "icao", "callsign", "country", "active"]

    routes = pd.read_csv(".\data\\routes.csv", header=None, dtype=str)
    routes.columns = ["airline", "airline_id", "source", "source_id", "dest", "dest_id", "codeshare", "stops", "equipment"]

    #in the airline_id there are rows with a value "\N", so we need to take them out
    routes = routes[routes["airline_id"] != "\\N"]

    #axis=1 to apply on row level
    route_lengths = routes.apply(calc_distance, args=(airports,), axis=1)

    plt.hist(route_lengths, bins=20)
    print('hey')

dataVisualization()

