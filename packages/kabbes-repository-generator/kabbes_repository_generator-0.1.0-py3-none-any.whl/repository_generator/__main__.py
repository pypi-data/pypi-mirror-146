import sys
sys_args = sys.argv[1:]

from repository_generator.repository_generator import run
run( *sys_args )
