from datetime import datetime

import psycopg2
from page_analyzer import config
from psycopg2.extras import NamedTupleCursor


def get_db(app):
    return psycopg2.connect(config.DATABASE_DSN)


def close(conn):
    conn.close()


def commit(conn):
    conn.commit()


def get_urls(conn):
    query = "SELECT * FROM urls ORDER BY id DESC;"
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(query)
        urls = curs.fetchall()  # noqa: WPS442
    return urls


def find_url_by_name(conn, url):
    query = "SELECT id, name\
            FROM urls\
            WHERE name=%s"
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            query,
            (url,),
        )
        url = curs.fetchone()
    return url


def get_url_by_id(conn, id):
    query = "SELECT * FROM urls WHERE id = %s"
    with conn.cursor(cursor_factory=NamedTupleCursor) as url_curs:
        url_curs.execute(
            query,
            (id,),
        )
        url = url_curs.fetchone()
    return url


def add_url(conn, url):
    query = "INSERT INTO urls (name, created_at)\
            VALUES (%s, %s)\
            RETURNING id;"
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            query,
            (url, datetime.now()),
        )
        id = curs.fetchone().id
    return id


def get_url_checks(conn, id):
    query = "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;"
    with conn.cursor(cursor_factory=NamedTupleCursor) as check_curs:
        check_curs.execute(
            query,
            (id,),
        )
        checks = check_curs.fetchall()
    return checks


def get_urls_with_checks(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        query = "SELECT * FROM urls ORDER BY id DESC;"
        curs.execute(query)
        urls = curs.fetchall()
        query = "SELECT DISTINCT ON (url_id) * FROM url_checks\
                ORDER BY url_id DESC, created_at ASC;"
        curs.execute(query)
        checks = curs.fetchall()

    result = []
    checks_by_url_id = {check.url_id: check for check in checks}
    for url in urls:
        url_data = {}
        check = checks_by_url_id.get(url.id)
        url_data["id"] = url.id
        url_data["name"] = url.name
        url_data["last_check_date"] = check.created_at if check else ""
        url_data["status_code"] = check.status_code if check else ""
        result.append(url_data)

    return result


def get_checks(conn):
    query = "SELECT DISTINCT ON (url_id) * FROM url_checks\
            ORDER BY url_id DESC, id DESC;"
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(query)
        checks = curs.fetchall()
    return checks


def add_url_check(conn, url_id, page_data):
    query = "INSERT INTO url_checks\
            (url_id, status_code, h1, title, description, created_at)\
            VALUES (%s, %s, %s, %s, %s, %s);"
    with conn.cursor(cursor_factory=NamedTupleCursor) as check_curs:
        check_curs.execute(
            query,
            (
                url_id,
                page_data["status_code"],
                page_data["h1"],
                page_data["title"],
                page_data["description"],
                datetime.now(),
            ),
        )
