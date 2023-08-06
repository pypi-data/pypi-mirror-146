import sys
sys_args = sys.argv[1:]

from pypi_builder.pypi_builder import run
run( *sys_args )
