import logging

from rss_reader.utils.log import SystemLog


def test_system_log(caplog):
    """ Tests if sys_log logs in a given format and level """

    sys_log = SystemLog('%(levelname)%s : (message)s')
    sys_log.logger.warning('Some warning')
    assert 'Some warning' in caplog.text
    caplog.set_level(logging.INFO)
    sys_log.logger.info('Some info')
    assert 'Some info' in caplog.text
