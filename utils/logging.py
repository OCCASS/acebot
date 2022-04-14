import logging


def init_logger():
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)
