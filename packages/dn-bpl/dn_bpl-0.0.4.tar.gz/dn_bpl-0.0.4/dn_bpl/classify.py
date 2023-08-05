import re
import dateutil
import pandas as pd

from datetime import datetime
from textblob.classifiers import NaiveBayesClassifier
from colorama import init, Fore, Style
from tabulate import tabulate


class BankClassify:

    def __init__(self, training_data, categories):
        """categories as dict, keys as id, values as descriptions """

        self.training_data = self.format_data(training_data)
        self.categories = self._read_categories(categories)
        self.unprocessed = None
        self.processed = None

        self.classifier = NaiveBayesClassifier(self._get_training(self.training_data), self._extractor)

    def format_data(self, data_df=None):
        """ input df needs to have columns containing columns in list below, or need to be within column labels"""

        columns = ['date', 'desc', 'amount', 'cat']
        rename_dict = dict()

        if data_df is not None:
            # try and match columns to desired columns in columns list
            for col in columns:
                for df_col in data_df.columns:
                    if col in df_col:
                        rename_dict[df_col] = col

            # rename_columns
            data_df = data_df.rename(columns=rename_dict)
            data_df = data_df.reset_index(drop=True)
        else:
            data_df = pd.DataFrame(columns=columns)

        return data_df

    def _read_categories(self, categories=None):
        """ pass categories as dataframe and get dict"""
        if not isinstance(categories, dict):
            if categories:
                dcategories = categories.to_dict()['cat_desc']
            else:
                dcategories = dict()
        else:
            dcategories = categories

        return dcategories

    def _prep_for_analysis(self):
        """Prepare data for analysis in pandas, setting index types and subsetting"""
        self.training_data = self._make_date_index(self.training_data)

        self.training_data['cat'] = self.training_data['cat'].str.strip()

        self.inc = self.training_data[self.training_data.amount > 0]
        self.out = self.training_data[self.training_data.amount < 0]
        self.out.amount = self.out.amount.abs()

        self.inc_noignore = self.inc[self.inc.cat != 'Ignore']
        self.inc_noexpignore = self.inc[(self.inc.cat != 'Ignore') & (self.inc.cat != 'Expenses')]

        self.out_noignore = self.out[self.out.cat != 'Ignore']
        self.out_noexpignore = self.out[(self.out.cat != 'Ignore') & (self.out.cat != 'Expenses')]

    def _add_new_category(self, categories, category):
        """Add a new category to categories.txt"""
        if len(categories) != 0:
            max_key = max(list(categories.keys()))
            new_key = max_key + 1
            categories[new_key] = category
        else:
            categories[1] = category

        return categories

    def ask_with_guess(self, unprocessed):
        """Interactively guess categories for each transaction in df, asking each time if the guess
        is correct

        unprocessed as df
        """
        # Initialise colorama
        init()

        # format unprocessed data
        self.unprocessed = self.format_data(unprocessed)
        # self.unprocessed.rename(columns={"txn_desc": "desc"}, inplace=True)
        # create dataframe to house processed data
        self.processed = self.unprocessed[0:0]

        for index, row in self.unprocessed.iterrows():
            # Generate the category numbers table from the list of categories
            cats_list = [[idnum, cat] for idnum, cat in self.categories.items()]
            cats_table = tabulate(cats_list)

            stripped_text = self._strip_numbers(row['desc'])

            # Guess a category using the classifier (only if there is data in the classifier)
            if len(self.classifier.train_set) > 1:
                guess = self.classifier.classify(stripped_text)
            else:
                guess = ""

            # Print list of categories
            print(cats_table)
            print("\n")
            # Print transaction
            # print("On: %s\t %.2f\n%s" % (row['date'], row['amount'], row['desc']))
            # print(Fore.RED  + Style.BRIGHT + "My guess is: " + str(guess) + Fore.RESET)
            print(tabulate(self.unprocessed.loc[[index]], headers='keys'))
            print(Fore.RED + Style.BRIGHT + "My guess is: " + str(guess) + Fore.RESET)

            input_value = input("> ")
            category = ""
            if input_value.lower() == 'q':
                # If the input was 'q' then quit
                return

            if input_value == "":
                # If the input was blank then our guess was right!

                # update data with category ID
                # guess is always category description, need to match key to category for
                category_key = self.get_dict_key(self.categories, guess)
                category = guess
                # self.unprocessed.at[index, 'cat_id'] = category_key

                # update classifier with category (guess)
                self.classifier.update([(stripped_text, guess)])

            else:
                # Otherwise, our guess was wrong
                if input_value in self.categories.values():
                    # if entered category is a categories dictionary value, convert ot integer id and update data
                    category = input_value
                    category_key = self.get_dict_key(self.categories, input_value)
                else:
                    try:
                        category_key = int(input_value)
                        if int(input_value) in self.categories.keys():
                            # if integer key entered for category use as is
                            category_key = input_value
                            category = self.categories[int(input_value)]

                    except ValueError:
                        # Otherwise, we've entered a new category, so add it to the list of
                        # categories
                        category = input_value
                        self._add_new_category(self.categories, input_value)
                        category_key = self.get_dict_key(self.categories, input_value)

            # Write correct answer
            self.unprocessed.at[index, 'cat'] = category_key
            self.processed = self.processed.append(self.unprocessed.loc[[index]])
            # Update classifier
            self.classifier.update([(stripped_text, category)])

        return

    def get_dict_key(self, dict, value):
        key = list(dict.keys())[list(dict.values()).index(value)]

        if key:
            return key
        else:
            return None

    def _make_date_index(self, df):
        """Make the index of df a Datetime index"""
        df.index = pd.DatetimeIndex(df.date.apply(dateutil.parser.parse, dayfirst=True))

        return df

    def _get_training(self, df):
        """Get training data for the classifier, consisting of tuples of
        (text, category)"""
        train = []
        subset = df[df['cat'] != '']
        for i in subset.index:
            row = subset.iloc[i]
            new_desc = self._strip_numbers(row['desc'])
            train.append((new_desc, row['cat']))

        return train

    def _extractor(self, doc):
        """Extract tokens from a given string"""
        # TODO: Extend to extract words within words
        # For example, MUSICROOM should give MUSIC and ROOM
        tokens = self._split_by_multiple_delims(doc, [' ', '/'])

        features = {}

        for token in tokens:
            if token == "":
                continue
            features[token] = True

        return features

    def _strip_numbers(self, s):
        """Strip numbers from the given string"""
        return re.sub("[^A-Z ]", "", s)

    def _split_by_multiple_delims(self, string, delims):
        """Split the given string by the list of delimiters given"""
        regexp = "|".join(delims)

        return re.split(regexp, string)