# argparse
import argparse

from je_auto_control.utils.json.json_file import read_action_json
from je_auto_control.utils.executor.action_executor import execute_action

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--execute_file", type=str, help="choose action file to execute")
    args = parser.parse_args()
    if args.execute_file is not None:
        execute_action(read_action_json(args.execute_file))
    else:
        print("No argument, Hello There :)")
