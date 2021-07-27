# file_sync
repo for file sync

This repo contains sources for a basic real time file sychronizer client.

It periodically scans for modifies in files_sync folder and syncs the files in it with remote clients.
It is fully cross-compatible because it does not use any 3rd party libraries nor system-specific calls nor external softwares.
It runs in combination with server-sync

just a quick reminder on how to run the softwares:

1) server is written in javascript on nodejs, just type npm install and npm start on the root folder to run it
2) client is written in python, it needs socket.io to work, just type pip install "python-socketio[client]" and then you can run it.
3) In servercom.py, you have to specify the ip address of the server (the port is already 3005 as the server) in variable self.host
4) files that you place in folder "files_sync", created at client first startup, will be kept in sync with other remote machines

Limitations:

1) it can sync small files (tested up to 210kb) because it uses websockets with no ustomization
2) it keeps folder sync as soon as both client are connected to the server at the same time
