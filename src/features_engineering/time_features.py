import re 






# Function to parse the time control and obtain the information of the time total and the increment 
def parse_time_control(tc_str):
    # Parse time controle 

    if not tc_str or tc_str == "*":
        return None, None

    try:
        # if many sentences, we keep the first one (ex: "40/6000+30:3000+30")
        first_phase = tc_str.split(":")[0]

        # Examples : "40/6000+30" ou "180+1"
        if "/" in first_phase:
            _, time_part = first_phase.split("/")
        else:
            time_part = first_phase

        # Cut time and increment 
        if "+" in time_part:
            base, inc = time_part.split("+")
            initial = int(base)
            increment = int(inc)
        else:
            initial = int(time_part)
            increment = 0

        return float(initial), float(increment)

    except Exception as e:
        print(f"⚠️ Impossible to parse time controle '{tc_str}' ({e})")
        return None, None


# Function to convert time in seconds 
def clock_str_to_seconds(clock_str):
    
    parts = clock_str.split(":")
    parts = [int(p) for p in parts]
    if len(parts) == 3:  # h:m:s
        h, m, s = parts
    elif len(parts) == 2:  # m:s
        h, m, s = 0, parts[0], parts[1]
    else:
        raise ValueError(f"Format de temps invalide : {clock_str}")
    return h * 3600 + m * 60 + s


# To select the time from the pgn files 
def extract_clock_from_comment(comment: str):
    """
    Extract time from a PGN comment containing {%clk X} or [%clk X]
    Returns a string "HH:MM:SS" or "MM:SS", or None.
    """
    if not comment:
        return None
    m = re.search(r"\%clk\s*([0-9:\.]+)", comment)
    if m:
        return m.group(1)
    return None
