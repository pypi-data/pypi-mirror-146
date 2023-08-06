from robertcommonio.system.io.file import FileType, FileConfig, FileAccessor
from robertcommonbasic.basic.dt.utils import parse_time
import re
import pyzipper
from io import BytesIO

def test_csv():
    accessor = FileAccessor(FileConfig(PATH='E:/test.csv', MODE=FileType.CSV))
    accessor.save('ss')

def test_zip_csv():
    accessor = FileAccessor(FileConfig(PATH=r'E:\DTU\real\testdtu\20210526\databackup_202105261405.zip', PSW='123456', MODE=FileType.AES_ZIP))
    results = accessor.read()
    for k, v in results.items():
        time = re.sub(r'[^0-9]+', '', k.strip())
        content = v.decode()
        body = {parse_time(time).strftime('%Y-%m-%d %H:%M:%S'): content}
        pp = [p.split(',') for p in content.split(';')]
        print()

def test_zip_csv1():
    content = b''
    with open(r'E:\DTU\real\testdtu\20210526\databackup_202105261430.zip', 'rb') as f:
        content = f.read()

    accessor = FileAccessor(FileConfig(PATH=BytesIO(content), PSW='123456',
                                       MODE=FileType.AES_ZIP))
    results = accessor.read()
    for k, v in results.items():
        print(k)
    results = {}
    with pyzipper.AESZipFile(BytesIO(content)) as zip:
        for file in zip.namelist():
            results[file] = zip.read(file)
    print(results)


test_zip_csv1()