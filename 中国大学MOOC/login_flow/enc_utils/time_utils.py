import time

def getTimeStamp():
    """Get the current time stamp in seconds."""
    return int(time.time())


def getTimeStampOfMilliSeconds():
    """Get the current time stamp in milliseconds."""
    return int(time.time() * 1000)

if __name__ == '__main__':
    print(getTimeStampOfMilliSeconds())