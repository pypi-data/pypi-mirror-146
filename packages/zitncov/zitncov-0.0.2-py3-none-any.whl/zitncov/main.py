import argparse
from rich.console import Console
from zitncov.user import zitUser

def main():

    console = Console()
    
    parser = argparse.ArgumentParser(
        description="A ncov cli tool for ZIT(Zhengzhou Institute of Science and Technology)",
        epilog="(c) 2022 mm62633482@gmail.com",
    )
    parser.add_argument("-u", "--username", help="the username", required=True)
    parser.add_argument("-p", "--password", help="the password", required=True)


    subparsers = parser.add_subparsers(dest="command")

    # report command
    report = subparsers.add_parser("report", help="run the report action")
    report.add_argument(
        "-a", "--all", action="store_true", help="do the all report tasks today"
    )
    report.add_argument("-f", "--force", action="store_true", help="forcely report")

    report.add_argument("-t", "--temp", help="the body temperature (float)")

    # info command
    info = subparsers.add_parser("info", help="get the user info")
    info.add_argument("-u", "--user", action="store_true", help="the user main info")



    args = parser.parse_args()

    testme=zitUser(args.username, args.password)


