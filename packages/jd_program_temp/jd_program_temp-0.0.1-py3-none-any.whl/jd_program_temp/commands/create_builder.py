# -*- coding: utf-8 -*-

import argparse

from jd_program_temp.commands.generate import *


def main():
    spider = argparse.ArgumentParser(description="生成器")

    spider.add_argument(
        "-p", "--project", help="创建项目 如  gengerate -p <project_name>", metavar=""
    )

    spider.add_argument(
         "--dt", help="项目时间标注",  action="store_true"
    )

    args = spider.parse_args()


    if args.project:
        GenerateProject().generate(args.project, args.dt)



if __name__ == "__main__":
    main()