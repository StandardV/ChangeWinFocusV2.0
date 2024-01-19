import win32gui,win32con,win32api
import pyautogui
import time
import os


path= os.path.join(os.path.dirname(__file__),'connect_zoom_in.png')
path1= os.path.join(os.path.dirname(__file__),'connect_zoom_out.png')


def move_cur(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x/1920*65535.0), int(y/1080*65535.0))
def mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

    
def windowEnumHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def bringToFront(window_name):
    top_windows = []
    win32gui.EnumWindows(windowEnumHandler, top_windows)
    for i in top_windows:
        # print(i[1])
        if window_name.lower() in i[1].lower():
            # print("found", window_name)
            win32gui.ShowWindow(i[0], win32con.SW_SHOWMAXIMIZED)
            win32gui.SetForegroundWindow(i[0])
            break

# Test with notepad
if __name__ == "__main__":
    winname = "Connect"
    bringToFront(winname)
    time.sleep(2)
    move_cur(100,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, -10)#region=( 1771 , 0 , 103 , 33 )
    time.sleep(0.5)

    # exit full screeen
    if pyautogui.locateOnScreen(path, confidence = 0.85, region=( 1649 , 0 , 270 , 35 )) != None:
        connect_zoom_icon_pos = pyautogui.locateCenterOnScreen(path, confidence = 0.85, region=( 1649 , 0 , 270 , 35 ))
        move_cur(connect_zoom_icon_pos[0],connect_zoom_icon_pos[1])
        time.sleep(0.1)
        mouse_click()
    elif pyautogui.locateOnScreen(path1, confidence = 0.85, region=( 1649 , 0 , 270 , 35 )) != None:
        connect_zoom_icon_pos = pyautogui.locateCenterOnScreen(path1, confidence = 0.85, region=( 1649 , 0 , 270 , 35 ))
        move_cur(connect_zoom_icon_pos[0],connect_zoom_icon_pos[1])
        time.sleep(0.1)
        mouse_click()


