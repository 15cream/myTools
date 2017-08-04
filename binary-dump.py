__author__ = 'gjy'
import argparse
import Utils
import socket
import time
import os
import re
import zipfile


class Dump():

    def __init__(self):
        self.iosIP = None
        self.bundle_id = None
        self.outdir = None
        self.ipa_path = None
        self.client = None
        self.static_file_path = None

    def dumpbinary(self):
        self.connect()
        if self.ipa_path:
            Utils.printy('Installing.. ', 0)
            self.install_ipa()
            self.get_bundleid()
        Utils.printy('Decrypting.. ', 0)
        self.clutch()
        # if self.ipa_path:
        #     Utils.printy('Uninstalling.. ', 0)
        #     Utils.cmd_block(self.client, "ipainstaller -u {}".format(self.bundle_id))

    def connect(self):
        while True:
            try:
                Utils.printy('Conneting..', 0)
                self.client = Utils.set_ssh_conn(self.iosIP, "22", "root", "alpine")
                break
            except socket.error:
                time.sleep(5)
                Utils.printy_result('Operation timed out.', 0)

    def clutch(self):
        client = self.client
        clutch_i = Utils.cmd_block(client, 'clutch -i')

        clutch_app_id = -1
        for line in clutch_i.split('\n'):
            if line.find(self.bundle_id) != -1:
                clutch_app_id = int(line.split(':')[0])
                break

        if clutch_app_id != -1:
            Utils.printy('the application is encrypted, and use clutch to decrypt', 0)
            cmd = 'clutch -b ' + str(clutch_app_id)
            out = Utils.cmd_block(client, cmd)
            pat = re.compile(r'.+Finished.+to (.+)\[0m')
            for line in out.split('\n'):
                m = pat.match(line)
                if m:
                    bin_dir = '{path}/{bundle_id}'.format(path=m.group(1), bundle_id=self.bundle_id)
                    binary_name = Utils.cmd_block(client, "cd {};ls".format(bin_dir)).strip()
                    src = '{dir}/{binary}'.format(dir=bin_dir, binary=binary_name)
                    if self.outdir:
                        des = '{}/{}'.format(os.path.abspath(self.outdir), self.bundle_id)
                    else:
                        des = '{}/{}'.format(os.path.abspath('.'), self.bundle_id)
                    Utils.sftp_get(self.iosIP, 22, "root", "alpine", src, des)
                    return
            Utils.printy('Failed to dump binary', 2)
        else:
            Utils.printy('the application is not encrypted', 4)

    def get_bundleid(self):
        # get plist path : Payload/*.app/Info.plist
        ipa = zipfile.ZipFile(self.ipa_path)
        pat = re.compile("Payload[/\\\][\w.]+[/\\\]Info.plist")
        for name in ipa.namelist():
            if pat.search(name):
                plist_path = name
                break
        Utils.cmd_block(self.client, "unzip -u /tmp/detect/temp.ipa {} -d /tmp/detect/".format(plist_path))
        self.bundle_id = Utils.cmd_block(self.client, 'plutil -key CFBundleIdentifier /tmp/detect/{}'
                                         .format(plist_path)).strip()

    def install_ipa(self):
        Utils.cmd_block(self.client, "mkdir /tmp/detect/")
        Utils.sftp_put(self.iosIP, 22, "root", "alpine", '/tmp/detect/temp.ipa', self.ipa_path)
        Utils.cmd_block(self.client, "ipainstaller /tmp/detect/temp.ipa")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="IPA file path")
    parser.add_argument("-i", help="App bundle id")
    parser.add_argument("-s", help="Device IP")
    parser.add_argument("-o", help="Outdir to put binary file. Default .")
    args = parser.parse_args()
    dump = Dump()

    if args.s:
        dump.iosIP = args.s
    else:
        print "Specify the IP of your device"
        exit(0)

    if args.f:
        if not os.path.exists(args.f):
            Utils.printy_result('No such file ', 0)
        elif not args.f.endswith("ipa"):
            Utils.printy_result('Not ipa file ', 0)
        dump.ipa_path = args.f
    elif args.i:
        dump.bundle_id = args.i
    else:
        print "Specify either IPA path of app to be installed or BundleID of app already installed on device"
        exit(0)

    if args.o:
        dump.outdir = args.o

    dump.dumpbinary()

