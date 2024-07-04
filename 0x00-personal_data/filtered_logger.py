#!/usr/bin/env python3
"""personal data"""
import mysql.connector
import logging
from os import environ
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """log message obfuscated

    Arguments
    ---------
    fields: List
    redaction: str
    message: str
    separator: str

    Return
    ------
    """
    for field in fields:
        pattern = f"{field}=.*?{separator}"
        message = re.sub(pattern, f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """get logger

    Arguments
    ---------
    None

    Return
    ------
    logging.logger
    """
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(c_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ get database

    Arguments
    ---------
    None

    Return:
    ------

    mysql.connector.connection.MySQLConnection
    """
    connection = None
    connection = mysql.connector.connect(
            host=environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
            user=environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=environ.get('PERSONAL_DATA_DB_PASSWORD', ""),
            database=environ.get('PERSONAL_DATA_DB_NAME')
            )
    return connection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format a given record

        Arguments
        ---------
        record: logging.LogRecord

        Return
        ------
        str
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def main():
    """main fonction"""

    db = get_db()
    logger = get_logger()
    sep = RedactingFormatter.SEPARATOR
    formater = RedactingFormatter(PII_FIELDS)
    cursor = db.cursor()
    querie = ("SELECT name, email, phone,\
              ssn, password, ip, last_login, user_agent FROM users")
    cursor.execute(querie)

    for row in cursor:
        log_record = ""
        message = ("name={}{}email={}{}phone={}{}ssn={}{}password={}\
                    {}ip={}{}last_login={}{}user_agent={}{}"
                   .format(row[0], sep, row[1], sep, row[2], sep,
                           row[3], sep, row[4], sep, row[5],
                           sep, row[6], sep, row[7], sep))
        logger.info(message)


if __name__ == "__main__":
    main()
