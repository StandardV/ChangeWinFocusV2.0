import win32con
import win32gui
import time
import win32api
import os
import threading
import FileModificationCheck as wd

auto_turn= False
nexttime = 0
path1 = os.path.join(os.path.dirname(__file__), "listrack.txt")
event = threading.Event()

current_directory = os.path.dirname(__file__)
track_file = "listrack.txt"




with open(path1, 'w') as fp:
    fp.write('True')
p_change = 'True'



def screen_off():
    """turn off screen"""
    #with open(path1, 'w') as fp:
    #    fp.write('False')
    return win32gui.SendMessage(win32con.HWND_BROADCAST,
                        win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)

def screen_on():
    """turn on screen from movement"""
    #with open(path1, 'w') as fp:
    #    fp.write('True')
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, -1)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1,-1)
    #return win32gui.SendMessage(win32con.HWND_BROADCAST,
    #                    win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, -1)
    

def perform_change(val): 
    """check if duplicate, if not perform screen off or on"""
    global p_change,auto_turn,nexttime,event
    if p_change != val and len(val) != 0:
        #print('infiltrated')
        
        if 'False'  in val:
            screen_off()
        elif 'True' in val:
            screen_on()
            event.set()
        elif 'Disable' in val:
            nexttime = time.time()+6_000_000_000
            with open(path1, 'w') as fp:
                fp.write(p_change)
        elif 'Enable' in val:
            nexttime = time.time()+600
            with open(path1, 'w') as fp:
                fp.write(p_change)
        elif 'Sleep' in val:
            nexttime = time.time()+5
            val = 'True'
            with open(path1, 'w') as fp:
                fp.write('True')
        else:
            print("houston we have a problem, output is:(",val,")")
        p_change = val

def auto_turnoff():
    """count down time to turn off screen"""
    global nexttime,event
    nexttime = time.time() + 600 
    while True:
        if p_change == 'False':
            
            event.wait()
            print('escape event wait')
            event.clear()     
            nexttime = time.time() + 600
        if nexttime < time.time():
            nexttime = time.time() + 600
            print('here')
            with open(path1, 'w') as fp:
                fp.write('False')
    #after a period of time, auto invoke screen of functionality

def actively_monitor(): #actively check if state changed
    """monitor file if it's true or false"""
    global auto_turn
    while True:
        time.sleep(1) #open file, (read), then wait and do it again

        #open...read
        # if state the same as it is from before, skip, else, trigger function
        if auto_turn == True:
            with open(path1, 'w') as fp:
                fp.write('False')
            auto_turn = False
        else:
            with open(path1, 'r') as fp:
                line = fp.readline()           
            perform_change(line)
        
def action_on_call():
    time.sleep(0.1)
    
    with open(path1, 'r') as fp:
        line = fp.readline()       

    print('watchdog triggered with line =',line)  
     
    perform_change(line)




if __name__ == '__main__':
    p1=wd.FileModifiedHandler(current_directory,track_file,action_on_call)
    #p1 = threading.Thread(target=wd.FileModifiedHandler(current_directory,track_file,action_on_call))
    p2 = threading.Thread(target=auto_turnoff)
    #p1.start()
    p2.start()