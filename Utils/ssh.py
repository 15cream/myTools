import paramiko
import time
import Utils


def set_ssh_conn(ip, port, username, password):
    c = paramiko.SSHClient()
    c.load_system_host_keys()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(ip, int(port), username=username, password=password)
    return c


def cmd_block(client, cmd):
        while True:
            try:
                stdin, out, err = client.exec_command(cmd)
                break
            except Exception, e:
                time.sleep(5)
        if type(out) is tuple:
            out = out[0]
        str = ''
        for line in out:
            str += line
        return str


def sftp_get(ip, port, username, password, remote_file, local_path):
    # -----set up sftp to get decrypted ipa file-----
    while True:
        try:
            Utils.printy("Pull {} to {}".format(remote_file, local_path), 0)
            t = paramiko.Transport(ip, port)
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.get(remote_file, local_path)
            t.close()
            break
        except Exception, e:
            print e
            time.sleep(5)


def sftp_put(ip, port, username, password, remote_path, local_file):
    while True:
        try:
            t = paramiko.Transport(ip, port)
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)
            Utils.printy("Push {} to {}".format(local_file, remote_path), 0)
            sftp.put(localpath=local_file, remotepath=remote_path)
            t.close()
            break
        except:
            time.sleep(5)

