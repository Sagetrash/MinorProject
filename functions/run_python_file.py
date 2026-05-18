import os
import subprocess


def run_python_file(working_directory, file_path: str, args: list = []):
    try:
        if file_path.split(".")[-1] != "py":
            return f"the given file path {file_path} is not a python file"
        abspath = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(abspath, file_path))
        if not os.path.commonpath([target, abspath]) == abspath:
            return f"the given path {target} is out of permitted scope"
        
        if not os.path.isfile(target):
            return f"the given file path {file_path}, either doesnt exist or is not a regular file"
        
        abs_file_path = os.path.abspath(target)
        command = ["python", abs_file_path]
        command.extend(args)
        job = subprocess.run(args=command, capture_output=True, text=True, timeout=30)
        if job.returncode != 0:
            return f"process exited with return code {job.returncode}"
        if not job.stderr and not job.stdout:
            return f"process produced no output: return code: {job.returncode}"
        return f""" return code: {job.returncode} \n STD_out: "{job.stdout}" \n std_err: {job.stderr}"""
    except Exception as e:
        return f"error running python file {file_path}: {str(e)}"


if __name__ == "__main__":
    pass
