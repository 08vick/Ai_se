def sort_list_of_dicts_ai(list_of_dicts, key_to_sort_by, reverse=False, default_value=None):
    """
    Sorts a list of dictionaries by a specific key.
    
    Args:
        list_of_dicts: The list of dictionaries to sort.
        key_to_sort_by: The key to sort by.
        reverse: Whether to sort in descending order.
        default_value: Default value for dictionaries missing the key.
    """
    if default_value is not None:
        # Use default value for missing keys
        return sorted(list_of_dicts, key=lambda d: d.get(key_to_sort_by, default_value), reverse=reverse)
    else:
        # Raise an error if a key is missing, as in the manual version
        return sorted(list_of_dicts, key=lambda d: d[key_to_sort_by], reverse=reverse)

# Example usage:
data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]
sorted_data = sort_list_of_dicts_ai(data, "age")
print(sorted_data)
