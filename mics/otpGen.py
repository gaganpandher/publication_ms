def otpfunc():
    import random
    import datetime as dt
    n=random.randint(100,1000)
    t=dt.datetime.now().time()
    return n,t