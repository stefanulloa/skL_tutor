#from tutorial: https://www.dataquest.io/blog/pandas-python-tutorial/

def part1():
    #%%
    #above comment to activate "run cell" to see histograms
    import pandas as pd
    import matplotlib

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

    # %%

