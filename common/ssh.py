# coding=utf-8
import paramiko
from scp import SCPClient

class SSH(object):

    def __init__(self):
        self.client = paramiko.SSHClient()

    def authSSH(self, host, port, usr, pwd):
        """
        :param host:
        :param port:
        :param usr:
        :param pwd:
        :return:
        """
        try:
            # key = paramiko.RSAKey.from_private_key_file(pkeyFile, password=pkeyPwd)
            # self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 通过公共方式进行认证 (不需要在known_hosts 文件中存在)
            # self.client.connect(host, port, username=usr, password=pwd, pkey=key)
            self.client.connect(host, port=port, username=usr, password=pwd)
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print("ssh登录错误：", e)
            raise paramiko.ssh_exception.NoValidConnectionsError
        except TimeoutError as e:
            print("登录超时：", e)
            raise TimeoutError
        except ConnectionError as e:
            print("建立失败：", e)
            raise ConnectionError

    def exec_cmd(self, cmd, bufsize=-1):
        """
        :param cmd:
        :param bufsize:
        :return: stdin, stdout, stderr
        """
        print(cmd)

        # return stdin, stdout, stderr
        return self.client.exec_command(cmd, bufsize)
    
    def upload(self, localpath, remotepath):
        self.sftpclient = SCPClient(self.client.get_transport(), socket_timeout=15.0)
        self.sftpclient.put(localpath, remotepath)

    def download(self, localpath, remotepath):
        self.sftpclient = SCPClient(self.client.get_transport(), socket_timeout=15.0)
        self.sftpclient.get(remotepath, localpath)

    def close(self):
        try:
            getattr(self, 'sftpclient')
            self.sftpclient.close()
        except AttributeError as e:
            pass

        self.client.close()




if __name__ == "__main__":
    ssh = SSH()
    ssh.close()