from pathlib import Path

import pandas as pd

from settings import MATCH_DATA_DIR


class Match:
    def __init__(self, json_file: str):
        self.json_file = json_file
        self.data = None

    def __repr__(self):
        return f"Match(json_file={self.json_file})"

    def load_data(self):
        match_path = Path(MATCH_DATA_DIR) / self.json_file
        self.data = pd.read_json(match_path)

    def extract_events(self):
        self.event_types = pd.json_normalize(self.data["Events"]).rename(
            columns={"Title": "EventType"}
        )

        self.events = self.event_types.explode("Clips").reset_index(drop=True)
        self.events = (
            pd.json_normalize(self.events["Clips"])
            .reset_index(drop=True)
            .join(self.events[["EventType"]], how="left")
        )

        self.event_types = (
            self.event_types.drop(columns=["Clips"])
            .drop_duplicates()
            .reset_index(drop=True)
        )

        all_tags = (
            pd.json_normalize(self.events["Tags"].explode())["Title"].dropna().unique()
        )
        for tag in all_tags:
            self.events[tag] = self.events["Tags"].apply(
                lambda tags: any(t.get("Title") == tag for t in tags)
                if isinstance(tags, list)
                else False
            )
