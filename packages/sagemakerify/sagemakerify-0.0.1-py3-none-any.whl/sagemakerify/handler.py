import argparse
import pickle
import json
import sys
import os
import tarfile
import logging
import importlib

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def to_pkl(data, file):
    with open(file, 'wb') as f:
        pickle.dump(data, f)

def read_pkl(file):
    if file.endswith("tar.gz"):
        with tarfile.open(file, 'r:gz') as tar:
            files = []
            for name in tar.getnames():
                f = tar.extractfile(name)
                files.append(pickle.load(f))
            return files
    else:
        with open(file, 'rb') as f:            
            return pickle.load(f)


def extract(dic,keys):
    attrs = {k: getattr(dic,k) for k in dir(dic) if k in keys}
    self = {}
    for attr in attrs:
        setattr(self,attr,attrs[attr])
    return self

if __name__=='__main__':      
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--output-data-dir', type=str, default=os.environ.get('SM_OUTPUT_DATA_DIR'))
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))    
    parser.add_argument('--data', type=str, default=os.environ['SM_CHANNEL_DATA'])
    parser.add_argument('--code', type=str, default=os.environ['SM_CHANNEL_CODE'])    
    parser.add_argument('--data-file', type=str, default='')
    parser.add_argument('--module', type=str)

    args, remaining = parser.parse_known_args()
    
    logger.info(f'Received arguments {args}')
    logger.info(f'Additional received arguments {remaining}')
      
    data = read_pkl(os.path.join(args.data, 'data.pkl'))
        
    # Each job could be executed using multiple EC2 instances, and in order to be able to manage what is executed on each instance, 
    # SageMaker provides us the following configuration file in which we can find the number of hosts the cluster has, as well as
    # the current host numbuer on which the script is being executed
    resourceconfig_file = '/opt/ml/input/config/resourceconfig.json'
    if os.path.exists(resourceconfig_file):        
        with open(resourceconfig_file) as f:
            config = json.load(f)

        logger.info(f"hosts:{config['hosts']}")
        num_hosts = len(config['hosts'])
        current_host = int(config['current_host'].split('-')[-1])
        logger.info(f'num hosts: {data["num_hosts"]}')
        logger.info(f'current host: {data["current_host"]}')
    else:
        num_hosts = 1
        current_host = 1
    
    # Set some usefull variables and functions as attributes of self object
    # This way we could access or use them on the scripts with the logic that we are going to execute  using SageMaker jobs
    """
    data['args'] = args
    data['remaining_args'] = remaining
    data['to_pkl'] = to_pkl
    data['read_pkl'] = read_pkl    
    data['extract'] = extract
    data['num_hosts'] = num_hosts
    data['current_host'] = current_host
    """

    # Import Python script provided with the logic to execute
    sys.path.insert(1, '/opt/ml/processing/dependencies')
    sys.path.insert(1, args.code)
    script = importlib.import_module(args.module)  
    
    os.chdir('/opt/ml')
    if type(data) is tuple:
        
        # Convert each argument to original data type
        for t in data:
            if hasattr(t,'get_data_types'):
                data_types = t.get_data_types()
                print(f'data_types = {data_types}')

                for attr in data_types:
                    attribute = attr.replace('-','_')
                    remaining[attribute] = data_types[attr](remaining[attribute])

        # Remove data_types object from data parameters
        data = [t for t in data if not hasattr(t,'get_data_types')]
                    
        data = getattr(script, args.module)(*data, **remaining)      
    else:
        data = getattr(script, args.module)(data, **remaining)
    
    # Save data object to be able to use it in future pipeline steps or jobs
    output_file = 'data.pkl' if num_hosts==1 else f'data-{current_host}.pkl'
    to_pkl(data, os.path.join(args.model_dir, output_file))