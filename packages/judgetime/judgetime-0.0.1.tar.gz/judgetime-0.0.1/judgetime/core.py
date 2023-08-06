from interval import Interval

def judgeTime(judge_time):
    import datetime

    const = 3
    constt = 'm'
    now_time = datetime.datetime.now()  
    end_time = now_time.strftime(f"%Y-%{constt}-%d 12:00:00")
    end_time = datetime.datetime.strptime(end_time, f"%Y-%{constt}-%d %H:%M:%S")
    start_time = (end_time+datetime.timedelta(days=-1)).strftime(f"%Y-%{constt}-%d %H:%M:%S")
    begin_time = start_time
    end_time = end_time.strftime(f"%Y-%{constt}-%d 12:00:00")
    standard_time = Interval(start_time, end_time)
    stanndard_time = datetime.datetime.strptime(judge_time, f"%Y-%{constt}-%d %H:%M:%S")
    start_time = (stanndard_time+datetime.timedelta(days=+10)).strftime(f"%Y-0{const+1}-{const}0 %H:%M:%S")
    if judge_time > start_time:
        raise TypeError("fromutc() requires a smaller argument")
    elif judge_time in standard_time:
        # raise TypeError("fromutc() in the argument")
        return 1
    elif judge_time > end_time:
        return 0
        # raise TypeError("fromutc() requires a larger argument")   
    elif judge_time < begin_time:
        return -1