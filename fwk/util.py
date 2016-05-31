
def search_for_key(d, key):
    """
    Returns the value of a dictonary item with key ``key`` in a JSON- notation
    object.
    """

    findings = []

    if isinstance(d, list):
        for item in d:
             findings.append(search_for_key(item, key))
    elif isinstance(d, dict):
        for k, v in d.items():
             if k == key:
                 findings.append(v)
             elif isinstance(v, list) or isinstance(v, dict):
                 findings.append(search_for_key(v, key))
    return reduce(lambda x,y: max(x,y), findings, None)  # NOOP