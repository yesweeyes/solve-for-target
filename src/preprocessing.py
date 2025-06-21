import pandas as pd
import numpy as np

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the input DataFrame by filling missing values and converting data types.

    Parameters:
    df (pd.DataFrame): Input DataFrame with potential missing values.

    Returns:
    pd.DataFrame: Preprocessed DataFrame with filled missing values and converted data types.
    """

    df = drop_columns(df, ["source", "date", "didPurchase"])
    df = drop_rows_with_missing_values(df, ["product", "categories", "reviews"])
    df = handle_missing_ratings(df)
    df = handle_missing_doRecommend(df)
    df = handle_missing_title(df)
    
    return df

def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Drop specified columns from the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    columns (list): List of column names to drop.

    Returns:
    pd.DataFrame: DataFrame with specified columns dropped.
    """
    return df.drop(columns=columns, errors='ignore')

def drop_rows_with_missing_values(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Drop rows with any missing values from the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with rows containing missing values dropped.
    """
    return df.dropna(subset=columns)


def handle_missing_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing ratings in the DataFrame by filling them with the mean rating.

    Parameters:
    df (pd.DataFrame): Input DataFrame with potential missing ratings.

    Returns:
    pd.DataFrame: DataFrame with missing ratings filled.
    """

    products_missing_ratings = df[df['rating'].isnull()]['product'].unique()
    for product in products_missing_ratings:
        median_rating = df[df['product'] == product]['rating'].median()
        df.loc[(df['product'] == product) & (df['rating'].isnull()), 'rating'] = median_rating

    return df

def handle_missing_doRecommend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing doRecommend values in the DataFrame by filling them with the mode.

    Parameters:
    df (pd.DataFrame): Input DataFrame with potential missing doRecommend values.

    Returns:
    pd.DataFrame: DataFrame with missing doRecommend values filled.
    """

    df.loc[df['doRecommend'].isna(), 'doRecommend'] = np.where(
        df.loc[df['doRecommend'].isna(), 'rating'] >= 4, 1, 0
    )
    
    return df

def handle_missing_title(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing titles in the DataFrame by filling them with the product name.

    Parameters:
    df (pd.DataFrame): Input DataFrame with potential missing titles.

    Returns:
    pd.DataFrame: DataFrame with missing titles filled.
    """

    df['title'] = df['title'].fillna('(missing title)')
    
    return df