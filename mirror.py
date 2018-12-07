#!/usr/bin/env python3
import os
import subprocess
import requests
import time
from pathlib import Path

"""This script auto-sync my document folder to google drive"""
path1 = "~/.backup"
path2 = "~/.backup2"

def internet_is_on():	
    try:
       response = requests.get("http://www.google.com")
       return True
    except requests.ConnectionError:
       return False

def check_file():
    file1 = Path("/home/luan/.backup")
    file2 = Path("/home/luan/.backup.old")
    if not file1.is_file():
        os.system("touch /home/luan/.backup")
    if not file2.is_file():
        os.system("touch /home/luan/.backup.old")


def has_changed():
    cmd = "wc -l < /home/luan/.backup"
    file1 = subprocess.check_output(cmd, shell=True)
    cmd = "wc -l < /home/luan/.backup.old"
    file2 = subprocess.check_output(cmd, shell=True)
    return file1 != file2

def main():    
    while True:
        time.sleep(0.5)
        if(has_changed()):
            if(internet_is_on()):
                try:                	
                 os.system('cat /home/luan/.backup > /home/luan/.backup.old') 
                 os.system('zenity --title "Backup"  --notification --text="Realizando backup" --window-icon=/home/luan/Área\ de\ Trabalho//easybackup/img.png')
                 os.system('rclone sync /home/luan/Documentos/ CDrive:/')              
                 os.system('zenity --title "Backup"  --notification --text="Backup realizado com sucesso" --window-icon=/home/luan/Área\ de\ Trabalho//easybackup/img.png')                                     

                except RuntimeError:
                    os.system('zenity --title "Backup"  --error --text="Ocorreu algum erro"')
            else:
                os.system('zenity --title "Backup"  --error --text="Nenhuma conexão encontrada"')
                while not internet_is_on():
                    internet_is_on()



###### MAIN #####

check_file() #Verify if the file exists 
os.system('fswatch -m poll_monitor -r /home/luan/Documentos/ >> /home/luan/.backup&') #Starts to monitor the file
main() #Runs the main routine

##### END MAIN ####
