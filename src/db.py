from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from .config import settings


def get_db_connection():
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
    )


def insert_job_entry(data: dict[str, Any]) -> None:
    sql = """
        INSERT INTO job_entries (
            file_name, file_modified_at, job, do_val,
            blk, blk_scan, blk_do,
            gen, gen_scan, gen_do,
            pol, pol_scan, pol_do,
            eng, eng_scan, eng_do,
            dba, dba_scan, dba_do
        ) VALUES (
            %(file_name)s, %(file_modified_at)s, %(job)s, %(do_val)s,
            %(blk)s, %(blk_scan)s, %(blk_do)s,
            %(gen)s, %(gen_scan)s, %(gen_do)s,
            %(pol)s, %(pol_scan)s, %(pol_do)s,
            %(eng)s, %(eng_scan)s, %(eng_do)s,
            %(dba)s, %(dba_scan)s, %(dba_do)s
        )
        ON CONFLICT (file_name, file_modified_at) DO NOTHING;
    """

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, data)


def load_processed_keys() -> set[tuple[str, object]]:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT file_name, file_modified_at FROM job_entries;")
            return set(cursor.fetchall())
