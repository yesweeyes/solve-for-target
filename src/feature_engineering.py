import pandas as pd
import src.utils as utils


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform feature engineering on the input DataFrame by cleaning product names and normalizing categories.

    Parameters:
    df (pd.DataFrame): Input DataFrame with product and category information.

    Returns:
    pd.DataFrame: DataFrame with cleaned product names and normalized categories.
    """

    df = clean_product_name(df)
    df = normalize_category(df)

    return df


def clean_product_name(df: pd.DataFrame) -> str:
    """
    Clean the product name by removing special characters and converting to lowercase.

    Parameters:
    df (pd.DataFrame): The original product name.

    Returns:
    pd.DataFrame: DataFrame with cleaned product names.
    """

    df['product'] = df['product'].apply(utils.util_clean_product_name)

    return df
    

def normalize_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the category names by converting them to lowercase and removing special characters.

    Parameters:
    df (pd.DataFrame): Input DataFrame with category names.

    Returns:
    pd.DataFrame: DataFrame with normalized category names.
    """

    df['categories'] = df['categories'].apply(utils.util_clean_category)
    df['categories'] = df['categories'].str.split(',')
    df['categories'] = df['categories'].apply(utils.util_normalize_category_list)

    # Same products can have multiple categories, so we merge them into a single list
    def merge_categories(series_of_category):
        all_tags = set()
        for tags in series_of_category:
            all_tags.update(tags)
        return list(all_tags)
    
    merged = df.groupby('product').agg({'categories': merge_categories}).reset_index()
    df = df.drop('categories', axis=1).merge(merged, on='product', how='left')
    
    return df

def create_feedback_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a feedback column from 'title' and 'reviews' columns.

    Parameters:
    df (pd.DataFrame): Input DataFrame with 'title' and 'reviews' columns.

    Returns:
    pd.DataFrame: DataFrame with a new 'feedback' column.
    """

    df['feedback'] = df['title'].astype(str) + df['reviews']
    
    return df