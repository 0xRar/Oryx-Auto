#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import argparse

from playsound import playsound
from lolpython import lol_py


def banner():
    lol_py('┌─┐┬─┐┬ ┬─┐ ┬')
    lol_py('│ │├┬┘└┬┘┌┴┬┘')
    lol_py('└─┘┴└─ ┴ ┴ └─')
    lol_py('# Recon Automation ~ mainly for webapp security testing')
    lol_py('# By 0xRar ~ (0xrar.net)\n')


def main():
    parser = argparse.ArgumentParser(
        epilog=f'\tExample: \r\npython3 {sys.argv[0]} -t hackerone.com'
    )

    parser.add_argument(
        "-t",
        dest="target",
        help="target domain/ip",
        type=str,
        required=True
    )

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    target = args.target

    # Commands to run on target
    nmap = f'nmap -p- -sC -sV -Pn -T4 --min-rate=10000 {target}|tee nmap.log'
    subfinder = f'subfinder -nW -d {target}| tee sub-domains.log'
    arjun = f'arjun -u http://{target}/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/burp-parameter-names.txt| tee parameters.log'
    gobuster = f'gobuster dir -u http://{target}/ -w /usr/share/wordlists/directory-list-2.3-medium.txt -x .php,.html,.bak,.conf| tee dirs.log'
    nuclei = f'nuclei -u http://{target}/ -as| tee nuclei.log'

    commands = [nmap, subfinder, arjun, gobuster, nuclei]

    # next: katana? naabu? 👀

    print('# Will run nmap, subfinder, arjun, gobuster, nuclei')
    print('# Please Wait...\n\n')

    # Iterates through commands
    for command in commands:
        subprocess.run(command, shell=True)

    # Run an alert when the recon finishes
    playsound('./resources/recon_finished.mp3')


if __name__ == "__main__":
    banner()
    main()
