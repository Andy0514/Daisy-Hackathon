import csv
import math


class car1:
    accel = 10*0.999
    brake = -8.2 * 0.999
    topSpeed = 10.009
    gasDuration = 1500
    tireDuration = 1250
    handling = 21


class car78:
    accel = 5 * 0.9999
    brake = -5.6 * 0.999
    topSpeed = 15.7
    gasDuration = 1500
    tireDuration = 1250
    handling = 21


class car34:
    accel = 5.51 * 0.999
    brake = -5.66 * 0.999
    topSpeed = 15
    gasDuration = 1500
    tireDuration = 1250
    handling = 21


class car56:
    accel = 6.8 * 0.999
    brake = -4.56 * 0.999
    topSpeed = 10.9
    gasDuration = 1500
    tireDuration = 1250
    handling = 21


class car2:  # worth 25%
    accel = 6.76 * 0.999
    brake = -5.53 * 0.9999
    topSpeed = 11.1
    gasDuration = 1500
    tireDuration = 1250
    handling = 21


# import CSV file as array T1

def runProgram(file_name):

    if file_name == "track_5.csv" or file_name == "track_6.csv":
        Car = car56()
    elif file_name == "track_2.csv":
        Car = car2()
    elif file_name == "track_3.csv" or file_name == "track_4.csv":
        Car = car34()
    elif file_name == "track_1.csv":
        Car = car1()
    else:
        Car = car78()

    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        T1 = list(reader)
        T1 = T1[1:]

    T1_new = []

    for i in T1:
        T1_new.append(float(i[0]))

    V1 = list()

    V1.append(0)


    #first run
    for i in range(1, len(T1_new)):

        # straight line
        if T1_new[i-1] == -1 and T1_new[i] == -1:
            V1.append(Car.topSpeed)

        elif T1_new[i-1] == -1 and T1_new[i] != -1:
            V_for_this_point = math.sqrt((T1_new[i] * Car.handling) / 1000000)

            if V_for_this_point<Car.topSpeed:
                V1.append(V_for_this_point)
            else:
                V1.append(Car.topSpeed)

        elif T1_new[i-1] != -1:
            V_for_last_point = math.sqrt((T1_new[i - 1] * Car.handling) / 1000000)

            if T1_new[i] == -1:
                V_for_this_point = V_for_last_point
            else:
                V_for_this_point = math.sqrt((T1_new[i] * Car.handling) / 1000000)

            if V_for_this_point < V_for_last_point:
                if V_for_this_point < Car.topSpeed:
                    V1.append(V_for_this_point)
                else:
                    V1.append(Car.topSpeed)
            else:
                if V_for_last_point < Car.topSpeed:
                    V1.append(V_for_last_point)
                else:
                    V1.append(Car.topSpeed)

    V1_old = V1.copy()

    for x in range(10):
        for i in range(len(V1)-1):
            max_next_v_accel = math.sqrt(pow(V1[i], 2) + 2*Car.accel)

            try:
                max_next_v_decel = math.sqrt(pow(V1[i], 2) + 2*Car.brake)
            except:
                max_next_v_decel = 0

            # if the 2nd point is faster by too much compared to the first point: reduce 2nd point speed
            if V1[i+1] > max_next_v_accel:
                V1[i+1] = max_next_v_accel

            # if the 2nd point is much lower than the 1st point, reduce first point speed
            elif V1[i+1] < max_next_v_decel:
                required = math.sqrt(pow(V1[i+1], 2) - 3*Car.brake)
                V1[i] = required

    A1 = list()
    for i in range(len(V1)-1):
        A_for_current_point = (math.pow(V1[i+1], 2) - math.pow(V1[i], 2)) / 2
        A1.append(A_for_current_point)

    current_gas = Car.gasDuration
    current_tire = Car.tireDuration
    time = 0

    pitstop_index = []

    for i in range(len(A1)):
        # for 0 acceleration, t = d/v
        if V1[i+1] == V1[i]:
            time += 1/V1[i]
        # for nonzero acceleration, t = [v(x+1)-v(x)]/a
        else:
            time += (V1[i+1] - V1[i]) / A1[i]

        if A1[i] > 0:
            current_gas -= 0.1 * pow(A1[i], 2)
        elif A1[i] < 0:
            current_tire -= 0.1 * pow(A1[i], 2)

        max_tire_waste = 0.1*pow(Car.brake, 2)
        max_gas_waste = 0.1*pow(Car.accel, 2)
        if current_gas <= max_gas_waste or current_tire <= 2*max_tire_waste:
            pitstop_index.append(i)
            time += 30
            V1[i] = 0
            current_gas = Car.gasDuration
            current_tire = Car.tireDuration

    # repeats code from above, in order to take into consideration the 0 velocity at pitstop
    for x in range(10):
        for i in range(len(V1)-1):
            max_next_v_accel = math.sqrt(pow(V1[i], 2) + 2*Car.accel)

            try:
                max_next_v_decel = math.sqrt(pow(V1[i], 2) + 2*Car.brake)
            except:
                max_next_v_decel = 0

            # if the 2nd point is faster by too much compared to the first point: reduce 2nd point speed
            if V1[i+1] > max_next_v_accel:
                V1[i+1] = max_next_v_accel

            # if the 2nd point is much lower than the 1st point, reduce first point speed
            elif V1[i+1] < max_next_v_decel:
                required = math.sqrt(pow(V1[i+1], 2) - 2*Car.brake)
                V1[i] = required

    A1 = list()
    for i in range(len(V1)-1):
        A_for_current_point = (math.pow(V1[i+1], 2) - math.pow(V1[i], 2)) / 2
        A1.append(A_for_current_point)

    # end repeat

    returnValues = [V1, A1, time, current_gas, current_tire, pitstop_index]

    return returnValues


t1 = runProgram('track_1.csv')
t2 = runProgram('track_2.csv')
t3 = runProgram('track_3.csv')
t4 = runProgram('track_4.csv')
t5 = runProgram('track_5.csv')
t6 = runProgram('track_6.csv')
t7 = runProgram('track_7.csv')
t8 = runProgram('track_8.csv')

print("Track One:   time = %fs, pitstop = %s" %(t1[2], t1[5]))
print("Track Two:   time = %fs, pitstop = %s" %(t2[2], t2[5]))
print("Track Three: time = %fs, pitstop = %s" %(t3[2], t3[5]))
print("Track Four:  time = %fs, pitstop = %s" %(t4[2], t4[5]))
print("Track Five:  time = %fs, pitstop = %s" %(t5[2], t5[5]))
print("Track Six:   time = %fs, pitstop = %s" %(t6[2], t6[5]))
print("Track Seven: time = %fs, pitstop = %s" %(t7[2], t7[5]))
print("Track Eight: time = %fs, pitstop = %s" %(t8[2], t8[5]))

tot_weighted_time = t1[2] + 0.25*(t2[2] + t3[2] + t4[2]) + 0.5*(t5[2] + t6[2]) + t7[2] + t8[2]
print("Total weighted time: %fs" % tot_weighted_time)


def writeFile(fileName, accel, pitstop):
    pitstop_to_write = [0] * 1000
    output = [["a", "pit_stop"]]
    for i in range(len(pitstop)):
        index = pitstop[i]
        pitstop_to_write[index] = 1

    for i in range(0, len(accel)):
        output.append([accel[i], pitstop_to_write[i]])

    with open(fileName, 'w') as write:
        writer = csv.writer(write)
        writer.writerows(output)


writeFile(r'C:\Users\Andy\Desktop\fitness\Input\instructions_1.csv', t1[1], t1[5])
writeFile(r'C:\Users\Andy\Desktop\fitness\Input\instructions_2.csv', t2[1], t2[5])
writeFile(r'C:\Users\Andy\Desktop\fitness\Input\instructions_3.csv', t3[1], t3[5])
writeFile(r'C:\Users\Andy\Desktop\fitness\Input\instructions_4.csv', t4[1], t4[5])
writeFile(r'C:\Users\Andy\Desktop\fitness\Input\instructions_5.csv', t5[1], t5[5])
writeFile(r'C:\Users\Andy\Desktop\fitness\Input\instructions_6.csv', t6[1], t6[5])
writeFile(r'C:\Users\Andy\Desktop\fitness\Input\instructions_7.csv', t7[1], t7[5])
writeFile(r'C:\Users\Andy\Desktop\fitness\Input\instructions_8.csv', t8[1], t8[5])

car_config = [["tire", "gas", "handling", "speed", "acceleration", "breaking"], [4, 5, 5, 2, 1, 1]]
with open(r'C:\Users\Andy\Desktop\fitness\Input\car.csv','w') as write:
    writer = csv.writer(write)
    writer.writerows(car_config)







