import logging as lg 


def logger(name):
	logger = lg.getLogger(name)
	sys_handler = lg.StreamHandler()
	sys_format = lg.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	sys_handler.setFormatter(sys_format)
	logger.addHandler(sys_handler)
	logger.setLevel(lg.DEBUG)

	return logger