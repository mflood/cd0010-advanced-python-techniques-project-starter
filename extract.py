"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
from typing import List

from models import CloseApproach, NearEarthObject


def load_neos(neo_csv_path: str) -> List[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, "r", encoding="utf-8") as handle:
        dict_reader = csv.DictReader(handle)
        neo_list = []
        for item in dict_reader:
            neo = NearEarthObject(
                designation=item["pdes"],
                name=item["name"],
                diameter=item["diameter"],
                hazardous=item["pha"],
            )
            neo_list.append(neo)
    return neo_list


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.

    approach_list = []
    with open(cad_json_path, "r", encoding="utf-8") as handle:
        cad_object = json.load(handle)
        fields = cad_object["fields"]
        data = cad_object["data"]
        for item in data:
            item_dict = dict(zip(fields, item))
            # {'des': '170903', 'orbit_id': '105', 'jd': '2415020.507669610', 'cd': '1900-Jan-01 00:11',
            # 'dist': '0.0921795123769547', 'dist_min': '0.0912006569517418', 'dist_max': '0.0931589328621254',
            # 'v_rel': '16.7523040362574', 'v_inf': '16.7505784933163', 't_sigma_f': '01:00', 'h': '18.1'}
            close_approach = CloseApproach(
                designation=item_dict["des"],
                time=item_dict["cd"],
                distance=item_dict["dist"],
                velocity=item_dict["v_rel"],
            )
            approach_list.append(close_approach)
    return approach_list


if __name__ == "__main__":
    neo_list = load_neos("data/neos.csv")
    print(repr(neo_list[0]))
    print(str(neo_list[0]))

    approach_list = load_approaches("data/cad.json")
    print(repr(approach_list[0]))
    print(str(approach_list[0]))
