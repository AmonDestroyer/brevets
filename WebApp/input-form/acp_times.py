"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import math

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#
ACP_brevets = [(0, 200, 15, 34),
               (200, 400, 15, 32),
               (400, 600, 15, 30),
               (600, 1000, 11.428, 28),
               (1000, 1300, 13.333, 26)]
#(bot of control location range, top of control location range, minimum speed, maximum speed)
#(km, km, km/hr, km/hr)
#A table containing th control times tables]
final_times = {200: 13.5,
               300: 20,
               400: 27,
               600: 40,
               1000: 75}
#Maximum closing times brevet_dist:time(hr)

def _get_time(control_dist_km, brevet_dist_km, open_time):
    """
    Args:
        control_dist_km: number, the control distance in kilometers.
        brevet_dist_km: number, the nominal distance of the brevet in
        kilometers, which is defined by official ACP brevet distances.
        open_time: boolean, if the open time should be provided. False if the
        close time should be provided.
    Returns:
        time: number, time in minutes from the start of the brevet that the
        open or close time should be set to.
    """
    time = 0
    for (bot_range, top_range, slow_speed, fast_speed) in ACP_brevets:
        if open_time:
            speed = fast_speed
        else:
            speed = slow_speed

        if top_range <= brevet_dist_km and top_range < control_dist_km:
            time += 60 * ((top_range - bot_range) / speed)
            if top_range == brevet_dist_km: #Checkpoint past brevet oddity
                time = final_times[top_range] * 60;
                break
        else:
            time += 60 * ((control_dist_km - bot_range) / speed)
            break

    return round(time)

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    time = _get_time(control_dist_km, brevet_dist_km, True)
    start_time = arrow.get(brevet_start_time)
    return start_time.shift(minutes=time).isoformat()

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    time = _get_time(control_dist_km, brevet_dist_km, False)
    start_time = arrow.get(brevet_start_time)
    return start_time.shift(minutes=time).isoformat()
