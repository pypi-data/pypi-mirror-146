# -*- coding: utf-8 -*-
"""
oathldap_srv.logger - initialite custom logger
"""

import logging
import logging.config


def init_logger(cfg):
    """
    Create logger instance from config data
    """
    # initialize and configure a custom logger
    if cfg.log_config is not None:
        logging.config.fileConfig(cfg.log_config)
    else:
        logging.basicConfig(
            level=cfg.log_level,
            format='%(asctime)s %(name)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
    _logger = logging.getLogger(cfg.log_name)
    _logger.setLevel(cfg.log_level)
    _logger.name = cfg.log_name
    return _logger
