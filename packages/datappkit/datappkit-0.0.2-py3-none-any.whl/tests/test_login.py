import sys
sys.path.append("/Users/baojiarui/PycharmProjects/data-service-sdk")

from datappkit.datapp import Datapp


if __name__ == '__main__':
    datapp = Datapp()
    # test account
    # datapp.login("13333330003", "test123")
    datapp.login("17610188166", "test123")
