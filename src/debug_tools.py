from collections import Counter

def count_ranges(values, step=20):
    """
    Count the number of occurrences in each range for a list of values.
    
    :param values: List of integer values.
    :param step: Range size for grouping values.
    :return: None
    """
    # Group values by range
    range_counts = Counter((x // step) * step for x in values)

    # Print the counts for each range
    for i in range(0, 360, step):
        # Calculate the range string, e.g., "[0, 10)"
        range_str = f"[{i}, {i + step})"
        # Print the count for the range, defaulting to 0 if not in the dictionary
        print(f"{range_str}: {range_counts.get(i, 0)}")