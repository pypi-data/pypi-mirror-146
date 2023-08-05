from docopt import docopt
import sqlalchemy as sa
import pathlib
import os
import copy
import pandas as pd
from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import Session
from db_struct import mapper_registry
from db_struct import Account, Category, Tag, Txn, SplitTxn
from statement_mappings import StatementFactory

# internal
from dn_docoptutils import elim_apostrophes
from classify import BankClassify

# sys.tracebacklimit = 0
# TODO revise usage to make actual sense
# TODO transfer when assigning txn to new account, negate symbol and keep original total as same essentially
# TODO duplicating the transaction but in another account - integrate with split function?

usage = """
Banking Pipeline CLI

Usage:
    bpl_driver.py create            ((--a <num> (--TD | --SPLIT) (--f | --api) [<description> <adjust>]) | 
                                    ( --t <tag_desc>... ) | 
                                    ( --c <cat_desc>... ) )
    bpl_driver.py update            [<accounts>...]
    bpl_driver.py split_txn         (<txn_id> <split_by> (--p | --am) (--new | --old)) 
                                    [<new_cat> <new_acc>]
    bpl_driver.py process
                                    
Arguments:
    <accounts>                      must be account id, institution, number, or description
   
"""

# init globals
STORAGE_FP = 'C:\\Users\\Daniel\\Desktop\\ct_finance\\01_test\\'
DB_NAME = 'test_db.db'
DB_ENGINE = 'sqlite'

# process docopt args
args = docopt(usage)

elim_apostrophes(args=args)
print(args)
print()


# initialize database
class BplModel:

    def __init__(self, db_fp=STORAGE_FP + 'db\\'):

        self.engine = create_engine(DB_ENGINE + ":///" + db_fp + DB_NAME, echo=True, future=True)

        mapper_registry.metadata.create_all(self.engine)


def split_txn(db,
              session,
              txn_id, split_by, amount=None, percent=None, old=None, new=None,
              new_cat=None,
              new_acc=None):

    if not isinstance(split_by, float):
        split_by = float(split_by)

    # get old statement
    txn = session.query(Txn).filter(Txn.id == txn_id).one()

    # process new category
    if not new_cat:
        new_cat = txn.cat_id
    elif new_cat == txn.cat_id:
        new_cat = txn.cat_id
    else:
        categories = session.query(Category).all()
        for cat in categories:
            if cat.cat_desc == new_cat:
                new_cat = (session.query(Category)
                           .filter(Category.cat_desc == new_cat).one().id)
            elif new_cat == str(cat.id):
                new_cat = int(new_cat)
            else:
                continue

    # process new account
    if not new_acc:
        new_acc = txn.acc_id
    elif new_acc == txn.acc_id:
        new_acc = new_acc
    else:
        accounts = session.query(Account).all()
        for account in accounts:
            if new_acc == str(account.acc_num):
                new_acc = session.query(Account).filter(Category.acc_num == new_acc).one().id
            if new_acc == account.acc_desc:
                new_acc = session.query(Account).filter(Category.acc_desc == new_acc).one().id
            elif new_acc == str(account.id):
                new_acc = int(new_acc)
            else:
                continue

    # push old statement to splittxns
    split_txn = SplitTxn()
    split_txn.txn_date = txn.txn_date
    split_txn.txn_amount = txn.txn_amount
    split_txn.txn_unq_id = txn.unq_id

    session.add(split_txn)

    # calc new amounts
    new_amount = txn.txn_amount
    if amount:
        new_amount = split_by
    elif percent:
        if split_by > 1:
            split_by = split_by/100
        new_amount = txn.txn_amount * split_by
    remainder = txn.txn_amount - new_amount

    new_entry_amount = 0
    if old:
        txn.txn_amount = new_amount
        new_entry_amount = remainder
    elif new:
        txn.txn_amount = remainder
        new_entry_amount = new_amount

    # calc new total_ids
    new_total_id = copy.deepcopy(txn.unq_id)
    txn.unq_id = txn.unq_id + txn.txn_amount

    # insert new statement
    stmt = insert(Txn).values(txn_date=txn.txn_date,
                              txn_desc=txn.txn_desc,
                              txn_amount= new_entry_amount,
                              unq_id=new_total_id,
                              cat_id=new_cat,
                              acc_id=new_acc,
                              )
    conn = db.engine.connect()
    conn.execute(stmt)
    conn.commit()
    session.commit()


def parse_path(path):
    if not isinstance(path, pathlib.Path):
        return pathlib.Path(path)
    else:
        return path


def update_os_file(new_fp, acc_num):
    new_fp = parse_path(new_fp)

    # create dir in destination filepath to house account dirs
    os.makedirs(new_fp.joinpath('accounts'), exist_ok=True)

    # create dir for each account using account number
    account_fp = new_fp.joinpath('accounts').joinpath(str(acc_num))
    os.makedirs(account_fp, exist_ok=True)

    # relocate existing files
    # move_all_files(source_fp, new_fp)

    return


# driver utility
def add_account(args, db):
    # convert source option into string
    source = ""
    if args['--f']:
        source = 'file'
    elif args['--api']:
        source = 'api'

    # convert institution into string
    institution = ""
    if args['--TD']:
        institution = 'TD'
    elif args['--SPLIT']:
        institution = 'SPLIT'

    # proccess filepath
    new_fp = None
    if not new_fp:
        new_fp = STORAGE_FP

    new_fp = pathlib.Path(new_fp).joinpath('accounts').joinpath(str(args['<num>']))
    new_fp_str = new_fp.__str__()
    update_os_file(new_fp, args['<num>'])

    stmt = insert(Account).values(acc_num=args['<num>'],
                                  acc_inst=institution,
                                  acc_desc=args['<description>'],
                                  acc_fp=new_fp_str,
                                  acc_src=source,
                                  acc_adj=args['<adjust>'])
    conn = db.engine.connect()
    conn.execute(stmt)
    conn.commit()


def add_tag(args, db):
    conn = db.engine.connect()

    for tag in args['<tag_desc>']:
        stmt = insert(Tag).values(tag_desc=tag)
        conn.execute(stmt)
    conn.commit()


def add_category(args, db):
    conn = db.engine.connect()
    for tag in args['<tag_desc>']:
        stmt = insert(Tag).values(tag_desc=tag)
        conn.execute(stmt)
    conn.commit()


# driver logic
if args['create']:
    db = BplModel()
    if args['--a']:
        add_account(args, db)

    if args['--t']:
        add_tag(args, db)

    if args['--c']:
        add_tag(args, db)

elif args['update']:
    db = BplModel()
    conn = db.engine.connect()
    session = Session(db.engine)

    # load all accounts as Account objects with source as 'file'
    stmt = select(Account).filter_by(acc_src="file")
    account_objs = session.query(Account).filter_by(acc_src="file")

    # get accounts from args - process into list of ids, if no accounts use all
    accounts_ids = list()
    accounts = args['<accounts>']

    # append all account ids to acocunt_ids
    for account in account_objs:
        accounts_ids.append(account.id)

    # upload account files to db
    for acc_id in accounts_ids:
        # select account from previous account_objs query
        account_to_update = None
        for account in account_objs:
            if account.id == acc_id:
                account_to_update = account

        # generate iterator of .csv files in the account directory
        acc_dir = pathlib.Path(account_to_update.acc_fp).rglob('*.csv')
        # generate new dataframe for update
        new_data = pd.DataFrame()
        # get mapper for parsing correct banking statement into txn table
        statement_mapper = StatementFactory().statement_factory(account_to_update.acc_inst)

        # process all files in the directory
        for file in acc_dir:
            statement = file
            statement_df = pd.read_csv(statement, header=None)

            mapped_df = statement_mapper.map_2_txns(statement_df)
            mapped_df['acc_id'] = acc_id
            mapped_df = statement_mapper.update_unqID(mapped_df)

            if new_data.empty:
                new_data = mapped_df
            else:
                new_data = pd.concat([new_data, mapped_df], ignore_index=True, )
                new_data.drop_duplicates(inplace=True)

        new_data.to_sql(name=Txn.__table__.name,
                        index=False,
                        con=db.engine,
                        if_exists='append',)

        # delete duplicates
        # select minimum ids when grouped (see grouping below)
        min_ids = (session.query(sa.func.min(Txn.id))
                   .filter(Txn.acc_id == account_to_update.id)
                   .group_by(Txn.txn_date, Txn.txn_desc, Txn.txn_amount, Txn.unq_id)
                   )
        aliased_min_ids = sa.alias(min_ids)

        # select all from account not in the min group
        q = session.query(Txn).filter(~Txn.id.in_(aliased_min_ids), Txn.acc_id == account_to_update.id)

        # delete all not in the min group
        for txn in q:
            session.delete(txn)
        session.commit()

    # delete all from splits
    # select all from split txns
    split_txns = session.query(SplitTxn)

    split_dates = list()
    split_amounts = list()
    split_unq_ids = list()
    for row in split_txns:
        split_dates.append(row.txn_date)
        split_amounts.append(row.txn_amount)
        split_unq_ids.append(row.txn_unq_id)

    # select txns matching dates, amounts and unq_ids from splt txns
    q = session.query(Txn).filter(Txn.txn_date.in_(split_dates),
                                  Txn.txn_amount.in_(split_amounts),
                                  Txn.unq_id.in_(split_unq_ids),
                                  )

    # delete same txns from split txns
    for txn in q:
        session.delete(txn)
    session.commit()

elif args['split_txn']:
    db = BplModel()
    session = Session(db.engine)

    split_txn(db=db,
              session=session,
              txn_id=args['<txn_id>'],
              split_by=args['<split_by>'],
              percent=args['--p'],
              amount=args['--am'],
              new=args['--new'],
              old=args['--old'],
              new_cat=args['<new_cat>'],
              new_acc=args['<new_acc>'])

elif args['process']:

    db = BplModel()
    session = Session(db.engine)

    categories = dict()
    category_obs = session.query(Category).all()
    for cat in category_obs:
        categories[cat.id] = cat.cat_desc

    categories_df = pd.DataFrame([t.__dict__ for t in category_obs])
    cat_table_cols = Category.__table__.columns.keys()
    # strip all columns not in txns table
    categories_df = categories_df[categories_df.columns.intersection(cat_table_cols)]

    txn_table_cols = Txn.__table__.columns.keys()
    # get processed (and txn with cat_id) as Txn objects
    processed_txns = session.query(Txn).join(Category, Category.id == Txn.cat_id).all()
    # assign cat_desc in place of cat_id
    cat_descs = list()
    for txn in processed_txns:
        if txn.category:
            cat_descs.append(txn.category.cat_desc)

    # create df from Txn objects
    processed_txns_df = pd.DataFrame([t.__dict__ for t in processed_txns])

    processed_txns_df['cat_id'] = cat_descs
    # strip all columns not in txns table
    processed_txns_df = processed_txns_df[processed_txns_df.columns.intersection(txn_table_cols)]
    # reorder columns to be same as txns table
    processed_txns_df = processed_txns_df[txn_table_cols]

    # get all txns
    all_txns = session.query(Txn).all()
    # create data frame from Txn objects with properties as columns
    all_txns_df = pd.DataFrame([t.__dict__ for t in all_txns])
    txn_table_cols = Txn.__table__.columns.keys()
    # strip all columns not in txns table
    all_txns_df = all_txns_df[all_txns_df.columns.intersection(txn_table_cols)]
    # reorder columns to be same as txns table
    all_txns_df = all_txns_df[txn_table_cols]
    unprocessed_txns_df = all_txns_df[all_txns_df['cat_id'].isna()]

    session.commit()

    classifier = BankClassify(training_data=processed_txns_df, categories=categories)
    classifier.ask_with_guess(unprocessed=unprocessed_txns_df)

    # get df of new categories if any
    classifier_categories_df = pd.DataFrame.from_dict(classifier.categories, orient='index')
    # classifier_categories_df['index'] = classifier_categories_df.index
    classifier_categories_df.reset_index(inplace=True)
    rename_dict = dict()
    for i in range(0, classifier_categories_df.columns.size):
        rename_dict[classifier_categories_df.columns[i]] = Category.__table__.columns.keys()[i]
    classifier_categories_df.rename(columns=rename_dict, inplace=True)

    # remove existing categories from classifier categories
    new_categories_df = pd.concat([categories_df, classifier_categories_df]).drop_duplicates(keep=False)

    # append new categories
    if new_categories_df is not None:
        # new_categories_df = new_categories_df['cat_desc']
        new_categories_df.to_sql(Category.__table__.name, db.engine, if_exists='append', index=False)

    # append processed_transactions
    rename_dict = dict()
    if classifier.processed is not None:
        # need to revert columns names from classifier
        columns = Txn.__table__.columns.keys()
        for col in columns:
            for df_col in classifier.processed.columns:
                if col in df_col or df_col in col:

                    rename_dict[df_col] = col

        # init classifier and let it do its thangg
        classifier.processed.rename(columns=rename_dict, inplace=True)
        classifier.processed.to_sql(Txn.__table__.name, db.engine, if_exists='append', index=False)
        # eliminate duplicates - keeping duplicates with cat_id's
        # select minimum ids when grouped (see grouping below)
        max_ids = (session.query(sa.func.max(Txn.id))
                   .group_by(Txn.txn_date, Txn.txn_desc, Txn.txn_amount, Txn.unq_id)
                   )
        aliased_max_ids = sa.alias(max_ids)

        session = Session(db.engine)
        # select all from account not in the min group
        q = session.query(Txn).filter(~Txn.id.in_(aliased_max_ids))

        # delete all not in the min group
        for txn in q:
            session.delete(txn)
        session.commit()


# future/deprecated/not implemented
# if args['view']:
#     table_name = args['<table>']
#     tables = mapper_registry.metadata.tables.keys()
#     if table_name in tables:
#         table_object = table_object_by_name(table_name)
#         stmt = select(table_object)
#         # stmt = select(Account)
#         session = Session(engine)
#         for row in session.execute(stmt):
#             print(row)
#
#     else:
#         print("Table does not exist")
#
# if args['tag']:
#     for tag in args['<tag_desc>']:
#         # data.tag_entry(db=db, tagged_query=query, tag_param=tag)
#
#         update = dbUpdate(db=db)
#         update.tag_entry(tagged_query=query, tag_param=tag)
#
# if args['--help']:
#     print(usage)
#
# if args['update']:
#     if args['--a']:
#         if args['<account>']:
#             update = dbUpdate(db=db)
#             update.update_account(account=args['<account>'])
#
#         elif args['--all']:
#             accounts = db.conn.cursor().execute("SELECT num FROM accounts").fetchall()
#
#             for account in accounts:
#                 update = dbUpdate(db=db)
#                 update.update_account(account=account[0])
