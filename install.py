import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Flask'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Flask-Cors'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sqlalchemy'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-python'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'crcmod'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyserial'])