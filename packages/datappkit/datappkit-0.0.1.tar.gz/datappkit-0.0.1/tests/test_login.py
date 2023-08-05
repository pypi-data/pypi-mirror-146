import sys
sys.path.append("/Users/baojiarui/PycharmProjects/data-service-sdk/datappkit")

from datappkit.datapp import Datapp


if __name__ == '__main__':
    datapp = Datapp()
    try:
        # test account
        # datapp.login("13333330003", "test123")
        datapp.login("17610188166", "test123")

        # prod account
        # datapp.login("18610928883", "21151091")

    except Exception as e:
        # print(e)
        pass
