from concurrent.futures import ThreadPoolExecutor
from threading import Lock
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
print(colored("=" * 45, "blue"))
print("Scan Target: " + target)
print("Scanning started: " + str(datetime.now()))
print(colored("=" * 45, "blue"))


# banner grabbing
def banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                try:
                    data = s.recv(1024).decode(errors="ignore").strip()
                    if data:
                        print(f"Port {port}: {data}")
                    else:
                        print(f"Port {port}: no banner received")
                except Exception:
                    print(f"Port {port}: connected but no banner")
    except Exception as e:
        print(f"Error: {e}")


scanned = 0
lock = Lock()
start_port = 1
end_port = 1023  # module-level defaults so scan() always has valid values


def scan(port):
    global scanned
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)
            if s.connect_ex((target, port)) == 0:
                print("\033[38;5;218m" + "Port number {} is open".format(port) + "\033[0m")
                banner(target, port)
    except Exception:
        pass
    finally:
        with lock:
            scanned += 1
            print(f"Scanned: {scanned}/{end_port - start_port + 1}", end="\r")


if __name__ == "__main__":
    # user defined range or default
    choice = input(colored("Use default port range (1-1023)? (y/n): ","yellow")).lower()
    if choice !="y":
        start_port = int(input(colored("Enter start port: ","green")))
        end_port = int(input(colored("Enter end port: ","green")))

    # Run the scan (multithreaded)
    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(scan, range(start_port, end_port + 1))
        print("\nScan completed!")
    except KeyboardInterrupt:
        print(colored("\nScan halted by user", "yellow"))
        sys.exit()
    except socket.error:
        print(colored("Couldn't connect to server.", "red"))
        sys.exit()
