import sys
sys_args = sys.argv[1:]

from ml_pipeline.ML_Models import init_Models

def run( *sys_args ):
    init_Models()    

run( *sys_args )

