import subprocess
import time
import os
import sys

# process_list = []

# def is_process_running(process_name):
#     #this one to keep tab of the client side and keyboard && mouse, since it might crash
    
#     #specifically also keeping tab of the webserver
#     cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)
#     output = subprocess.check_output(cmd, shell=True).decode()
#     if process_name.lower() in output.lower():
#         return True
#     else:
#         return False


# def if_process_running(pid):
#     """ Check if a process with the given PID is still running. """
#     try:
#         os.kill(pid, 0)
#     except OSError:
#         return False
#     else:
#         return True




# def monitor_server(process):
#     """ Monitor the server process, restart if it stops. """
#     try:
#         while True:
#             if not is_process_running(process.pid):
#                 print("Server crashed, restarting...")
#                 process = start_server()
#             time.sleep(60)  # Check every 60 seconds
#     except KeyboardInterrupt:
#         print("Monitoring stopped.")    
# #also have to make an additional checking method for both client and server side

# # Ctrl+shift+W

# is_process_running("chrome.exe")
class Program_Bundle_manager:
    def __init__(self):
        self.do_while_track = True
        self.reset_attempt = 1
        self.time_wait = 300
        self.last_reset_time = 0
        self.wait_attempt = 3 #attempt to reset, preset and wont change

    def start_server(self): 
        """ Start the server and return the process. """
        command = "python manage.py runserver 0.0.0.0:8000"
        process = subprocess.Popen(command,
                               shell=True,
                               cwd = r"C:\Users\duong\Documents\autostart\virtual-assistant\Store-django")
        return process

    def start_client(self): 
        """start the screen control process"""
        command = "python client.py"
        process = subprocess.Popen(command,
                                   shell=True,
                                   cwd = r"C:\Users\duong\Documents\autostart\virtual-assistant")
        return process

    def start_screen_control(self):
        """start the screen control process"""
        command = "python screencontrol.py"
        process = subprocess.Popen(command,
                                    shell=True,
                                    cwd = r"C:\Users\duong\Documents\autostart")
        return process

    def client_attempting_reset(self,process):
        """attempting to reset client 3 times"""
        print('Return code is: ',process)
        try:
            rasp_client = self.start_client()
        except Exception as e:
            print('Exception Ocurred:', e)
            pass

        if self.reset_attempt > self.wait_attempt :
            print('access time modifer')
            self.time_wait = 43200 #half a day waiting after 3 fail reset attempt

        current_time = time.time()
        if current_time - 600 <= self.last_reset_time:
            self.reset_attempt +=1
        else:
            self.reset_attempt = 1
            self.time_wait = 300
        self.last_reset_time = current_time
        return rasp_client


    def program_run(self):
        while True:
            if self.do_while_track is True:
                try:
                    screen_control = self.start_screen_control()
                    django_server = self.start_server()
                    rasp_client = self.start_client()
                except Exception as e:
                    print('Exception Ocurred:', e)
                    pass
                self.do_while_track = False


            _, _ = rasp_client.communicate()
            print('\nRasp_client interupted, attempting reset.\n Wait time:',self.time_wait
              ,'\n Current time:',time.localtime(),'\n Reset Attempt:',self.reset_attempt,'\n\n')
            time.sleep(self.time_wait)
            rasp_client = self.client_attempting_reset(rasp_client.returncode)



BundleManager = Program_Bundle_manager()
BundleManager.program_run()