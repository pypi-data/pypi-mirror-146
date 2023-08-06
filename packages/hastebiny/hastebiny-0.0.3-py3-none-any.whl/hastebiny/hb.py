import requests

def send(payload:str, logging=True):
    """Send text to hastebin and return (str) key, return -1 if error. (400k character constraint)

    Args:
        payload (str): The text being sent.
        logging (bool, optional): Enables error logging to console. Defaults to True.

    Returns:
        str: Key attributed to text posted on hastebin.
    """
    
    try:
        preq = requests.post("https://www.toptal.com/developers/hastebin/documents", data=payload)
        return preq.json()["key"]
    except Exception as e:
        if logging:
            print(f"Error: {e} | Possibly attempted to send >400k characters")
        return -1

def get(key:str, logging=True):
    """Return (str) text attributed to a key from hastebin, return -1 if error.

    Args:
        key (str): Key attributed to a hastebin post.
        logging (bool, optional): Enables error logging to console. Defaults to True.

    Returns:
        str: Text from hastebin with given key.
    """
    
    try:
        greq = requests.get(f"https://www.toptal.com/developers/hastebin/raw/{key}")
        if greq.status_code == 410:
            if logging:
                print("Document not found. Possibly invalid key?")
            return -1
        return greq.text
    except Exception as e:
        if logging:
            print(f"Error: {e}")
        return -1

# used only for testing when this is main file, if this file is being imported nothing happens
if __name__ == "__main__":
    key = send("This is posting the message to hastebin and returning a key.")
    print(get(key)) # printing the returned text from the given key