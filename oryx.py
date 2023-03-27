#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import argparse

from lolpython import lol_py


def banner():
    lol_py('=======================================================')
    lol_py('┌─┐┬─┐┬ ┬─┐ ┬')
    lol_py('│ │├┬┘└┬┘┌┴┬┘')
    lol_py('└─┘┴└─ ┴ ┴ └─')
    lol_py('# Recon Automation ~ for webapp security testing')
    lol_py('# By 0xRar ~ (0xrar.net)')
    lol_py('=======================================================')


def main():
    examples = f'''
    examples:
    python3 {sys.argv[0]} -t hackerone.com
    python3 {sys.argv[0]} -c -t machine.htb
    '''
    parser = argparse.ArgumentParser(
        epilog=examples,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-t",
        dest="target",
        help="target domain/ip",
        type=str,
        required=True
    )

    parser.add_argument(
        "-c",
        dest="ctf",
        help="used for ctfs/boot2root",
        required=False,
        action='store_true'
    )

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    target = args.target
    ctf = args.ctf

    # Wordlists
    params = '/usr/share/wordlists/SecLists/Discovery/Web-Content/burp-parameter-names.txt'
    dirs_files = '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .php,.js,.html,.bak,.xml'

    # Commands
    nmap = f'nmap -p- -sC -sV -Pn -T4 --min-rate=10000 {target}| tee recon/nmap.log'
    subfinder = f'subfinder -nW -d {target}| tee recon/sub-domains.log'
    arjun = f'arjun --stable -u http://{target}/ -w {params}| tee recon/parameters.log'
    gobuster = f'gobuster dir -u http://{target}/ -w {dirs_files}| tee recon/dirs.log'
    nuclei = f'nuclei -u http://{target}/ -as| tee recon/nuclei.log'

    print('# Please Wait 😄...\n')

    # Creating a recon directory to store the results
    subprocess.run('mkdir recon', shell=True)

    # Iterates through commands
    commands = [nmap, subfinder, arjun, gobuster, nuclei]

    if target and ctf:
        del commands[1]

    for command in commands:
        subprocess.run(command, shell=True)

    print('\nHappy Hacking 😄')


if __name__ == "__main__":
    banner()
    main()
