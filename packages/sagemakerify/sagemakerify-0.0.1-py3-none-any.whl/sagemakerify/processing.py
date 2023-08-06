import inspect
import sagemaker_utils
from time import gmtime, strftime
from sagemaker.processing import Processor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemakerify import utils, globals, handler, globals
from sagemakerify.data_types import DataTypes

def processing_job(libraries, base_job_name=None, base_image = None, secret = None, dependencies = None, 
                  image_name =None, image_s3_prefix = None, image_uri = None,
                  others=None, data_s3_prefix = None, code_s3_prefix = None, codebuild_role = None, session = None,
                  instance_count = None, instance_type = None, image_env = None,
                  role = None, volume_size_in_gb = None, max_runtime_in_seconds = None):

    
    base_image = globals.DEFAULTS.base_image if base_image is None else base_image
    secret = globals.DEFAULTS.secret if secret is None else secret
    codebuild_role = globals.DEFAULTS.codebuild_role if codebuild_role is None else codebuild_role
    session = globals.DEFAULTS.session if session is None else session
    instance_count = globals.DEFAULTS.instance_count if instance_count is None else instance_count
    instance_type = globals.DEFAULTS.instance_type if instance_type is None else instance_type
    role = globals.DEFAULTS.role if role is None else role
    volume_size_in_gb = globals.DEFAULTS.volume_size_in_gb if volume_size_in_gb is None else volume_size_in_gb
    max_runtime_in_seconds = globals.DEFAULTS.max_runtime_in_seconds if max_runtime_in_seconds is None else max_runtime_in_seconds
    build_image = image_uri is None

    role = utils.get_execution_role(role)
        
    if instance_count is None or instance_count <= 0:
        raise Exception('instance_count is required and must be grather than 0')
    elif instance_type is None:
        raise Exception('instance_type is required')
    elif role is None:
        raise Exception('role is required')
    elif volume_size_in_gb is None or volume_size_in_gb <5:
        raise Exception('volume_size_in_gb is required and must be grather or equal to 5 GB')
    elif max_runtime_in_seconds is None or max_runtime_in_seconds <= 0:
        raise Exception('max_runtime_in_seconds is required and must be grather than 0')
    elif (code_s3_prefix is None or len(code_s3_prefix)==0) and globals.DEFAULTS.bucket is None:
        raise Exception('code_s3_prefix or default bucket is required')
    elif (data_s3_prefix is None or len(data_s3_prefix)==0) and globals.DEFAULTS.bucket is None:
        raise Exception('data_s3_prefix or default bucket is required')

    
    if build_image:
        #Create docker image
        if base_image is None:
            raise Exception('base_image is required')
        elif codebuild_role is None:
            raise Exception('codebuild_role is required or set it globally')
        elif (image_s3_prefix is None or len(image_s3_prefix)==0) and globals.DEFAULTS.bucket is None:
            raise Exception('image_s3_prefix or default bucket is required')
    
        if image_s3_prefix is None or len(image_s3_prefix)==0:            
            image_s3_prefix = f's3://{globals.DEFAULTS.bucket}/{globals.DEFAULTS.prefix}/docker_images'

    if code_s3_prefix is None:
            code_s3_prefix = f's3://{globals.DEFAULTS.bucket}/{globals.DEFAULTS.prefix}/code'

    if data_s3_prefix is None:
                data_s3_prefix = f's3://{globals.DEFAULTS.bucket}/{globals.DEFAULTS.prefix}/data'

    base_job_name = base_job_name.lower() if base_job_name is not None else f'{globals.DEFAULTS.prefix}'.lower()
        

    def processing(func):         
        # Create a file with the code received
        function_name, function_file = utils.create_function_file(func)            

        # Create handler code
        handler_file = f'{globals.DEFAULTS.source_code_location}/handler.py'        
        sagemaker_utils.make_dirs(handler_file)        
        with open(handler_file, 'w') as f:
            f.write(inspect.getsource(handler))


        prefix_job_name = f'{base_job_name}-{function_name}'.lower().replace('_','-')

        if build_image:
            #Create docker image                        
            parameters = {
                'image_name': image_name if image_name is not None else prefix_job_name,
                'base_image': base_image,
                's3_path': image_s3_prefix,
                'role': codebuild_role,
                'wait': True}

            if libraries is not None:
                parameters['libraries'] = libraries
            
            if secret is not None:
                parameters['secret'] = secret

            if dependencies is not None:
                parameters['dependencies'] = dependencies
            else:
                parameters['dependencies'] = []

            parameters['dependencies'].append((handler_file,'/opt/ml/code/handler.py'))

            if others is not None:
                parameters['others'] = others

            if image_env is not None:
                parameters['env'] = image_env
            else:
                parameters['env'] = {}
            
            parameters['env']['SAGEMAKER_SUBMIT_DIRECTORY'] = '/opt/ml/code'
            parameters['env']['SAGEMAKER_PROGRAM'] = 'handler.py'

            hash = utils.dict_hash(parameters)
            if parameters['image_name'] not in globals.LAST_CONFIG \
                or (parameters['image_name'] in globals.LAST_CONFIG \
                    and globals.LAST_CONFIG[parameters['image_name']]['hash'] != hash):
                
                image_uri = sagemaker_utils.create_docker_image(**parameters)       
                
                globals.LAST_CONFIG[parameters['image_name']]={
                    'uri': image_uri,
                    'hash': hash
                }
            else:
                image_uri = globals.LAST_CONFIG[parameters['image_name']]['uri']
            

        #Create a Processor
        processor = Processor(            
            image_uri = image_uri,
            role = role,
            instance_count = instance_count,
            instance_type = instance_type, 
            entrypoint = ['python3',f'/opt/ml/code/handler.py'],
            env = {'SM_OUTPUT_DATA_DIR':'/opt/ml/processing/output',
                 'SM_MODEL_DIR':'/opt/ml/processing/output',
                 'SM_CHANNEL_DATA':'/opt/ml/processing/input',
                 'SM_CHANNEL_CODE':'/opt/ml/processing/input/code'},
            volume_size_in_gb = volume_size_in_gb,
            max_runtime_in_seconds = max_runtime_in_seconds
        )

        def wrapper(*data, **kwargs):    
            return_type = kwargs.get('return_type',None)   

            if return_type is None:
                job_name = f'{prefix_job_name}-{strftime("%H-%M-%S", gmtime())}'.lower()

                # Set arguments        
                arguments_types = DataTypes()
                arguments = []
                for k in kwargs:
                    if utils.is_builtin_class_instance(kwargs[k]): 
                        key = f"--{k.replace('_','-')}"
                        arguments_types.set_type(key, kwargs[k])
                        arguments.append(key)
                        arguments.append(kwargs[k])
                    else:
                        raise Exception(f'{type(kwargs[k])} is not supported')   
                
                if len(arguments)>0:
                    data = data + (arguments_types,)

                # Serialize data
                data_file = utils.to_pkl(data,f'{globals.DEFAULTS.source_code_location}/data.pkl')

                # Upload function code to S3        
                function_s3_path = sagemaker_utils.upload(function_file, f'{code_s3_prefix}/{job_name}', session = session.boto_session)
                
                # Upload data to S3            
                data_s3_path = sagemaker_utils.upload(data_file, f'{data_s3_prefix}/{job_name}', session = session.boto_session)
                
                             
                
                arguments.append('--module')
                arguments.append(function_name)

                print(f'arguments = {arguments}')

                processor.run(job_name = job_name,
                            inputs = [ProcessingInput(input_name='data',
                                                    source=data_s3_path,
                                                    destination='/opt/ml/processing/input'),
                                    ProcessingInput(input_name='code',
                                                    source=function_s3_path,
                                                    destination='/opt/ml/processing/input/code')],
                            outputs = [ProcessingOutput(output_name='output',
                                                        source=f'/opt/ml/processing/output',
                                                        destination=f'{data_s3_prefix}/processed/{job_name}')],
                            arguments = arguments)

                data_s3_path = sagemaker_utils.list_s3(processor.latest_job.outputs[0].destination)[0]
                
                return sagemaker_utils.read_pkl(data_s3_path, session = session.boto_session)            

            elif return_type == 'processor':
                return processor

            elif return_type == 'image_uri':
                return image_uri
        
        return wrapper 
    return processing

