from pandas.api.types import is_numeric_dtype, is_string_dtype


def getColumnTypes(df):
    col = df.columns
    ColumnType = []
    Categorical = []
    Object = []
    Numerical = []
    for i in range(len(col)):
        if is_numeric_dtype(df[col[i]]):
            ColumnType.append("Numerical")
            Numerical.append(col[i])
        elif is_string_dtype(df[col[i]]):
            ColumnType.append("Categorical")
            Categorical.append(col[i])
        else:
            ColumnType.append("Object")
            Object.append(col[i])

    return ColumnType, Categorical, Numerical, Object


def getNumberNullsByCol(df):
    col = df.columns
    nullNumber = []
    for i in range(len(col)):
        nullNumber.append(sum(df[col[i]].isna()))
    return nullNumber
