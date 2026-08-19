from concurrent.futures import ThreadPoolExecutor
import pyfiglet
import sys
import socket
from datetime import datetime
from termcolor import colored
# ASCII art
result = pyfiglet.figlet_format("PORT SCANNER", font="pagga")
print(colored(result, "magenta"))


# Define a target
if len(sys.argv) == 2:
    # Translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Please add a target hostname or IP address")
    sys.exit()

# Show scan info
print(colored("=" * 45,"blue"))
print("Scan Target: " + target)
print("Scanning started: " + str(datetime.now()))
print(colored("=" * 45,"blue"))


# Scans specified ports (adjustable, recommend well-known ports 1-1023)
def scan(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)
            # Scan results
            if s.connect_ex((target, port)) == 0:
                print("\033[38;5;218m"+"Port number {} is open".format(port)+"\033[0m")
    except Exception:
        pass


# Run the scan (multithreaded)
try:
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan, range(1, 1024))
# Interrupt a scan
except KeyboardInterrupt:
    print(colored("\nScan halted by user","yellow"))
    sys.exit()
except socket.error:
    print(colored("Couldn't connect to server.","red"))
    sys.exit()
