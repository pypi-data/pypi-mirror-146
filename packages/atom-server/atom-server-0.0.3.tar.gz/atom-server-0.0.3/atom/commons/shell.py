import subprocess


def run(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stdout.decode("utf-8"), result.stderr.decode("utf-8")
