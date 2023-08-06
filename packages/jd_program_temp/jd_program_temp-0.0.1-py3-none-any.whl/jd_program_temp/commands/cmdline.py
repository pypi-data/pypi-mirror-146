# -*- coding: utf-8 -*-


import sys
from os.path import dirname, join

from jd_program_temp.commands import create_builder



def _print_commands():
    with open(join(dirname(dirname(__file__)), "VERSION"), "rb") as f:
        version = f.read().decode("ascii").strip()

    print("jd_program_temp {}".format(version))
    print("\nUsage:")
    print("  jd_program_temp <command> [options] [args]\n")
    print("Available commands:")
    cmds = {
        "create": "create project",

    }
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass))

    print('\nUse "jd_program_temp <command> -h" to see more info about a command')


def execute():
    args = sys.argv
    if len(args) < 2:
        _print_commands()
        return

    command = args.pop(1)
    if command == "generate":
        create_builder.main()
    else:
        _print_commands()
if __name__ == "__main__":
    execute()