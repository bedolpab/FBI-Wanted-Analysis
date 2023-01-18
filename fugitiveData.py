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
# ATTR MAY RETURN NONE, IMPLEMENT NONE CHECK ? lambda?
class Fugitive:
    def __init__(self, df):
        self.df = df
        self.details = self.get_details()
        self.remarks = self.get_remarks()
        self.ncic = self.df.ncic
        self.scars_and_marks = self.get_scars_and_marks()
        self.images = FImages(df=self.df.images[0])
        self.person_classification = self.df.person_classification[0]
        # self.weight = None (disregard, make algo to fix)
        self.height_min = self.df.height_min[0] # stores np.float64
        self.race = self.df.race[0] # str
        self.age_range = None # Discard (algo to fix)
        self.aliases = self.get_fugitive_aliases()
        self.complexion = self.df.complexion[0]
        self.uid = self.df.uid[0]
        self.eyes_raw = self.df.eyes_raw[0]
        self.languages = self.df.languages[0]
        self.locations = None # Literally, no data for all 966
        self.status = None if self.df.status[9] == "na" else None
        self.reward_max = self.df.reward_max[0] # numpy.int64
        self.eyes = self.df.eyes[0] # str
        self.race_raw = self.df.race_raw[0] # str
        self.modified = self.df.modified[0] # str
        self.url = self.df.url[0] # str
        self.publication = self.df.publication[0] # str
        self.additional_information = None # useless, keep attr for change
        self.reward_min = self.df.reward_min[0] # numpy.int64
        self.weight_max = self.df.weight_max[0]
        self.build = None #Disregard build
        self.nationality = self.df.nationality[0] # str
        self.files = None # no need for files, its data present here
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

    # Should return list of aliases, not single (error)
    def get_fugitive_aliases(self):
        if self.df.aliases[0] is None:
            return None
        else:
            for alias in self.df.aliases[0]:
                if '"' in alias or '“' in alias:
                    match = re.search(r'"(.*?)"|“(.*?)”|“(.*?)"|"(.*?)“', alias).group(0)
                    match = re.sub(r'[\"|\“]', "", match)
                    return match
                else:
                    return alias

