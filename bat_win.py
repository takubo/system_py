#!/bin/python

from ctypes import windll
from ctypes import Structure, byref
from ctypes.wintypes import BYTE, LONG
import vim

class SystemPowerStatus(Structure):
    # https://msdn.microsoft.com/ja-jp/library/windows/desktop/aa373232(v=vs.85).aspx
    _fields_ = [
        ('ACLineStatus', BYTE),
        ('BatteryFlag', BYTE),
        ('BatteryLifePercent', BYTE),
        ('Reserved1', BYTE),
        ('BatteryLifeTime', LONG),
        ('BatteryFullLifeTime', LONG),
    ]

bat_info = { }
sps = SystemPowerStatus()

def bat_win_main():
    windll.kernel32.GetSystemPowerStatus(byref(sps))

    bat_info['ACLine'] = '$' if sps.ACLineStatus == 1 else '@' if sps.ACLineStatus == 0 else '?'

    bat_info['Charging'] = 'И' if sps.BatteryFlag & 0x08 else 'Ф'

    bat_info['RemainingPercent'] = '%3d%%' % sps.BatteryLifePercent if sps.BatteryLifePercent != -1 else '---%%'

    rem_sec = sps.BatteryLifeTime
    bat_info['RemainingTime'] = '[%2d:%02d:%02d]' % ( rem_sec / 3600, rem_sec % 3600 / 60, rem_sec % 60 ) if rem_sec != -1 else '[--:--:--]'

    full_sec = sps.BatteryFullLifeTime
    bat_info['FullTime'] = '[%2d:%02d:%02d]' % ( full_sec / 3600, full_sec % 3600 / 60, full_sec % 60 ) if full_sec != -1 else '[--:--:--]'

    # copy to vim var
    for i in bat_info:
        vim.command('let g:bat_info["' + i + '"] = "' + bat_info[i] + '"')
