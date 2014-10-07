CSE 4990 - Practical 3
===============

This is the third practical that I did for my Reverse Engineering and Malware Analysis class that I took at Mississippi State University during Spring 2014. It analyzes the WEBC2-CSON malware sample that Mandiant has attributed to the APT1 Chinese hacker group. In addition to analyzing it, I was also required to create a local command and comtrol server that interacts with a patched version of the malware sample that points to this local server.

For more information, please take a look at Report.pdf. Opening practical3.idb in IDA would also give some more information about what I did while reverse engineering the malware. 

Usage
------
Unzip practical3_patched.zip with password "malware" and run the executable inside. WARNING: This zip file contains real, potentially harmful malware. It has been modified to not communicate with the attacker's command and control server, so it is unlikely that any harm will be done, but is still malware, so precautions should be taken when executing it. I only ran it in a virtual machine that wasn't connected to the Internet.

Open one terminal window and issue:
`python CCServer.py`

In a second terminal window, issue:
`python CCInterface.py`

In the window running CCInterface.py, a list of valid commands is shown. Any of these commands can now be issued. The other window running CCServer.py will show some output from the server.
