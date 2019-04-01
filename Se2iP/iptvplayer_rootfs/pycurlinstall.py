#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform
import os
import re
import sys
import time

INSTALL_BASE = '/iptvplayer_rootfs/'
MSG_FORMAT = "\n\n=====================================================\n{0}\n=====================================================\n"

def printWRN(txt):
    print(MSG_FORMAT.format(txt))
    
def printMSG(txt):
    print(MSG_FORMAT.format(txt))

def printDBG(txt):
    print(str(txt))

def ReadGnuMIPSABIFP(elfFileName):
    SHT_GNU_ATTRIBUTES=0x6ffffff5
    SHT_MIPS_ABIFLAGS=0x7000002a
    Tag_GNU_MIPS_ABI_FP=4
    Val_GNU_MIPS_ABI_FP_ANY=0
    Val_GNU_MIPS_ABI_FP_DOUBLE=1
    Val_GNU_MIPS_ABI_FP_SINGLE=2
    Val_GNU_MIPS_ABI_FP_SOFT=3
    Val_GNU_MIPS_ABI_FP_OLD_64=4
    Val_GNU_MIPS_ABI_FP_XX=5
    Val_GNU_MIPS_ABI_FP_64=6
    Val_GNU_MIPS_ABI_FP_64A=7
    Val_GNU_MIPS_ABI_FP_NAN2008=8

    def _readUint16(tmp):
        return ord(tmp[1]) << 8 | ord(tmp[0])
    
    def _readUint32(tmp):
        return ord(tmp[3]) << 24 | ord(tmp[2]) << 16 | ord(tmp[1]) << 8 | ord(tmp[0])
    
    def _readLeb128(data, start, end):
        result = 0
        numRead = 0
        shift = 0
        byte = 0

        while start < end:
            byte = ord(data[start])
            numRead += 1

            result |= (byte & 0x7f) << shift

            shift += 7
            if byte < 0x80:
                break
        return numRead, result
    
    def _getStr(stsTable, idx):
        val = ''
        while stsTable[idx] != '\0':
            val += stsTable[idx]
            idx += 1
        return val
    
    Val_HAS_MIPS_ABI_FLAGS = False
    Val_GNU_MIPS_ABI_FP = -1
    with open(elfFileName, "rb") as file:
        # e_shoff - Start of section headers
        file.seek(32)
        shoff = _readUint32(file.read(4))
    
        # e_shentsize - Size of section headers
        file.seek(46)
        shentsize = _readUint16(file.read(2))
        
        # e_shnum -  Number of section headers
        shnum = _readUint16(file.read(2))
        
        # e_shstrndx - Section header string table index
        shstrndx = _readUint16(file.read(2))
        
        # read .shstrtab section header
        headerOffset = shoff + shstrndx * shentsize
        
        file.seek(headerOffset + 16)
        offset = _readUint32(file.read(4))
        size = _readUint32(file.read(4))
        
        file.seek(offset)
        secNameStrTable = file.read(size)
        
        for idx in range(shnum):
            offset = shoff + idx * shentsize
            file.seek(offset)
            sh_name = _readUint32(file.read(4))
            sh_type = _readUint32(file.read(4))
            if sh_type == SHT_GNU_ATTRIBUTES:
                file.seek(offset + 16)
                sh_offset = _readUint32(file.read(4))
                sh_size   = _readUint32(file.read(4))
                file.seek(sh_offset)
                contents = file.read(sh_size)
                p = 0
                if contents.startswith('A'):
                    p += 1
                    sectionLen = sh_size -1
                    while sectionLen > 0:
                        attrLen = _readUint32(contents[p:])
                        p += 4
                        
                        if attrLen > sectionLen:
                            attrLen = sectionLen
                        elif attrLen < 5:
                            break
                        sectionLen -= attrLen
                        attrLen -= 4
                        attrName =  _getStr(contents, p)
                        
                        p += len(attrName) + 1
                        attrLen -= len(attrName) + 1
                        
                        while attrLen > 0 and p < len(contents):
                            if attrLen < 6:
                                sectionLen = 0
                                break
                            tag = ord(contents[p])
                            p += 1
                            size = _readUint32(contents[p:])
                            if size > attrLen:
                                size = attrLen
                            if size < 6:
                                sectionLen = 0
                                break
                                
                            attrLen -= size
                            end = p + size - 1
                            p += 4
                            
                            if tag == 1 and attrName == "gnu": #File Attributes
                                while p < end:
                                    # display_gnu_attribute
                                      numRead, tag = _readLeb128(contents, p, end)
                                      p += numRead
                                      if tag == Tag_GNU_MIPS_ABI_FP:
                                        numRead, val = _readLeb128(contents, p, end)
                                        p += numRead
                                        Val_GNU_MIPS_ABI_FP = val
                                        break
                            elif p < end:
                                p = end
                            else:
                                attrLen = 0
            elif sh_type == SHT_MIPS_ABIFLAGS:
                Val_HAS_MIPS_ABI_FLAGS = True
    return Val_HAS_MIPS_ABI_FLAGS, Val_GNU_MIPS_ABI_FP

# check free size in the rootfs
s = os.statvfs(INSTALL_BASE) if os.path.isdir(INSTALL_BASE) else os.statvfs("/")
freeSpaceMB = s.f_bfree * s.f_frsize / (1024*1024) # in KB
availSpaceMB = s.f_bavail * s.f_frsize / (1024*1024) # in KB

requiredFreeSpaceMB = 5
printDBG("Free space %s MB in rootfs" % (availSpaceMB))
if availSpaceMB < requiredFreeSpaceMB:
    msg = "Not enough disk space for installing PyCurl libraties!\nAt least %s MB is required.\nYou have %s MB free space in the rootfs.\nDo you want to continue anyway?" % (requiredFreeSpaceMB, availSpaceMB)
    answer = ''
    while answer not in ['Y', 'N']:
        answer = raw_input(MSG_FORMAT.format(msg) + "\nY/N: ").strip().upper()
        msg = ''
    
    if answer != 'Y':
        raise Exception("Not enough disk space for installing PyCurl libraties!\nAt least %s MB is required." % requiredFreeSpaceMB)
    

iptvPlatform = ''
iptvOpenSSLVer = ''

machine = platform.uname()[4]

printDBG("Machine: %s" % machine)

iptvPlatform = ''
if 'armv7' in machine:  iptvPlatform = "armv7"
elif 'sh4' in machine:  iptvPlatform = "sh4"
elif 'mips' in machine: iptvPlatform = "mipsel"
elif 'x86_64' in machine: iptvPlatform = "i686"
elif 'i686' in machine: iptvPlatform = "i686"

if iptvPlatform == '':
    with open('/proc/cpuinfo', "r") as file:
        data = file.read().lower()
        if " mips" in data: 
            iptvPlatform = "mipsel"
        elif "armv7" in data:
            iptvPlatform = "armv7"

if iptvPlatform == '':
    raise Exception('Your platform has not been detected! Machine [%s].\n' % machine)

elif iptvPlatform not in ['armv7', 'sh4', 'mipsel']: 
    raise Exception('Your platform "%s" is not supported!' % iptvPlatform)


fpuType = ''
if iptvPlatform == "mipsel":
    hasAbiFlags, abiFP = ReadGnuMIPSABIFP('/lib/libc.so.6')
    if abiFP not in [-1, 0]:
        if abiFP == 3: fpuType = "soft"
        else: fpuType = "hard"
    if fpuType == '':
        raise Exception('Unknown FPU type!')
    printDBG("MIPSEL FPU TYPE [%s]" % fpuType)
else:
    fpuType = 'hard'
    
data = os.path.realpath('/lib/libc.so.6')
glibcVer = re.compile('\-([0-9\.]+?)\.so').search(data).group(1)
if glibcVer.count('.') > 1:
    glibcVer = glibcVer.rsplit('.', 1)[0]

glibcVer = float(glibcVer)
printDBG("glibc version [%s]" % glibcVer)

pyVersion = 'python%s.%s' % (sys.version_info[0], sys.version_info[1])
if pyVersion not in ['python2.7', 'python2.6']:
    raise Exception('Your python version "%s" is not supported!' % pyVersion)

#iptvPlatform
#fpuType
#availSpaceMB
#glibcVer
#pyVersion

# old hard float glibc 2.12 
# old soft float glibc 2.12
#     hard float glibc 2.21
#     soft float glibc 2.20
if iptvPlatform == 'mipsel':
    if fpuType == 'hard':
        if glibcVer >= 2.21:
            installOld = ''
        elif glibcVer >= 2.12:
            installOld = 'old_'
    elif fpuType == 'soft':
        if glibcVer >= 2.20:
            installOld = ''
        elif glibcVer >= 2.12:
            installOld = 'old_'
elif iptvPlatform == 'sh4':
    if glibcVer >= 2.19:
        installOld = ''
    elif glibcVer >= 2.10:
        installOld = 'old_'
elif iptvPlatform == 'armv7':
    if glibcVer >= 2.18:
        installOld = ''

try:
    test = installOld + ''
except Exception:
    raise Exception('Your glibc version "%s" is not supported!' % glibcVer)

installFPU = 'fpu_%s' % fpuType


pypurlPackageBaseName = 'pycurl7.43.0.2_curl7.61.0_wolfssl3.15.3'
pycurlPackageConfig = '%s_%s_%s%s' % (pyVersion, iptvPlatform, installOld, installFPU)
pycurlInstallPackage = '%s_%s.tar.gz' % (pypurlPackageBaseName, pycurlPackageConfig)

if pycurlPackageConfig not in ['python2.6_mipsel_old_fpu_hard', 'python2.6_mipsel_old_fpu_soft', 'python2.6_sh4_old_fpu_hard', \
                               'python2.7_armv7_fpu_hard', 'python2.7_mipsel_fpu_hard', 'python2.7_mipsel_fpu_soft', \
                               'python2.7_sh4_fpu_hard', 'python2.7_sh4_old_fpu_hard', 'python2.7_mipsel_old_fpu_soft', \
                               'python2.7_mipsel_old_fpu_hard']:
    raise Exception('At now there is no\n"%s"\npackage available!\nYou can request it via e-mail: IPTVPlayerE2@gmail.com' % pycurlInstallPackage)

printDBG("Slected ffmpeg package: %s" % pycurlInstallPackage)

sitePackagesPath='/usr/lib/%s/site-packages' % pyVersion
if not os.path.isdir(sitePackagesPath):
    raise Exception('Python site-packages directory "%s" does not exists!\nPlease report this via e-mail: IPTVPlayerE2@gmail.com' % sitePackagesPath)

expectedPyCurlVersion = 'PycURL/7.43.0.2 libcurl/7.61.0 wolfSSL/3.15.3'
acctionNeededBeforeInstall = 'NONE'
systemPyCurlPath = sitePackagesPath + '/pycurl.so'

if os.path.isfile(systemPyCurlPath) and not os.path.islink(systemPyCurlPath):
    ret = os.system('python -c "import sys; import pycurl; test=pycurl.version.startswith(\\"' + expectedPyCurlVersion + '\\"); sys.exit(0 if test else -1);"')
    if ret == 0:
        # same version but by copy
        acctionNeededBeforeInstall = "REMOVE_FILE"
    else:
        acctionNeededBeforeInstall = "BACKUP_FILE"
elif os.path.islink(systemPyCurlPath):
    # systemPyCurlPath is symbolic link
    linkTarget = os.path.realpath(systemPyCurlPath)
    if linkTarget != os.path.join(INSTALL_BASE, systemPyCurlPath[1:]):
        raise Exception('Error!!! Your %s is symbolc link to %s!\nThis can not be handled by this installer.\nYou can remove it by hand and try again.\n' % (systemPyCurlPath, linkTarget))
    else:
        acctionNeededBeforeInstall = "REMOVE_SYMBOLIC_LINK"

printDBG("Action needed before install %s" % acctionNeededBeforeInstall)
ret = os.system("mkdir -p %s" % INSTALL_BASE)
if ret not in [None, 0]:
    raise Exception('Creating %s failed! Return code: %s' % (INSTALL_BASE, ret))

ret = os.system('rm -f /tmp/%s' % pycurlInstallPackage)
if ret not in [None, 0]:
    raise Exception('Removing old downloaded package /tmp/%s failed! Return code: %s' % (pycurlInstallPackage, ret))

WGET = ''
for cmd in ['wget', 'fullwget', '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/bin/wget']:
    try:
        file = os.popen(cmd + ' "http://www.iptvplayer.gitlab.io/precompiled/%s/%s" -O "/tmp/%s" ' % (pypurlPackageBaseName, pycurlInstallPackage, pycurlInstallPackage))
        data = file.read()
        ret = file.close()
        if ret in [0, None]:
            WGET = cmd
            break
        else:
            printDBG("Download using %s failed with return code: %s" % ret)
    except Exception,e:
        printDBG(e)

if WGET == '':
    raise Exception('Download package %s failed!' % pycurlInstallPackage)

msg = 'Package %s ready to install.\nDo you want to proceed?' % pycurlInstallPackage
answer = ''
while answer not in ['Y', 'N']:
    answer = raw_input(MSG_FORMAT.format(msg) + "\nY/N: ").strip().upper()
    msg = ''

if answer == 'Y':
    # remove old version
    os.system('rm -rf %s/lib/libcurl.so*' % INSTALL_BASE)
    os.system('rm -rf %s/lib/libwolfssl.so*' % INSTALL_BASE)
    
    ret = os.system("mkdir -p %s && tar -xvf /tmp/%s -C %s " % (INSTALL_BASE, pycurlInstallPackage, INSTALL_BASE))
    if ret not in [None, 0]:
        raise Exception('PyCurl unpack archive failed with return code: %s' % (ret))
    
    os.system('rm -f /tmp/%s' % pycurlInstallPackage)
    
    if acctionNeededBeforeInstall in ['REMOVE_FILE', 'REMOVE_SYMBOLIC_LINK']:
        os.unlink(systemPyCurlPath)
    elif acctionNeededBeforeInstall == 'BACKUP_FILE':
        backup = '%s_backup_%s' % (systemPyCurlPath, str(time.time()))
        os.rename(systemPyCurlPath, backup)
    
    # create symlink
    os.symlink(os.path.join(INSTALL_BASE, systemPyCurlPath[1:]), systemPyCurlPath)
    
    # check if pycurl is working
    import pycurl
    if pycurl.version.startswith(expectedPyCurlVersion):
        printMSG('Done. PyCurl version "%s" installed correctly.\nPlease remember to restart your Enigma2.' % (pycurl.version))
    else:
        raise Exception('Installed PyCurl is NOT working correctly! It report diffrent version "%s" then expected "%s"' % (pycurl.version, expectedPyCurlVersion))


# cd /tmp && rm -f pycurlinstall.py && wget http://www.iptvplayer.gitlab.io/pycurlinstall.py && python pycurlinstall.py

