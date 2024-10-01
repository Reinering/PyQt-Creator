#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


import os, sys
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor


class ThreadPool():
    def __init__(self, max_workers=5):
        self.max_workers = max_workers

    def init(self):
        self.pool = ThreadPoolExecutor(max_workers=self.max_workers)

    def submit(self, func, *args):
        if len(args) > 0:
            th = self.pool.submit(func, args)
        else:
            th = self.pool.submit(func)
        return th.result()

    def shutdown(self):
        self.pool.shutdown()



TH_POOL = ThreadPool()
TH_POOL.init()


class CommandRunner:
    def __init__(self):
        self.process = None
        self.stdout = ""
        self.stderr = ""

    def setEnviron(self, **kwargs):
        for key, value in kwargs.items():
            os.environ[key] = value

    def run_command(self, cmd):
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        # 使用线程来读取输出，避免阻塞
        stdout_thread = threading.Thread(target=self._read_output, args=(self.process.stdout, "stdout"))
        stderr_thread = threading.Thread(target=self._read_output, args=(self.process.stderr, "stderr"))

        stdout_thread.start()
        stderr_thread.start()

        # 等待进程结束
        returncode = self.process.wait()

        # 等待输出读取完成
        stdout_thread.join()
        stderr_thread.join()

        if returncode == 0:
            print(f"{self.stdout}")
            return [True, f"{self.stdout}"]
        else:
            print(f"Error: {self.stderr}")
            return [False, f"Error: {self.stderr}"]

    def _read_output(self, pipe, type):
        for line in pipe:
            if type == "stdout":
                self.stdout += line
            else:
                self.stderr += line

    def stop(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()



class CommandRunner1:
    def __init__(self):
        self.process = None
        self.stdout = ""
        self.stderr = ""

    def run_command(self, cmd):
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            shell=True
        )

        # 使用线程来读取输出，实现实时日志
        stdout_thread = threading.Thread(target=self._read_output, args=(self.process.stdout, sys.stdout))
        stderr_thread = threading.Thread(target=self._read_output, args=(self.process.stderr, sys.stderr))

        stdout_thread.start()
        stderr_thread.start()

        # 等待进程结束
        returncode = self.process.wait()

        # 等待输出读取完成
        stdout_thread.join()
        stderr_thread.join()

        if returncode == 0:
            return [True, self.stdout]
        else:
            return [False, f"Error: {self.stderr}"]

    def _read_output(self, pipe, output_stream):
        for line in iter(pipe.readline, ''):
            print(line, end='', file=output_stream)
            if output_stream == sys.stdout:
                self.stdout += line
            else:
                self.stderr += line

    def stop(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()