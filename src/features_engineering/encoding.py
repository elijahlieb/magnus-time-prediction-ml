

def safe_int(x):
    """Return an int, else return None."""
    try:
        return int(x)
    except:
        return None
    
def encode_title(title):
    if title in [None, "", "NA"]:
        return 0
    title = title.upper()
    if title == "CM":
        return 1
    elif title in ["FM", "WFM"]:
        return 2
    elif title in ["IM", "WIM"]:
        return 3
    elif title == "GM":
        return 4
    else:
        return 0