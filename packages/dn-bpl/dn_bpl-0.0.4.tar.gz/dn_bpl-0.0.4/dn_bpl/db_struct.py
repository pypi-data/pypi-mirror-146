from sqlalchemy import Table, create_engine, UniqueConstraint, Column, Integer, DateTime, Text, REAL, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, registry

mapper_registry = registry()
Base = mapper_registry.generate_base()

txn_tags = Table(
    'txn_tags', mapper_registry.metadata,
    Column('txn_id', ForeignKey('txns.id', onupdate='CASCADE', ondelete='SET NULL'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id', onupdate='CASCADE', ondelete='SET NULL'), primary_key=True)
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_desc = Column(Text, nullable=False)

    txns = relationship("Txn", back_populates="category")

    # optional
    def __repr__(self):
        return f"Category(id={self.id!r}, cat_desc={self.cat_desc!r})"


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    acc_num = Column(Integer, nullable=False)
    acc_inst = Column(Text, nullable=False)
    acc_desc = Column(Text)
    acc_fp = Column(Text, unique=True)
    acc_src = Column(Text, CheckConstraint("acc_src IN ('file', 'api')"), nullable=False)
    acc_adj = Column(REAL)

    UniqueConstraint(acc_num, acc_inst)

    txns = relationship("Txn", back_populates="account")


class Txn(Base):
    __tablename__ = 'txns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    txn_date = Column(DateTime, nullable=False)
    txn_desc = Column(Text, nullable=False)
    txn_amount = Column(REAL, nullable=False)
    unq_id = Column(Integer, nullable=False)
    cat_id = Column(Integer, ForeignKey('categories.id', onupdate='CASCADE', ondelete='SET NULL'), default=None)
    acc_id = Column(Integer, ForeignKey('accounts.id', onupdate='CASCADE', ondelete='SET NULL'), nullable=False)

    category = relationship("Category", back_populates="txns", primaryjoin="Category.id==Txn.cat_id")
    account = relationship("Account", back_populates="txns")
    tags = relationship("Tag", secondary=txn_tags, back_populates="txns")


class SplitTxn(Base):
    """ store historical originals of split transactions otherwise will be picked up in updates from spreadsheets """
    __tablename__ = 'split_txns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    txn_date = Column(DateTime, nullable=False)
    txn_amount = Column(REAL, nullable=False)
    txn_unq_id = Column(Integer, nullable=False)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_desc = Column(Text, nullable=False, unique=True)

    txns = relationship("Txn", secondary=txn_tags, back_populates="tags")


# must include all table objects in this file!
TABLES = [Category, Account, Txn, SplitTxn, Tag]


# maybe a package for sqlqlchemy utility in future
def table_object_by_name(name):
    for table_object in TABLES:
        if table_object.__table__.name == name:
            return table_object
        else:
            continue


DB_NAME = 'test_db.db'
DB_ENGINE = 'sqlite'
STORAGE_FP = 'C:\\Users\\Daniel\\Desktop\\ct_finance\\01_test\\'


# initialize database
class BplModel:

    def __init__(self, db_fp=STORAGE_FP + 'db\\'):

        self.engine = create_engine(DB_ENGINE + ":///" + db_fp + DB_NAME, echo=True, future=True)

        mapper_registry.metadata.create_all(self.engine)
