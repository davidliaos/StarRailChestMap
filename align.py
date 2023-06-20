#taken from https://github.com/CHNZYX/Auto_Simulated_Universe since i was too lazy to create initial alignment 
import time

import numpy as np
import pywintypes
import win32api
import win32con
import win32gui

from utils.config import config
from utils.log import log
from utils.utils import UniverseUtils


def get_angle(su, safe):
    su.press("w")
    time.sleep(0.5)
    su.get_screen()
    blue = np.array([234, 191, 4])
    shape = (int(su.scx * 190), int(su.scx * 190))
    local_screen = su.get_local(0.9333, 0.8657, shape)
    local_screen[np.sum(np.abs(local_screen - blue), axis=-1) <= 150] = blue
    if safe:
        su.press("s")
    return su.get_now_direc(local_screen)


def main(cnt=10, safe=0):
    if safe:
        return
    log.info("Calibration Loading")
    su = UniverseUtils()
    su.multi = 1
    init_ang = get_angle(su, safe)
    lst_ang = init_ang
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 3000)
    if safe:
        su.press("w", 0.2)
    for i in [1,1,3]:
        ang_list = []
        for j in range(i):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 300)
            su.mouse_move(60)
            now_ang = get_angle(su, safe)
            sub = lst_ang - now_ang
            while sub < 0:
                sub += 360
            ang_list.append(sub)
            lst_ang = now_ang
        ang_list = np.array(ang_list)

        print(ang_list)
        ax = 0
        ay = 0
        for j in ang_list:
            if abs(j - np.median(ang_list)) <= 5:
                ax += 60
                ay += j
        su.multi *= ax / ay
    config.angle = str(su.multi)
    config.save()
    if safe == 0:
        try:
            win32gui.SetForegroundWindow(su.my_nd)
        except pywintypes.error:
            pass
    else:
        key = "sasddwwwaw"
        su.threshold = 0.97
        for i in range(len(key)):
            time.sleep(0.5)
            su.get_screen()
            if su.goodf() and not su.check("herta", 0.5,0.62):
                break
            else:
                su.press(key[i], 0.2)
    log.info("Calibrated")
    return 1


if __name__ == "__main__":
    main()
