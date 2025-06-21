import re

import re

import re

def remove_duplicate_product_name(product_name: str) -> str:
    """
    Remove duplicated product names if the name is repeated consecutively.

    Parameters:
    product_name (str): The raw product name.

    Returns:
    str: Cleaned product name with duplicates removed.
    """
    if not product_name:
        return ""

    # Normalize whitespaces and lowercase
    name = product_name.lower().strip()
    name = re.sub(r'\s+', ' ', name)

    # Split by space and check halves
    tokens = name.split()
    half = len(tokens) // 2

    if len(tokens) % 2 == 0 and tokens[:half] == tokens[half:]:
        return ' '.join(tokens[:half])
    return name


def util_clean_product_name(product_name: str) -> str:
    """
    Clean the product name by removing special characters, HTML artifacts, and normalizing text.
    
    Parameters:
    product_name (str): The original product name.
    
    Returns:
    str: Cleaned product name.
    """
    if not product_name:
        return ""

    cleaned_name = product_name.lower().strip()

    cleaned_name = remove_duplicate_product_name(cleaned_name)

    # Handle common artifacts like 'x000d'
    cleaned_name = re.sub(r'(\\x[0-9a-fA-F]{2,4}|x000d|\\r|\\n)', ' ', cleaned_name)

    # Remove any special characters except alphanumerics and space
    cleaned_name = re.sub(r'[^a-z0-9\s]', ' ', cleaned_name)

    # Remove extra whitespace
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)

    # Remove noise words (case-insensitive full word match)
    noise_terms = [
        'brand name', 'xyz brand', 'retail brand', 'electronics brand',
        'certified refurbished', 'includes special offers',
        'with special offers', 'special offers', 'previous generation',
        'new', 'brand new', 'official oem', 'product name'
    ]

    # Replace noise terms
    for term in noise_terms:
        cleaned_name = re.sub(rf'\b{re.escape(term)}\b', '', cleaned_name)

    # Final whitespace cleanup
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)

    return cleaned_name.strip()


def util_clean_category(category: str) -> str:
    """
    Normalize the category name by converting it to lowercase and removing special characters.

    Parameters:
    category (str): The original category name.

    Returns:
    str: Normalized category name.
    """
    
    cleaned_category = str(category).lower().strip()
    brand_patterns = r"(all.*?|walmart.*?|target.*?|mazon.co.uk|retail brand.*?|xyz.*?|brand name.*?|see more.*?)(,|$)"

    cleaned_category = re.sub(brand_patterns, '', cleaned_category)
    # cleaned_category = re.sub(r'[^a-z0-9\s]', '', cleaned_category)  # Remove special characters except spaces
    cleaned_category = re.sub(r'\s{2,}', ' ', cleaned_category)  # Remove multiple spaces
    cleaned_category = re.sub(r'\s+', ' ', cleaned_category)  # Remove extra spaces
    cleaned_category = cleaned_category.strip()

    return cleaned_category

def util_normalize_category_list(category_list: list) -> list:
    """
    Normalize a list of category names by cleaning each category.

    Parameters:
    category_list (list): List of category names.

    Returns:
    list: List of normalized category names.
    """

    normalization_map = {
        'ipad & tablets': 'tablets',
        'ipads tablets': 'tablets',
        'all tablets': 'tablets',
        'xyz brand tablets': 'tablets',
        'android tablets': 'tablets',
        'windows tablets': 'tablets',
        'tablets & ebook readers': 'tablets',
        'tablets & ereaders': 'tablets',
        'kids\' tablets': 'tablets',

        'e-readers': 'ereaders',
        'ebook readers': 'ereaders',
        'ebook readers & accessories': 'ereaders',
        'e-readers & accessories': 'ereaders',
        'ereaders & accessories': 'ereaders',
        'brand name e-readers': 'ereaders',

        'computers/tablets & networking': 'computers & tablets',
        'computers & laptops': 'computers & tablets',

        'audio docks & mini speakers': 'audio',
        'speaker systems': 'audio',
        'portable audio & headphones': 'audio',
        'audio player accessories': 'audio',

        'smart home & connected living': 'smart home',
        'smart home & home automation devices': 'smart home',
        'home safety & security': 'smart home',
        'smart hubs & wireless routers': 'smart home',
        'voice-enabled smart assistants': 'smart home',
        'voice assistants': 'smart home',
        'virtual assistant speakers': 'smart home',
        'alarms & sensors': 'smart home',

        'cases & bags': 'accessories',
        'tablet accessories': 'accessories',
        'tablet cases covers': 'accessories',
        'power adapters': 'accessories',
        'power adapters & cables': 'accessories',
        'computer accessories': 'accessories',
        'covers': 'accessories',

        'brand name e-reader accessories': 'accessories',
        'brand name paperwhite accessories': 'accessories',
        'brand name touch (4th generation) accessories': 'accessories',
        'brand name touch (4th generation) covers': 'accessories',
        'brand name (5th generation) accessories': 'accessories',
        'brand name (5th generation) covers': 'accessories',

        'books & magazines': 'media',
        'software & books': 'media',
        'book accessories': 'media',
        'movies': 'media',
        'music': 'media',

        'walmart for business': 'retail',
        'top rated': 'retail',
        'clearance': 'retail',
        'frys': 'retail',
        'categories': 'retail',
        'featured brands': 'retail',
    }

    normalized = []
    for cat in category_list:
        key = cat.strip().lower()
        if key in normalization_map:
            mapped = normalization_map[key]
            if mapped not in normalized:
                normalized.append(mapped)
        else:
            if key not in normalized:
                normalized.append(key)
    return normalized
