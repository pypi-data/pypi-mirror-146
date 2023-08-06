import pandas as pd

meta_data_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
#local_static_path = "/media/tighu/extended_storage/local_static_files_ukb/"

encoding_dict = {"ethnicity": {"-3.0": "Prefer not to answer", "-1.0": "Do not know", "1.0": "White", "2.0": "Mixed",
                               "3.0": "Asian or Asian British", "4.0": "Black or Black British", "5.0": "Chinese",
                               "6.0": "Other ethnic group", "1001.0": "British", "1002.0": "Irish",
                               "1003.0": "Any other white background", "2001.0": "White and Black Caribbean",
                               "2002.0": "White and Black African", "2003.0": "White and Asian",
                               "2004.0": "Any other mixed background", "3001.0": "Indian", "3002.0": "Pakistani",
                               "3003.0": "Bangladeshi", "3004.0": "Any other Asian background", "4001.0": "Caribbean",
                               "4002.0": "African", "4003.0": "Any other Black background"},
                 "nationality_encoding_dict": {},
                 "imaging_data_dictionary": {}, }


class scalar_data_handler:

    """
    A class to represent family of methods for handling and fetching scalar data

    ...

    Attributes
    ----------
    columns_to_read_for_field_id :
        list of relevant columns to read from metadata file


    Methods
    -------
    display_all_ukb_categories():
        displays all the categories

    get_field_ids_for_category(category_name):
        retrieves filed ids for a category

    get_subject_list_field_ids(category_name):
        retrieves list of subject relevant to that field id

    get_data_scalar(field_id,subject_id):
        fetches scalar data from metadata file

    """

    def __init__(self):
        self.columns_to_read_for_field_id = []
        return

    def display_all_ukb_categories(self):

        """
        The first prominent function which lets user see all the major categories present in the UKB dataset. Read
        categories from a static resource file inside package

        Parameters:
        Needs no parameters to operate

        Returns:
        categories list: List having all the unique categories of UKB
        :rtype: list of strings
        """
        unique_category_file_object = open(meta_data_path+"all_unique_categories.txt", "r")
        all_categories_list = unique_category_file_object.readlines()
        formatted_category_list = [a.rstrip() for a in all_categories_list]
        return formatted_category_list

    def get_field_ids_for_category(self, category_name=None):
        """
        A utility function which lets user see the associated field ids for each category, reads from a static file
        containing all the  category names and field ids

        Parameters:
        a string representing a category name

        Returns:
        categories list: pandas object having related field ids of the category
        :rtype: pandas table
        """

        temp_field_ids_df = pd.read_csv(meta_data_path+"ukb_field_ids.csv")
        return temp_field_ids_df[temp_field_ids_df['Category'] == category_name]

    def get_subject_list_field_ids(self, field_id=None):

        """
        A helper function which lets user see subjects having data related to a field_id. Reads a metadata file
        into a pandas object, only reading relevant columns because of size of the csv file

        Parameters:
        a int representing a field id

        Returns:
        subject list: a list of subject ids
        :rtype: list
        """

        with open(meta_data_path+'new_column_list_1.txt') as f:
            columns_list_df1 = f.readlines()

        for column_name in columns_list_df1:
            if int(column_name.split("-")[0]) == field_id:
                self.columns_to_read_for_field_id.append(column_name.strip())

        tempdf = pd.read_csv(meta_data_path+"ukb49570.csv", usecols=self.columns_to_read_for_field_id+['eid'])

        return tempdf['eid'].unique()

    def get_data_scalar(self, field_id=None, subject_list=None):
        """
        A helper function which lets user fetch scalar data associated with a field id and subject list.
        The fields in UKB dataset have been encoded in the following way: field_id-instance_number.array_index
        field_id : Numerical Number representing a particular feature of UKB dataset. For example 20252 represents
                   T1 NIFTI files
        instance_number: Currently 4 instances are present in the UKB dataset represents in which years of study was
                         data collected or recorded
                         Instance 0--> 2006-2010
                         Instance 1--> 2012-2013
                         Instance 2--> (2014+)
                         Instance 3--> (2019+)
        array_index: is the identifier present in cases where a single field id can have multiple values. An example
                     could be multiple readings of blood-pressure taken after fixed intervals

        Parameters:
        integers representing field id and subject id

        Returns:
        int/string: value of scalar data
        :rtype: int/str
        """

        field_id = str(field_id)
        cols_to_read = []
        for cols in self.columns_to_read_for_field_id:
            if cols.startswith(field_id):
                cols_to_read.append(cols)

        tempdf = pd.read_csv(meta_data_path+"ukb49570.csv", usecols=cols_to_read+['eid'])
        tempdf = tempdf.set_index('eid')

        return tempdf[tempdf.index.isin(subject_list)]
