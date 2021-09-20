import pandas as pd

# U-score function
def uscore(data):
    """Calcultates the uscore of either a single value (univariate), or multiple values (multivariate).

    data - A list of rows
    """
    res = []
    for row in data:
        scores = [] # Init empty scores list
        for row2 in data:
            scores.append(indicator(row, row2))

        res.append(sum(scores))

    return res
    
# Indicator function
def indicator(datum1, datum2):
    """Returns 1 for superiority. Returns 0 if it can't be ordered, or if it is inferior"""
    if test_superiority(datum2, datum1):
        return 1
    elif test_superiority(datum1, datum2):
        return -1
    else:
        return 0 # Cannot be ordered
    
# Superiority test
def test_superiority(datum1, datum2):
    """Returns True if it is superior, returns False if it is inferior. Comparison is always "Is the second value superior to the 1st?"""
    # Test to see if they are equal
    if datum2 == datum1:
        return False # Identical pairs can't be superior/inferior

    # Run through each variable
    gt_cnt = 0
    for i in range(len(datum2)):
        if datum2[i] < datum1[i]:
            return False
        else: # It's greater than or equal
            if datum2[i] > datum1[i]:
                gt_cnt += 1

    # If any variables are greater than, it is superior
    if gt_cnt > 0:
        return True

##################################################
# Garbage dump
##################################################

# Pandas wrapper
def df_to_gen(df):
    """
    Generator that converts `pandas.DataFrame` rows into a generator of lists
    """
    df = df.dropna()
    for i, row in df.iterrows():
        yield row.tolist()

def calc_uscore_column(df):
    """Calculates a U score column based on all the columns present"""
    res = [] # Empty list for results
    for i, row in df.iterrows():
        datum = row.tolist()
        data = df_to_gen(df.drop(i))
        res.append(uscore(datum, data))

    return res

def uscore_sorted(datum_index, data):
    """Calculates a U score on a list that has already been sorted.

    datum_index - the index of the datum in question.
    data - a sorted list of the data.
    """
    import pdb
    pdb.set_trace()
    res = []

    new_ind = datum_index

    while new_ind != 0 and indicator(data[new_ind], data[datum_index]) != -1:
        new_ind -= 1

    num_superior = new_ind

    new_ind = datum_index
    total_n = len(data)

    while new_ind != total_n and indicator(data[new_ind], data[datum_index]) != 1:
        new_ind += 1

    num_inferior = total_n - (new_ind - 1)

    return num_inferior - num_superior

def calc_uscore_sorted(data):
    import functools
    data_sorted = sorted(data, key=functools.cmp_to_key(indicator), reverse=True)
    print("Data:\n {0}".format(data))
    print("Data Sorted:\n {0}".format(data_sorted))
    res = []
    for i, row in enumerate(data_sorted):
        res.append(uscore_sorted(i, data_sorted))
    return res, data_sorted



if __name__=='__main__':

    import numpy as np

    np.random.seed(1234)
    dat = pd.DataFrame(data=np.random.random_integers(1, 5, size=(5,3)), columns = ['v1','v2','v3'])
    orig_data = pd.DataFrame(index = [tuple(row) for row in dat.values.tolist()])
    data = dat.drop_duplicates().values.tolist()

    output = uscore(data)
    index = [tuple(row) for row in data]
    output_df = pd.DataFrame(data = output, index = index, columns = ['UScore'])

    result = orig_data.join(output_df)

    # Method 2
    output, data_sorted = calc_uscore_sorted(data)

    index = [tuple(row) for row in data_sorted]
    sorted_df = pd.DataFrame(data = output, index = index, columns = ['UScore2'])

    joined = result.join(sorted_df)

    print ("Results:\n {0}".format(joined))

