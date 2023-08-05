import logging, sys, re
from colorama import Fore, Style
import coloredlogs, tailer
from functools import wraps

# print('hello worlds 2')

########################################################################################################################
# Create colors for the output
class MyFormatter(logging.Formatter):
    prefix = "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] [%(levelname)-5.5s] "
    FORMATS = {
        logging.ERROR: Fore.RED + prefix + Style.RESET_ALL + "%(message)s", 
        logging.DEBUG: Fore.BLUE + prefix + Style.RESET_ALL + "%(message)s",
        logging.WARNING: Fore.YELLOW + prefix + Style.RESET_ALL + "%(message)s",
        "DEFAULT": Fore.CYAN + prefix + Style.RESET_ALL + "%(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record) 


########################################################################################################################
# Log to console and to file
class MCLogger(object):
	log_inst = None 
	logfilepath = ""
	config = []

	# def read_file(last_n_rows):
	def __init__(self, out_filename):
		self._filename = out_filename

		self._setupLogger()

	################################################################################################
	# Get last n_rows from the log
	def read_log_file(self, last_n_rows = 20):
		with open(self._filename, 'r') as file:
			last_lines = tailer.tail(file, last_n_rows)
		return last_lines
	
	################################################################################################
	# Get last n_rows from the log
	def read_log_file_as_text(self, last_n_rows = 20):
		last_lines = self.read_log_file(last_n_rows)
		for index, line in enumerate(last_lines):
			last_lines[index] = re.sub(r'\x1b\[.+?m', '', last_lines[index], flags=re.MULTILINE )
		return last_lines

	################################################################################################
	# Configure logger
	def _setupLogger(self):
		self.log_inst = logging.getLogger(__name__)

		custom_formatter = MyFormatter()
		self.log_inst.setLevel(logging.DEBUG)

		fileHandler = logging.FileHandler( self._filename)
		fileHandler.setFormatter(custom_formatter)
		self.log_inst.addHandler(fileHandler)

		consoleHandler = logging.StreamHandler(sys.stdout)
		consoleHandler.setFormatter(custom_formatter)
		self.log_inst.addHandler(consoleHandler)
		self.log_inst.read_log_file_as_text = self.read_log_file_as_text
		self.log_inst.read_log_file  = self.read_log_file  

		# return self.log_inst

	################################################################################################
	# Main function to call
	# def getLogger(self): 
	# 	if self.log_inst	== None:
	# 		self.log_inst	= self._setupLogger( )
	# 	return self.log_inst	 	

	def logfunc_loc(self, original_func): 
		def wrapper_func( *args, **kwargs):	 
			self.debug( f"{Fore.GREEN}>>{original_func.__module__}::{original_func.__qualname__} {Style.RESET_ALL} ARGS[{args}] KWARGS[{kwargs}]")
			return original_func(*args, **kwargs)	 
		return wrapper_func

	@classmethod
	def logfunc_cls(cls, logger_attrib_name ):
		def main_decorator(  original_func): 
			def wrapper_func( *args, **kwargs):	 
				log_ref = getattr( args[0],logger_attrib_name, None )
				if log_ref: log_ref.debug( f"{Fore.GREEN}>>{original_func.__module__}::{original_func.__qualname__} {Style.RESET_ALL}	 ARGS[{args}] KWARGS[{kwargs}]")	
				return original_func(*args, **kwargs)	 
			return wrapper_func
		return main_decorator


	def debug(self, message): self.log_inst.debug(message)
	def error(self, message): self.log_inst.error(message)
	def warning(self, message): self.log_inst.warning(message)
	def info(self, message): self.log_inst.info(message)
	
