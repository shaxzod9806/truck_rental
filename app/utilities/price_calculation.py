from datetime import datetime


def renting_time_calc(start_time, end_time):
    start_time = datetime.strptime(start_time, '%d/%m/%Y %H:%M:%S')
    end_time = datetime.strptime(end_time, '%d/%m/%Y %H:%M:%S')
    total_time = end_time - start_time
    renting_time = round(float(total_time.total_seconds()) / 3600, 1)
    return renting_time