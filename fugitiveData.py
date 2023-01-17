import pandas as pd
import re

from bs4 import BeautifulSoup


# Images model for fugitive -> images
class FImages:
    def __init__(self, df):
        self.df = pd.DataFrame(df)
        self.original = self.df.original.tolist()
        self.large = self.df.large.tolist()
        self.caption = self.df.caption.tolist()
        self.thumb = self.df.thumb.tolist()


# Files model for fugitive -> files
class FFiles:
    def __init__(self, df):
        self.url = None
        self.name = None


# Fugitive object
# Attr count: 53
class Fugitive:
    def __init__(self, df):
        self.df = df
        self.details = self.get_details()
        self.remarks = self.get_remarks()
        self.ncic = self.df.ncic
        self.scars_and_marks = self.get_scars_and_marks()
        self.images = FImages(df=self.df.images[0])
        self.person_classification = None
        self.weight = None
        self.height_min = None
        self.race = None
        self.age_range = None
        self.aliases = None
        self.complexion = None
        self.uid = None
        self.eyes_raw = None
        self.languages = None
        self.locations = None
        self.status = None
        self.reward_max = None
        self.eyes = None
        self.race_raw = None
        self.modified = None
        self.url = None
        self.publication = None
        self.additional_information = None
        self.reward_min = None
        self.weight_max = None
        self.build = None
        self.nationality = None
        self.files = None
        self.subject = None
        self.suspect = None
        self.weight_min = None
        self.occupations = None
        self.possible_states = None
        self.warning_message = None
        self.height_max = None
        self.title = None
        self.age_min = None
        self.reward_text = None
        self.description = None
        self.caution = None
        self.age_max = None
        self.path = None
        self.legat_names = None # Legal? FBI api grammar mistake
        self.possible_countries = None
        self.sex = None
        self.place_of_birth = None
        self.dates_of_birth_used = None
        self.hair_raw = None
        self.hair = None
        self.coordinates = None
        self.field_offices = None
        self.id = None

    def get_details(self):
        if self.df.remarks[0] is None:
            return None
        else:
            return re.sub(r'[\n\xa0]', '', BeautifulSoup.BeautifulSoup(self.df.details[0]).get_text())

    def get_remarks(self):
        if self.df.remarks[0] is None:
            return None
        else:
            return BeautifulSoup.BeautifulSoup(self.df.remarks[0]).get_text()

    def get_scars_and_marks(self):
        if self.df.scars_and_marks[0] is None:
            return None
        else:
            return re.sub(r'[\n\r]', '', self.df.scars_and_marks[0])
