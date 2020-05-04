""" Generate Transcript for Google ASR json files """

import json, datetime
from pathlib import Path
import pandas


def convert_time_stamp(n):
    """ Function to help convert timestamps from s to H:M:S """
    ts = datetime.timedelta(seconds=float(n))
    ts = ts - datetime.timedelta(microseconds=ts.microseconds)
    to_dt = datetime.datetime.strptime(str(ts), "%H:%M:%S")
    from_dt = to_dt.strftime("%H:%M:%S")
    return from_dt


def load_json(file):
    """Load in JSON file and return as dict"""
    json_filepath = Path(file)
    # check the json file exists
    assert json_filepath.is_file(), "JSON file does not exist"

    data = json.load(open(json_filepath.absolute(), "r", encoding="utf-8"))
    # check if we have the 'results' section in the json file
    assert "results" in data
    for i in range(len(data["results"])):
        # check if we have "alternatives", considering the format of Google ASR output
        assert "alternatives" in data["results"][i]
    return data


def decode_transcript(data):
    """Decode the transcript into a pandas dataframe"""

    # Assign data to variable
    data = data

    decoded_data = {"startTime": [], "endTime": [], "speaker": [], "comment": []}

    #TODO: how to generae seperate transcripts for multiple speakers?
    for i in range(len(data["results"])):
        # "alternatives" is not empty
        if len(data["results"][i]["alternatives"][0]) > 0:
            for j in range(len(data["results"][i]["alternatives"][0]["words"])):
                decoded_data["startTime"] = convert_time_stamp(
                    data["results"][i]["alternatives"][0]["words"][j]["startTime"][:-1])
                decoded_data["endTime"] = convert_time_stamp(
                    data["results"][i]["alternatives"][0]["words"][j]["endTime"][:-1])
                decoded_data["speaker"].append("")
                decoded_data["comment"].append("")

                # Write the word
                decoded_data["comment"][-1] += " " + data["results"][i]["alternatives"][0]["words"][j]["word"]

    # Produce pandas dataframe
    df = pandas.DataFrame(
        decoded_data, columns=["startTime", "endTime", "speaker", "comment"]
    )

    # Clean leading whitespace
    df["comment"] = df["comment"].str.lstrip()

    return df


def write(file, **kwargs):
    """Main function, write transcript file from json"""
    filename = file.replace(".json", "")
    print(f"Start loading {file}")
    # Load json file as dict
    data = load_json(file)

    # Decode transcript
    print(f"Start decoding {file}")
    df = decode_transcript(data)

    output_filename = f"output_{filename}.txt"
    print(f"Start generating the output file {output_filename}")
    # generate a txt file for transcript
    output = ""
    for i in range(df.shape[0]):
        output += df['comment'][i] + " "
    with open(output_filename, 'w') as file:
        file.write(output)
    print("Finish!")

