from sys import platform
from subprocess import call
import os

if platform == "linux" or platform == "linux32":
    call(["cd", ".\\src"])
    call(["chmod","+x","start.sh"])
    call("./start.sh")
elif platform == "win32":
    proto_path = ".\\protos"
    # call(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])
    for filename in os.listdir(os.getcwd() + proto_path):
        f = os.path.join(proto_path, filename)
        print( f"Generating grpc files for {filename}")
        call(["python", "-m", "grpc_tools.protoc", "-I.\\protos", "--python_out=.", "--grpc_python_out=.", f"{filename}"])
    call(["git", "lfs", "pull"])
    # call("run_client.bat")