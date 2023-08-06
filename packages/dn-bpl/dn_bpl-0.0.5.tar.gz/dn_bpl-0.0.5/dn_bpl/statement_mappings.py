import pandas as pd
# from pandas.DataFrame import round


class StatementFactory:

    def statement_factory(self, institution):
        """ determine which statement ob to use and return """
        if 'TD'.lower() in institution or 'TD' in institution:
            return TDStatement()
        elif 'SPLIT'.lower() in institution or 'SPLIT' in institution:
            return SplitwiseStatement()
        else:
            return


class BankStatement:

    def map_2_txns(self, statement):
        """ map native statement structure to txns table/model """
        return


class TDStatement(BankStatement):
    def map_2_txns(self, statement):
        """
        TD .csv statement structure

        col0:       date
        col1:       description
        col2:       outgoing txns
        col3:       incoming txns
        col4:       account total
        """
        # merge negative and positive txns to single column, invert negative txns
        statement[3].fillna(statement[2]*-1, inplace=True)
        # drop negative txns col after merge
        statement.drop(columns=[2], inplace=True)
        statement.columns = ['txn_date', 'txn_desc', 'txn_amount', 'unq_id']
        # parse date col as datetime
        statement['txn_date'] = pd.to_datetime(statement['txn_date'])

        return statement

    def update_unqID(self, statement):
        """ create new total id from existing - unq_id is rounded total of account """

        statement['unq_id'] = statement['unq_id'].round(decimals=2)

        return statement


class SplitwiseStatement(BankStatement):
    def map_2_txns(self, statement):
        """
        Splitwise .csv statement structure

        col0:       date
        col1:       description
        col2:       expense category
        col3:       total expense amount
        col4:       currency str
        col5:       others expense
        col6:       personal expense
        """

        # drop expense category, total, currency and others expense
        statement.drop(columns=[2, 3, 4, 5], inplace=True)

        # slice out bottom statement and total
        last_index = statement.loc[statement[0].isnull()].index.tolist()
        statement = statement.iloc[:last_index[0]]

        statement[3] = statement[6]
        # assign column mappings to txns db model
        statement.columns = ['txn_date', 'txn_desc', 'txn_amount', 'unq_id']
        # parse date col as datetime
        statement['txn_date'] = pd.to_datetime(statement['txn_date'])

        return statement

    def update_unqID(self, statement):
        """ create new total id from existing - unq_id is rounded total of account """

        # statement['unq_id'] = statement.groupby(by=['txn_date'], sort=False).rolling(window=2)['txn_amount'].sum().values
        # statement['unq_id'] = statement.rolling(window=2)['txn_amount'].sum().values
        statement['unq_id'] = statement['txn_amount'].cumsum()
        statement['unq_id'] = statement['unq_id'].round(decimals=2)

        return statement
