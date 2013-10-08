#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import pygame

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    def on_created(self, event):
        print "e=", event
        print "path=", event.src_path
        if len(os.listdir('/home/pi/Player')) == 1:
            if event.src_path[len(event.src_path)-4:] == ".mp3":
                try:
                    print "Load musique : " + event.src_path
                    pygame.mixer.music.load(event.src_path)
                    print "play musique"
                    pygame.mixer.music.play()
                except Exception as e:
                    print str(e)
            else:
                print "Ce n'est pas un fichier mp3"
        else:
            print "Plusieurs fichiers présent dans le dossier"

def main():    
    pygame.mixer.init()
    observer = Observer()
    event_handler = MyEventHandler(observer)

    observer.schedule(event_handler, "/home/pi/Player", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        observer.stop()
    observer.join()

    return 0

if __name__ == "__main__":
    sys.exit(main())