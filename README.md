# Richmond Hockey Club - Performance Analysis

This repo contains the tools I use for analysis (but obviously not the raw data, because that would be confidential). 

We currently use [Coach Logic](https://www.coach-logic.com/) as our video analysis platform which is also where the data collection happens. Data is exported as JSON and analysed with the tools here. 

## Running the tool

You will need a `.env` file in the project root with the following:

```
MATCH_DATA_DIR="path_to_match_data"
OUTPUT_DIR="path_to_output"
```

This repo uses [uv](https://docs.astral.sh/uv/) for package management. Install it, then run 

```
uv run main.py
```
