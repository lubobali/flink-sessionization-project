def get_location(ip: str) -> str:
    if ip == "1.2.3.4":
        return "Chicago, IL"
    elif ip == "5.6.7.8":
        return "Sofia, Bulgaria"
    else:
        return "Unknown"
