import math


# 计算经纬度距离，lon结尾的是经度，lat结尾的是纬度
def distance(leftlon,leftlat,rightlon,rightlat):
    EARTH_RADIUS = 6371000.0
    lon1 = ConvertDegereeToRadians(leftlon)
    lat1 = ConvertDegereeToRadians(leftlat)
    lon2 = ConvertDegereeToRadians(rightlon)
    lat2 = ConvertDegereeToRadians(rightlat)
    dlat = math.fabs(lat1-lat2)
    dlon = math.fabs(lon1-lon2)
    h = HaverSin(dlat) + math.cos(lat1) * math.cos(lat2) * HaverSin(dlon)
    dist = 2 * EARTH_RADIUS * math.asin(math.sqrt(h))
    return dist

# 根据距离和方位角计算经纬度
def GetJinWeiDu(azimuth, dist,lon,lat):
    EARTH_RADIUS = 6371000.0
    c = dist / EARTH_RADIUS
    azimuth = ConvertDegereeToRadians(azimuth);
    x = 90.0 - lat
    x = ConvertDegereeToRadians(x);
    d = math.cos(x) * math.cos(c) + math.sin(x) * math.sin(c) * math.cos(azimuth);
    d = math.acos(d);
    C = math.asin(math.sin(c) * math.sin(azimuth) / math.sin(d));
    d = ConvertRadiansToDegeree(d);
    C = ConvertRadiansToDegeree(C);
    return lon + C, 90 - d



def ConvertRadiansToDegeree(radians):
    return radians * 180 / math.pi


def ConvertDegereeToRadians(degrees):
    return degrees * math.pi / 180


def HaverSin(theta):
    v = math.sin(theta / 2)
    return v * v

