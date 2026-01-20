from pathlib import Path

import pandas as pd

from settings import EVENT_NAMES, MATCH_DATA_DIR, TAG_NAMES


class Match:
    def __init__(self, json_file: str, match_data_dir=None):
        self.json_file = json_file
        self.match_data_dir = match_data_dir
        self.data = None
        self.stats = {}
        self.event_types = None
        self.events = None

    def __repr__(self):
        return f"Match(json_file={self.json_file})"

    def load_data(self):
        data_dir = self.match_data_dir or MATCH_DATA_DIR
        match_path = Path(data_dir) / self.json_file
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
            .dropna(subset=["StartTimeMs"])
        )

        self.event_types = (
            self.event_types.drop(columns=["Clips"])
            .drop_duplicates()
            .reset_index(drop=True)
        )

        self.all_tags = (
            pd.json_normalize(self.events["Tags"].explode())["Title"].dropna().unique()
        )
        for tag in self.all_tags:
            self.events[tag] = self.events["Tags"].apply(
                lambda tags: any(t.get("Title") == tag for t in tags)
                if isinstance(tags, list)
                else False
            )

    def count_stats(self):
        # Get counts of each event type
        event_type_counts = (
            self.events["EventType"].value_counts().to_frame().reset_index()
        )
        self.stats["EventCounts"] = event_type_counts

        # Get tag counts for each event as DataFrame
        tag_counts = {}
        for tag in self.all_tags:
            tag_counts[tag] = (
                self.events[self.events[tag]].groupby("EventType").size().to_dict()
            )
        self.stats["TagCounts"] = (
            pd.DataFrame(tag_counts)
            .fillna(0)
            .astype(int)
            .reset_index()
            .rename(columns={"index": "EventType"})
        )

        # Extract detailed stats
        self._extract_quarters()
        self._extract_for_against_stats()
        self._extract_penalty_corner_stats()
        self._extract_circle_entry_stats()
        self._extract_goals()

    def _extract_quarters(self):
        """Extract quarter boundaries from Quarter Start events"""
        quarter_events = self.events[
            self.events["EventType"].str.contains("Quarter", case=False, na=False)
        ].sort_values("StartTimeMs")

        self.stats["quarters"] = {}
        self.num_quarters = len(quarter_events)

        # If no quarter events found, assign all events to Q1
        if self.num_quarters == 0:
            self.num_quarters = 1
            self.stats["quarters"]["Q1"] = self.events
            return

        quarter_times = quarter_events["StartTimeMs"].tolist()

        # All quarters except last: between quarter starts
        for i in range(0, self.num_quarters - 1):
            start_time = quarter_times[i]
            end_time = quarter_times[i + 1]
            quarter_events_df = self.events[
                (self.events["StartTimeMs"] >= start_time)
                & (self.events["StartTimeMs"] < end_time)
            ]
            self.stats["quarters"][f"Q{i + 1}"] = quarter_events_df

        # Last quarter: from last quarter start to end
        start_time = quarter_times[self.num_quarters - 1]
        end_time = self.events["StartTimeMs"].max()
        quarter_events_df = self.events[
            (self.events["StartTimeMs"] >= start_time)
            & (self.events["StartTimeMs"] < end_time)
        ]
        self.stats["quarters"][f"Q{self.num_quarters}"] = quarter_events_df

    def _extract_for_against_stats(self):
        """Separate events into FOR (ATT) and AGAINST (DEF) based on event type"""
        self.stats["for_events"] = self.events[
            self.events["EventType"].isin(
                [event["att"] for event in EVENT_NAMES.values()]
            )
        ]
        self.stats["against_events"] = self.events[
            self.events["EventType"].isin(
                [event["def"] for event in EVENT_NAMES.values()]
            )
        ]

        # Count by quarter
        self.stats["for_by_quarter"] = {}
        self.stats["against_by_quarter"] = {}

        for quarter in [f"Q{i + 1}" for i in range(self.num_quarters)]:
            if (
                quarter in self.stats["quarters"]
                and not self.stats["quarters"][quarter].empty
            ):
                q_events = self.stats["quarters"][quarter]
                self.stats["for_by_quarter"][quarter] = len(
                    q_events[
                        q_events["EventType"].isin(
                            [event["att"] for event in EVENT_NAMES.values()]
                        )
                    ]
                )
                self.stats["against_by_quarter"][quarter] = len(
                    q_events[
                        q_events["EventType"].isin(
                            [event["def"] for event in EVENT_NAMES.values()]
                        )
                    ]
                )
            else:
                self.stats["for_by_quarter"][quarter] = 0
                self.stats["against_by_quarter"][quarter] = 0

    def count_tag(self, df, tags: list[str]):
        for tag in tags:
            if tag in df.columns:
                return len(df[df[tag]])
        return 0

    def _extract_penalty_corner_stats(self):
        """Extract penalty corner outcomes"""
        pc_att = self.events[
            self.events["EventType"] == EVENT_NAMES["Penalty Corners"]["att"]
        ]
        pc_def = self.events[
            self.events["EventType"] == EVENT_NAMES["Penalty Corners"]["def"]
        ]

        # PCA stats
        self.stats["pca"] = {
            key: self.count_tag(pc_att, tags) for key, tags in TAG_NAMES.items()
        }
        self.stats["pca"]["total"] = len(pc_att)

        # PCD stats
        self.stats["pcd"] = {
            key: self.count_tag(pc_def, tags) for key, tags in TAG_NAMES.items()
        }
        self.stats["pcd"]["total"] = len(pc_def)

    def _extract_circle_entry_stats(self):
        """Extract circle entry outcomes and positions"""
        circle_att = self.events[
            self.events["EventType"] == EVENT_NAMES["Circle Entries"]["att"]
        ]
        circle_def = self.events[
            self.events["EventType"] == EVENT_NAMES["Circle Entries"]["def"]
        ]

        # Circle ATT stats
        self.stats["circle_att"] = {
            key: self.count_tag(circle_att, tags) for key, tags in TAG_NAMES.items()
        }
        self.stats["circle_att"]["total"] = len(circle_att)

        # Circle DEF stats
        self.stats["circle_def"] = {
            key: self.count_tag(circle_def, tags) for key, tags in TAG_NAMES.items()
        }
        self.stats["circle_def"]["total"] = len(circle_def)

    def _extract_goals(self):
        """Extract goal counts by quarter"""
        self.stats["goals_by_quarter"] = {"for": {}, "against": {}}

        # Get goal events
        for_goals = self.events[self.events["EventType"] == EVENT_NAMES["Goals"]["att"]]
        against_goals = self.events[
            self.events["EventType"] == EVENT_NAMES["Goals"]["def"]
        ]

        for quarter in ["Q1", "Q2", "Q3", "Q4"]:
            if (
                quarter in self.stats["quarters"]
                and not self.stats["quarters"][quarter].empty
            ):
                q_events = self.stats["quarters"][quarter]
                start_time = q_events["StartTimeMs"].min()
                end_time = q_events["StartTimeMs"].max()

                # Count goals in this quarter's time range
                q_for_goals = for_goals[
                    (for_goals["StartTimeMs"] >= start_time)
                    & (for_goals["StartTimeMs"] <= end_time)
                ]
                q_against_goals = against_goals[
                    (against_goals["StartTimeMs"] >= start_time)
                    & (against_goals["StartTimeMs"] <= end_time)
                ]

                self.stats["goals_by_quarter"]["for"][quarter] = len(q_for_goals)
                self.stats["goals_by_quarter"]["against"][quarter] = len(
                    q_against_goals
                )
            else:
                self.stats["goals_by_quarter"]["for"][quarter] = 0
                self.stats["goals_by_quarter"]["against"][quarter] = 0
