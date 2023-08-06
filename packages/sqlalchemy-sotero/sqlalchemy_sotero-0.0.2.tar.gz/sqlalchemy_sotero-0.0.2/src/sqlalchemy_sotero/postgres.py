from __future__ import absolute_import
from __future__ import unicode_literals

from collections import defaultdict
from sqlalchemy.dialects.postgresql.base import PGDialect
from sqlalchemy.sql import sqltypes
from sqlalchemy import util, sql
from sqlalchemy.engine import reflection
from .base import BaseDialect, MixedBinary
from urllib.parse import urlparse, parse_qs


colspecs = util.update_copy(
    PGDialect.colspecs,
    {sqltypes.LargeBinary: MixedBinary},
)


class SoteroPGDialect(BaseDialect, PGDialect):
    jdbc_db_name = "sotero:https"
    jdbc_driver_name = "com.soterosoft.jdbc.Driver"
    colspecs = colspecs

    def initialize(self, connection):
        super(SoteroPGDialect, self).initialize(connection)

    def create_connect_args(self, url):
        """
        Secured dialect expects jdbc url in the specific form that will conply with SQLAlchemy and Superset requirements.
        The dialect will make all the modifications needed to run the query
        "jdbc:sotero://<user>:<password>@<host>?creds_file=<json_location>&dataset=<dataset_id>&import_pwd=<pwd>"
        """
        if url is None:
            return
        d = url.translate_connect_args()

        split_result = d.get('database').rsplit('&import_pwd=')
        import_pwd = "" if len(split_result) == 1 else split_result[1]

        jdbc_url = d.get('host') + '/' + split_result[0]

        # add driver information
        if not jdbc_url.startswith("jdbc"):
            jdbc_url = f"jdbc:{self.jdbc_db_name}://{jdbc_url}"
        drivers = []

        kwargs = {
            "jclassname": self.jdbc_driver_name,
            "url": jdbc_url,
            # pass driver args - username and password via JVM System settings
            "driver_args": [d.get('username'), d.get('password', import_pwd)],
        }
        return ((), kwargs)

    @reflection.cache
    def get_unique_constraints(
        self, connection, table_name, schema=None, **kw
    ):
        table_oid = self.get_table_oid(
            connection, table_name, schema, info_cache=kw.get("info_cache")
        )

        UNIQUE_SQL = """
            SELECT
                cons.conname as name,
                cons.conkey as key,
                a.attnum as col_num,
                a.attname as col_name
            FROM
                pg_catalog.pg_constraint cons
                join pg_attribute a
                  on cons.conrelid = a.attrelid AND
                    a.attnum = ANY(cons.conkey)
            WHERE
                cons.conrelid = :table_oid AND
                cons.contype = 'u'
        """

        t = sql.text(UNIQUE_SQL).columns(col_name=sqltypes.Unicode)
        c = connection.execute(t, table_oid=table_oid)

        uniques = defaultdict(lambda: defaultdict(dict))
        for row in c.fetchall():
            uc = uniques[row.name]
            uc["key"] = (
                row.key.getArray() if hasattr(row.key, "getArray") else row.key
            )
            uc["cols"][row.col_num] = row.col_name

        return [
            {"name": name, "column_names": [uc["cols"][i] for i in uc["key"]]}
            for name, uc in uniques.items()
        ]


dialect = SoteroPGDialect
