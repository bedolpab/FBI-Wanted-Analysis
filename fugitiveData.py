import numpy
import pandas as pd
import re

from bs4 import BeautifulSoup


# Images model for fugitive -> images
# We are finding patterns in textual data,
# though this df can be used later on for image patterns
class FImages:
    def __init__(self, df):
        self.df = pd.DataFrame(df)
        self.original = self.df.original.tolist()
        self.large = self.df.large.tolist()
        self.caption = self.df.caption.tolist()
        self.thumb = self.df.thumb.tolist()


# Files model for fugitive -> files
# We don't need pdfs atm, but may be useful to model it
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
        self.images = FImages(df=self.df.images)
        self.person_classification = self.df.person_classification
        # self.weight = None (disregard, make algo to fix)
        self.height_min = self.df.height_min  # stores np.float64
        self.race = self.df.race  # str
        self.age_range = None  # Discard (algo to fix)
        self.aliases = self.get_fugitive_aliases()
        self.complexion = self.df.complexion
        self.uid = self.df.uid
        self.eyes_raw = self.df.eyes_raw
        self.languages = self.df.languages
        self.locations = None  # Literally, no data for all 966
        self.status = None if self.df.status == "na" else None
        self.reward_max = self.df.reward_max  # numpy.int64
        self.eyes = self.df.eyes  # str
        self.race_raw = self.df.race_raw  # str
        self.modified = self.df.modified  # str
        self.url = self.df.url # str
        self.publication = self.df.publication  # str
        self.additional_information = None  # useless, keep attr for change
        self.reward_min = self.df.reward_min  # numpy.int64
        self.weight_max = self.df.weight_max # numpy.float64
        self.build = None  # Disregard build
        self.nationality = self.df.nationality  # str
        self.files = None  # no need for files, its data present here
        self.subject = self.df.subjects
        self.suspect = None  # dead column
        self.weight_min = self.df.weight_max # numpy.float64
        self.occupations = self.df.occupations  # list
        self.possible_states = self.get_possible_states()  # list of states ("IL", "PA")
        if self.df.warning_message is not None:
            self.warning_message = self.df.warning_message.lower() # str
        else:
            self.warning_message = self.df.warning_message
        self.height_max = self.df.height_max  # numpy.float64
        self.title = self.get_title()  # str
        self.age_min = self.df.age_min  # numpy.float64
        self.reward_text = self.get_reward()  # numpy.int32 (save space)
        self.description = self.df.description  # str
        self.caution = self.get_caution()  # str
        self.age_max = self.df.age_max  # numpy.float64
        if self.df.path is not None:
            self.path = self.df.path.split('/')[1] #str
        else:
            self.path = self.df.path
        self.legat_names = None  # Legal? FBI api grammar mistake (also empty, disregard)
        self.possible_countries = self.df.possible_countries  # list
        if self.df.sex is not None:
            self.sex = self.df.sex.lower()  # lower case str
        else:
            self.sex = self.df.sex
        self.place_of_birth = self.df.place_of_birth  # str
        self.dates_of_birth_used = self.df.dates_of_birth_used  # str list
        self.hair_raw = self.df.hair_raw
        self.hair = self.df.hair  # str
        self.coordinates = None  # empty - disregard
        self.field_offices = self.df.field_offices  # list str
        self.at_id = self.df.__getattr__("@id")

    def to_dict(self):
        return {
            f'Details ({type(self.details)})': self.details,
            f'Remarks ({type(self.remarks)})': self.remarks,
            f'NCIC ({type(self.ncic)})': self.ncic,
            f'Scars & Marks ({type(self.scars_and_marks)})': self.scars_and_marks,
            f'Images ({type(self.images)})': self.images,
            f'Person Classification ({type(self.person_classification)})': self.person_classification,
            f'Height Min ({type(self.height_min)})': self.height_min,
            f'Race ({type(self.race)})': self.race,
            f'Age Range ({type(self.age_range)})': self.age_range,
            f'Aliases ({type(self.aliases)})': self.aliases,
            f'Complexion ({type(self.complexion)})': self.complexion,
            f'U-ID ({type(self.uid)})': self.uid,
            f'Eyes Raw ({type(self.eyes_raw)})': self.eyes_raw,
            f'Languages ({type(self.languages)})': self.languages,
            f'Locations ({type(self.locations)})': self.locations,
            f'Status ({type(self.status)})': self.status,
            f'Reward Max ({type(self.reward_max)})': self.reward_max,
            f'Eyes ({type(self.eyes)})': self.eyes,
            f'Race Raw ({type(self.race_raw)})': self.race_raw,
            f'Modified ({type(self.modified)})': self.modified,
            f'URL ({type(self.url)})': self.url,
            f'Publication ({type(self.publication)})': self.publication,
            f'Additional Info ({type(self.additional_information)})': self.additional_information,
            f'Reward Min ({type(self.reward_min)})': self.reward_min,
            f'Weight Max ({type(self.weight_max)})': self.weight_max,
            f'Build ({type(self.build)})': self.build,
            f'Nationality ({type(self.nationality)})': self.nationality,
            f'Files ({type(self.files)})': self.files,
            f'Subject ({type(self.subject)})': self.subject,
            f'Suspect ({type(self.suspect)})': self.suspect,
            f'Weight Min ({type(self.weight_min)})': self.weight_min,
            f'Occupations ({type(self.occupations)})': self.occupations,
            f'Possible States ({type(self.possible_states)})': self.possible_states,
            f'Warning Message ({type(self.warning_message)})': self.warning_message,
            f'Height Max ({type(self.height_max)})': self.height_max,
            f'Title ({type(self.title)})': self.title,
            f'Age min ({type(self.age_min)})': self.age_min,
            f'Reward Text ({type(self.reward_text)})': self.reward_text,
            f'Description ({type(self.description)})': self.description,
            f'Caution ({type(self.caution)})': self.caution,
            f'Age Max ({type(self.details)})': self.age_max,
            f'Path ({type(self.path)})': self.path,
            f'Legal Names ({type(self.legat_names)})': self.legat_names,
            f'Possible Countries ({type(self.possible_countries)})': self.possible_countries,
            f'Sex ({type(self.sex)})': self.sex,
            f'Place of Birth ({type(self.place_of_birth)})': self.place_of_birth,
            f'Dates of Birth Used ({type(self.dates_of_birth_used)})': self.dates_of_birth_used,
            f'Hair Raw ({type(self.hair_raw)})': self.hair_raw,
            f'Hair ({type(self.hair)})': self.hair,
            f'Coordinates ({type(self.coordinates)})': self.coordinates,
            f'Field Offices ({type(self.field_offices)})': self.field_offices,
            f'@ID ({type(self.at_id)})': self.at_id
        }

    def get_details(self):
        if self.df.details is None:
            return None
        else:
            return re.sub(r'[\n\xa0]', '', BeautifulSoup(self.df.details, features="html.parser").get_text())

    def get_remarks(self):
        if self.df.remarks is None:
            return None
        else:
            return BeautifulSoup(self.df.remarks, features="html.parser").get_text()

    def get_scars_and_marks(self):
        if self.df.scars_and_marks is None:
            return None
        else:
            return re.sub(r'[\n\r]', '', self.df.scars_and_marks)

    # Should return list of aliases, not single (error)
    def get_fugitive_aliases(self):
        if self.df.aliases is None:
            return None
        else:
            for alias in self.df.aliases:
                if '"' in alias or '“' in alias:
                    match = re.search(r'"(.*?)"|“(.*?)”|“(.*?)"|"(.*?)“', alias).group(0)
                    match = re.sub(r'[\"|\“]', "", match)
                    return match
                else:
                    return alias

    def get_possible_states(self):
        if self.df.possible_states is None:
            return None
        else:
            states = []
            for state in self.df.possible_states:
                states.append(state.replace("US-", ""))

            return states

    def get_title(self):
        if self.df.title is None:
            return None
        else:
            # remove "-,.\" etc..
            return (' '.join([c for c in self.df.title if c.isalpha()])).lower()

    def get_reward(self):
        if self.df.reward_text is None:
            return None
        else:
            reward = self.df.reward_text.split(" ")
            for i, s in enumerate(reward):
                value = re.findall(r'(?:[\
                £\$\€][,\d]+.?\d*)', s)
                output = re.sub(r'[$,]', '', "".join(value))
                if output.__len__() == 0:
                    return None
                if output.__len__() < 2:
                    if reward[i + 1] == "million":
                        return numpy.int32(int(output) * 1000000)

                else:
                    return numpy.int32(output)  # no fug is worth $2B + atm

    def get_caution(self):
        if self.df.remarks is None:
            return None
        else:
            return re.sub(r'[\n\xa0]', '', BeautifulSoup(self.df.remarks, features="html.parser").get_text())

