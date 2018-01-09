import requests
import sys
from flask import json


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_results(results):

    results_by_unit = dict({})

    for result in results:
        unit_name = result["unit_name"]
        if not unit_name in results_by_unit:
            results_by_unit[unit_name] = []
        results_by_unit[unit_name].append(result)

    for unit_name, results in results_by_unit.items():
        heading_text = "# Unit: {}".format(unit_name)
        heading_pin = "{}{}# Unit: {}".format(bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC)
        heading = "{}{}".format(heading_pin, unit_name)
        underline = "{}{}{}".format(bcolors.OKBLUE, len(heading_text)*"-", bcolors.ENDC)
        print(heading)
        print("{}\n".format(underline))
        for result in results:
            passed = result["passed"]
            passing_marker = "✔" if passed else "X"
            marker_color = bcolors.OKGREEN if passed else bcolors.FAIL
            passing_marker = "{}{}{}".format(marker_color, passing_marker, bcolors.ENDC)
            print("[{}] Case: {}".format(passing_marker, result["case_name"]))
            if not passed:
                print("{}{}{}".format(bcolors.FAIL, result["message"], bcolors.ENDC))
                print("")

        print("\n")

if __name__ == "__main__":

    flags = []
    if len(sys.argv) > 1:
        flags = [f for f in sys.argv[1]]

    test_result = requests.post("http://localhost/test/runall")

    if 'v' in flags:
        print("Raw HTTP text:\n")
        print(test_result.text)

    if not test_result.status_code == 200:
        print("Tests didn't run properly.")
        print("HTTP status code: {}".format(test_result.status_code))
        print("")
        print(test_result.text)

    if "j" in flags:
        print(test_result.text)
        sys.exit(0)

    print("")
    test_result = json.loads(test_result.text)["result"]
    print_results(test_result)