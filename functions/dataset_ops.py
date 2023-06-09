from pandas.api.types import is_numeric_dtype, is_string_dtype


def getColumnTypes(df):
    col = df.columns
    ColumnType = []
    Categorical = []
    Object = []
    Numerical = []
    for i in range(len(col)):
        if is_numeric_dtype(df[col[i]]):
            ColumnType.append("Numeric")
            Numerical.append(col[i])
        elif is_string_dtype(df[col[i]]):
            ColumnType.append("String")
            Categorical.append(col[i])
        else:
            ColumnType.append("Object")
            Object.append(col[i])

    return ColumnType, Categorical, Numerical, Object

def getElementsNotSharedInLists(list1, list2):
    new_elements = list(set(list2) - set(list1))
    deleted_elements = list(set(list1) - set(list2))
    return new_elements, deleted_elements

def getNumberNullsByCol(df):
    col = df.columns
    nullNumber = []
    for i in range(len(col)):
        nullNumber.append(sum(df[col[i]].isna()))
    return nullNumber
