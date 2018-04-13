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

def print_bat_info(key):
    return
    if __name__ == '__main__':
        print(key, ':', bat_info[key])

def copy_to_vim():
    for i in bat_info:
        set_vim_var(i)

def set_vim_var(key):
    vim.command('let g:bat_info["' + key + '"] = "' + bat_info[key] + '"')

def bat_win_ini():
    global bat_info
    global sps

    bat_info = { }
    sps = SystemPowerStatus()
    #vim.command('let g:bat_info = {}')

def bat_win_main():
    windll.kernel32.GetSystemPowerStatus(byref(sps))

    bat_info['ACLine'] = '@' if sps.ACLineStatus == 1 else ':' if sps.ACLineStatus == 0 else '?'
    print_bat_info('ACLine')

    bat_info['Charging'] = 'y' if sps.BatteryFlag & 0x08 else 'n'
    print_bat_info('Charging')

    #t sps.BatteryLifePercent = 98  # test
    #t sps.BatteryLifePercent =  8  # test
    bat_info['RemainingPercent'] = '%3d%%' % sps.BatteryLifePercent if sps.BatteryLifePercent != -1 else '---%'
    print_bat_info('RemainingPercent')

    rem_sec = sps.BatteryLifeTime
    #t rem_sec = 7527   # test
    bat_info['RemainingTime'] = '[%d:%02d:%02d]' % ( rem_sec / 3600, rem_sec % 3600 / 60, rem_sec % 60 ) if rem_sec != -1 else '[-:--:--]'
    print_bat_info('RemainingTime')

    full_sec = sps.BatteryFullLifeTime
    bat_info['FullTime'] = '[%d:%02d:%02d]' % ( full_sec / 3600, full_sec % 3600 / 60, full_sec % 60 ) if full_sec != -1 else '[-:--:--]'
    print_bat_info('FullTime')

    copy_to_vim()

if __name__ == '__main__':
    #v bat_win_ini()
    #v bat_win_main()
    pass
