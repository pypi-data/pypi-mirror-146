import win32api,win32con,ctypes,time
def _123Tasd(_dat):
    return [65,83,68,70,71,72,74][ord(_dat)-49]
def _cde2zxc(_dat):
    return [90,88,67,86,66,78,77][[99,100,101,102,103,97,98].index(ord(_dat))]
def _CDE2qwe(_dat):
    return [81,87,69,82,84,89,85][[67,68,69,70,71,65,66].index(ord(_dat))]
def setBPM(_bpm):
    global _BPM
    _BPM=_bpm
def play(_notes,_Len):
    _MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
    _pressKey=[]
    for _i in _notes:   #将音符转换为键盘符
        if ord(_i)>=49 and ord(_i)<=55:  #中音
            _pressKey.append(_123Tasd(_i))
        elif ord(_i)>=97 and ord(_i)<=103:  #低音
            _pressKey.append(_cde2zxc(_i))
        elif ord(_i)>=65 and ord(_i)<=71:    #高音
            _pressKey.append(_CDE2qwe(_i))
            
    for _i in _pressKey:  #按键d
            win32api.keybd_event(_i,_MapVirtualKey(_i,0),0,0)
    time.sleep(60/_BPM*(1/_Len))
    for _i in _pressKey:  #释放
        win32api.keybd_event(_i,_MapVirtualKey(_i,0),win32con.KEYEVENTF_KEYUP, 0)
def Delay(_Len):
    time.sleep(60/_BPM*(1/_Len))
    
