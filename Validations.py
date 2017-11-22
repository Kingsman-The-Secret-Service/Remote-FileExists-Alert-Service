import re
def checkValidIp(ip):
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        return False
    except (AttributeError, TypeError):
        return False
def checkValidPort(port):
    try:
        while not re.findall(r'[0-9]+', port):
            return False
        else:
            return True
    except ValueError:
        return False
    except (AttributeError, TypeError):
        return False

def checkIsEmpty(value):
    try:
        if not value:
            return False
        else:
            return True
    except ValueError:
        return False
    except (AttributeError, TypeError):
        return False

def checkIsInteger(value):
    try:
        if not value:
            return False
        else:
            int(value)
            return True
    except ValueError:
        return False
    except (AttributeError, TypeError):
        return False