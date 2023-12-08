# encoding=utf-8
import subprocess
import threading


class Runner:

    def __init__(self, exec_script):
        # adb devices
        self.devices = []
        process = subprocess.Popen("sh ./init.sh", stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        stdout = process.stdout.readlines()
        for i in range(len(stdout)):
            if i == 0:
                continue
            if ":" in stdout[i]:
                self.devices.append(stdout[i].split("device")[0].strip("\t"))

        def _exec_(d, packagename):
            subprocess.Popen(f"python3 {exec_script} {d} {packagename}", stdout=subprocess.PIPE, shell=True, encoding='utf-8')

        # create thread
        for device in self.devices:
            thread = threading.Thread(target=_exec_, args=(f"{device}", "---"))
            thread.start()


if __name__ == '__main__':
    runner = Runner("")
