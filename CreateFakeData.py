import random
import Distance


def read_find_data(num):
    sensor_ids = []
    sensor_nums = []
    with open("F:/Find Data/"+str(num)+".txt", 'r') as f:
        for s in f.readlines():
            if s == "":
                break
            x = s.split(';')
            sensor_ids.append(int(x[0]))
            sensor_nums.append(int(x[1]))
    return sensor_ids, sensor_nums


def read_sensor_location():
    sensor_locations = []
    with open("sensor_location.txt", 'r') as f:
        for s in f.readlines():
            if s == "":
                break
            x = s.split(';')
            sensor_locations.append([float(x[0]), float(x[1])])
    return sensor_locations


def chose_god_and_bad(begin=317, good=40, bad=20):
    index = [i for i in range(begin, good + bad + begin)]
    random.shuffle(index)
    good_cars = [index[i] for i in range(good)]
    bad_cars = [index[i] for i in range(good, good+bad)]
    return good_cars, bad_cars


def add_data_sensordata(file_num, car_id, car_x, car_y, sensor_id, sensor_x, sensor_y, dist):
    with open("F:/Sensor Data/" + str(file_num)+'.txt', 'a') as f:
        # s = str(car_id) + ';' + str(car_x) + ';' + str(car_y) + ';'+sensor_id + ';'+sensor_x + ';'+sensor_y + ';' + dist
        s = "%d;%.15f;%.15f;%d;%.15f;%.15f;%.15f\n"%(car_id, car_x, car_y, sensor_id, sensor_x, sensor_y, dist)
        f.write(s)


def add_abnormal(car):
    with open('abnormal_id.txt', 'a') as f:
        for c in car:
            f.write(str(c) + '\n')


def add_normal(car):
    with open('normal_id.txt', 'a') as f:
        for c in car:
            f.write(str(c) + '\n')


if __name__ == '__main__':
    '''
    add_normal(good_car)
    add_abnormal(bad_car)
    print('good_car 编号：')
    print(good_car)
    print('bad_car 编号:')
    print(bad_car)
    '''
    good_car, bad_car = chose_god_and_bad()
    sensor_location = read_sensor_location()
    for filenum in range(2, 9):
        senor_id, sensor_num = read_find_data(filenum)
        print('第', filenum, '个周期')
        print('good')
        for car_index in good_car:
            s_num = random.randint(32, 59)
            s_id = senor_id[s_num]
            s_x = sensor_location[s_id][0]
            s_y = sensor_location[s_id][1]
            for time in range(7):
                r_azimuth = random.uniform(0, 360)
                r_dist = random.uniform(0, 80)
                fake_x, fake_y = Distance.GetJinWeiDu(r_azimuth, r_dist, s_x, s_y)
                add_data_sensordata(filenum, car_index, fake_x, fake_y, s_id, s_x, s_y,
                                    Distance.distance(s_x, s_y, fake_x, fake_y))
                # print(Distance.distance(s_x, s_y, fake_x, fake_y))
                print(car_index, ';', fake_x, ';', fake_y, ';', s_id, ';', s_x, ';', s_y, sep='')
        print('bad')
        for car_index in bad_car:
            s_num = random.randint(32, 59)
            s_id = senor_id[s_num]
            s_x = sensor_location[s_id][0]
            s_y = sensor_location[s_id][1]
            for time in range(6):
                r_azimuth = random.uniform(0, 360)
                r_dist = random.uniform(0, 80)
                fake_x, fake_y = Distance.GetJinWeiDu(r_azimuth, r_dist, s_x, s_y)
                add_data_sensordata(filenum, car_index, fake_x, fake_y, s_id, s_x, s_y,
                                    Distance.distance(s_x, s_y, fake_x, fake_y))
                # print(Distance.distance(s_x, s_y, fake_x, fake_y))
                print(car_index, ';', fake_x, ';', fake_y, ';', s_id, ';', s_x, ';', s_y, sep='')
