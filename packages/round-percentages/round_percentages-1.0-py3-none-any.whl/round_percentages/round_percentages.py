def round_percentages(percentages):
    """
    Given an iterable of percentages that add up to 100, round them to the nearest integer such
    that the rounded percentages also add up to 100. Uses the largest remainder method.

    E.g.
    round_percentages([13.626332, 47.989636, 9.596008, 28.788024]) -> [14, 48, 9, 29]

    """
    result = []
    sum_of_integer_parts = 0

    for index, percentage in enumerate(percentages):
        integer, decimal = str(float(percentage)).split('.')
        integer = int(integer)
        decimal = int(decimal)

        result.append([integer, decimal, index])
        sum_of_integer_parts += integer

    result.sort(key=lambda x: x[1], reverse=True)
    difference = 100 - sum_of_integer_parts

    for percentage in result:
        if difference == 0:
            break
        percentage[0] += 1
        difference -= 1

    # order by the original order
    result.sort(key=lambda x: x[2])

    # return just the percentage
    return [percentage[0] for percentage in result]
