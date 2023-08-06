from sqlalchemy.engine.reflection import Inspector
from alembic import op


def prep_upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    for table in tables:
        if table.startswith("_alembic_tmp_"):
            op.drop_table(table)
