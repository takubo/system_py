from ctypes import windll
from ctypes import Structure, byref
from ctypes.wintypes import BYTE, LONG

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

sps = SystemPowerStatus()
windll.kernel32.GetSystemPowerStatus(byref(sps))

bat_info = { }

def print_bi(key):
    print(key, ':', bat_info[key])

bat_info['ACLine'] = '@' if sps.ACLineStatus == 1 else ':' if sps.ACLineStatus == 0 else '?'
print_bi('ACLine')

bat_info['Charging'] = 'y' if sps.BatteryFlag & 0x08 else 'n'
print_bi('Charging')

#t sps.BatteryLifePercent = 98
#t sps.BatteryLifePercent =  8
bat_info['RemainingPercent'] = '%2d%%' % sps.BatteryLifePercent if sps.BatteryLifePercent != -1 else '--%'
print_bi('RemainingPercent')

rem_sec = sps.BatteryLifeTime
#t rem_sec = 7527
bat_info['RemainingTime'] = '[%d:%02d:%02d]' % ( rem_sec / 3600, rem_sec % 3600 / 60, rem_sec % 60 ) if rem_sec != -1 else '[--:--:--]'
print_bi('RemainingTime')

full_sec = sps.BatteryFullLifeTime
bat_info['FullTime'] = '[%d:%02d:%02d]' % ( full_sec / 3600, full_sec % 3600 / 60, full_sec % 60 ) if full_sec != -1 else '[--:--:--]'
print_bi('FullTime')
