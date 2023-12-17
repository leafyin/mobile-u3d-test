# encoding=utf-8
import platform
import subprocess
import threading


class Runner:

    def __init__(self, exec_script):
        # adb devices
        self.devices = []
        system = platform.system()
        if system == 'Windows':
            cmd = ".\init.bat"
        elif system in ['Darwin', 'Linux']:
            cmd = "sh ./init.sh"
        else:
            return
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        stdout = process.stdout.readlines()
        # 去掉头部尾部
        stdout.pop(0)
        stdout.pop(len(stdout) - 1)
        for i in range(len(stdout)):
            if ":" or "emulator" in stdout[i]:
                self.devices.append(stdout[i].split("device")[0].strip("\t"))
        print(f"{len(self.devices)} devices have been found {self.devices}")

        def _exec_(d):
            subprocess.Popen(f"python {exec_script} {d}", stdout=subprocess.PIPE, shell=True, encoding='utf-8')

        # create thread
        for device in self.devices:
            thread = threading.Thread(target=_exec_, args=(f"{device}",))
            thread.start()


if __name__ == '__main__':
    runner = Runner("AndroidBase.py")
