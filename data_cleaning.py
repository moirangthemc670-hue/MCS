import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# ---------------- REMOVE DUPLICATES ----------------

def remove_duplicates(df):
    return df.drop_duplicates()

# ---------------- FILL MISSING ----------------

def fill_missing(df):

    numeric = df.select_dtypes(include='number').columns

    for col in numeric:
        df[col] = df[col].fillna(df[col].median())

    return df

# ---------------- SMART AI FILL ----------------

def smart_fill(df):

    df_copy = df.copy()

    numeric_cols = df_copy.select_dtypes(include='number').columns

    for col in numeric_cols:

        if df_copy[col].isnull().sum() > 0:

            train = df_copy[df_copy[col].notnull()]
            test = df_copy[df_copy[col].isnull()]

            if len(train) < 2:
                continue

            X_train = train[numeric_cols].drop(columns=[col], errors='ignore')
            y_train = train[col]

            X_test = test[numeric_cols].drop(columns=[col], errors='ignore')

            X_train = X_train.fillna(0)
            X_test = X_test.fillna(0)

            if X_train.shape[1] == 0:
                continue

            model = LinearRegression()

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            df_copy.loc[df_copy[col].isnull(), col] = predictions

    return df_copy

# ---------------- REMOVE OUTLIERS ----------------

def remove_outliers(df):

    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df = df[
            (df[col] >= lower) &
            (df[col] <= upper)
        ]

    return df

# ---------------- ENCODE ----------------

def encode_categorical(df):

    encoder = LabelEncoder()

    cat_cols = df.select_dtypes(include='object').columns

    for col in cat_cols:

        df[col] = encoder.fit_transform(df[col].astype(str))

    return df