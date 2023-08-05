import sys
sys.path.append("/Users/garry/PycharmProjects/data-service-sdk/datappkit")

from datapp import Datapp


if __name__ == '__main__':
    datapp = Datapp()

    file_path = datapp.download_cli(1, "/Users/garry/Downloads")
    print(file_path)

