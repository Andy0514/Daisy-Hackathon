import csv
import math


class car:
    accel = 10 * 0.999  # tier 1
    brake = -10 * 0.999  # tier 1
    topSpeed = 9.99  # tier 1
    gasDuration = 1500  # tier 5, cost = 6
    tireDuration = 1500  # tier 5, cost = 6
    handling = 21  # tier 5, cost = 6


# import CSV file as array T1

def runProgram(file_name):
    Car = car()

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
            V_for_this_point = math.sqrt((T1_new[i] * car.handling) / 1000000)

            if V_for_this_point<Car.topSpeed:
                V1.append(V_for_this_point)
            else:
                V1.append(car.topSpeed)

        elif T1_new[i-1] != -1:
            V_for_last_point = math.sqrt((T1_new[i - 1] * car.handling) / 1000000)

            if T1_new[i] == -1:
                V_for_this_point = V_for_last_point
            else:
                V_for_this_point = math.sqrt((T1_new[i] * car.handling) / 1000000)

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

    for i in range(5):
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


    current_gas = Car.gasDuration
    current_tire = Car.tireDuration
    time = 0


    pitstop_index = []

    for i in range(len(A1)):
        # for 0 acceleration, t = d/v
        added_Time = 0
        if V1[i+1] == V1[i]:
            added_Time = 1/V1[i]
        # for nonzero acceleration, t = [v(x+1)-v(x)]/a
        else:
            added_Time += (V1[i+1] - V1[i]) / A1[i]
        time += added_Time

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

    #repeats code from above
    for i in range(5):
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

    for i in range(len(A1)):

        if A1[i] > 10 or A1[i] < -10:
            print(A1[i], " ", i)

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

tot_weighted_time = t1[2] + 0.25*(t2[2] +t3[2] +t4[2]) + 0.5*(t5[2] +t6[2]) +t7[2] +t8[2]
print("Total weighted time: %fs" %tot_weighted_time)


def writeFile(fileName, accel, pitstop):
    pitstop_to_write = [0] * 999
    output=[]
    for i in range(len(pitstop)):
        index = pitstop[i]
        pitstop_to_write[index] = 1

    for i in range(len(accel)):
        output.append([accel[i], pitstop_to_write[i]])

    with open(fileName, 'w') as write:
        writer = csv.writer(write)
        writer.writerows(output)


writeFile('instruction_1.csv', t1[1], t1[5])
writeFile('instruction_2.csv', t2[1], t2[5])
writeFile('instruction_3.csv', t3[1], t3[5])
writeFile('instruction_4.csv', t4[1], t4[5])
writeFile('instruction_5.csv', t5[1], t5[5])
writeFile('instruction_6.csv', t6[1], t6[5])
writeFile('instruction_7.csv', t7[1], t7[5])
writeFile('instruction_8.csv', t8[1], t8[5])







