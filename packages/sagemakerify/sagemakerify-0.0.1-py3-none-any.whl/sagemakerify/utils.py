import ast
import json
import astor
import pickle
import inspect
import hashlib
import sagemaker_utils
from sagemakerify import globals
from sagemaker import Session
from sagemaker import get_execution_role as sm_get_execution_role

class Defaults():
    def __init__(self, 
                 base_image = 'python:3.7.6-slim-buster', 
                 session = Session(), 
                 secret = None, 
                 codebuild_role = None,
                 bucket = Session().default_bucket(),
                 prefix = 'sagemakerify',
                 role = None,
                 instance_count = 1,
                 instance_type = 'ml.m5.2xlarge', 
                 volume_size_in_gb = 5, 
                 max_runtime_in_seconds = 60*60*5,
                 source_code_location = '.code'):
        self.source_code_location = source_code_location
        self.base_image = base_image
        self.session = session
        self.secret = secret
        self.codebuild_role = codebuild_role
        self.bucket = bucket
        self.prefix = prefix
        self.role = role
        self.instance_count = instance_count
        self.instance_type = instance_type
        self.volume_size_in_gb = volume_size_in_gb
        self.max_runtime_in_seconds = max_runtime_in_seconds

globals.DEFAULTS = Defaults()

def set_defaults(**kwargs):    
    globals.DEFAULTS = Defaults(**kwargs)
    

def get_execution_role(role):
    try:
        if role is None:
            role = sm_get_execution_role()
        return role
    except:
        raise Exception('You have to specify an execution role')

def get_decorators(cls):
    target = cls
    decorators = {}

    def visit_FunctionDef(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ''
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id

            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators
    
def get_function_code(func):
    code = {}

    def visit_FunctionDef(node):          
        node.decorator_list = []  
        code[node.name] = astor.to_source(node)        

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(func)))

    return code

def create_function_file(func):
    code = get_function_code(func)
        
    if len(code)!=1:
        raise Exception('Just one function is supported')

    function_name = list(code.keys())[0]
    function_file = f'{globals.DEFAULTS.source_code_location}/{function_name}.py'
    sagemaker_utils.make_dirs(function_file)
    with open(function_file,'w') as f:
        f.write(code[function_name])

    return function_name, function_file

def to_pkl(data, file):
    sagemaker_utils.make_dirs(file)
    with open(file, 'wb') as f:
        pickle.dump(data, f)
    return file

def dict_hash(dictionary):
    dhash = hashlib.md5()

    encoded = json.dumps(dictionary, sort_keys=True).encode()

    dhash.update(encoded)

    return dhash.hexdigest()

def is_builtin_class_instance(obj):
    return obj.__class__.__module__ == 'builtins'
