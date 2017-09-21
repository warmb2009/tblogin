#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

#配置logging
ch = logging.StreamHandler()
    
def create_logger(level=logging.DEBUG, record_format=None):
    """Create a logger according to the given settings"""
    if record_format is None:
        record_format = "%(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s\t%(message)s"

    logger = logging.getLogger("mylogger")
    logger.setLevel(level)

    fh = logging.FileHandler('sys.log')
    fh.setLevel(level)


    ch.setLevel(level)

    formatter = logging.Formatter(record_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

