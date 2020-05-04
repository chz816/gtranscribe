# gtanscribe

This is a small tool could help you generate the transcript from the Google ASR output json files.

The code is inspired and modified from [tscribe](https://github.com/kibaffo33/aws_transcribe_to_docx). ```tscribe``` is a wonderful tool to help you produce transcriptions using the ASR files from AWS.

The input is expected to be a ```json``` file from Google ASR, and the output is the txt file.

## Local Setup

Tested with Python 3.7 via virtual environment.

Clone the repo, go to the repo folder, setup the virtual environment, and install the required packages:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

```python
import gtanscribe
gtanscribe.write("output.json")
```

```
Start loading sample.json
Start decoding sample.json
Start generating the output file sample.txt
Finish!
```

