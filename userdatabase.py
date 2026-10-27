def data_quality_score(df):

    total = df.size

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    score = 100 - ((missing + duplicates) / total * 100)

    return max(0, round(score, 2))