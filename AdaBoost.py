import numpy as np
import matplotlib.pyplot as plt
from point2d import Point2D
from numpy import log as ln
import random
from itertools import combinations
import sys
import math
def rSubset(arr, r):
    # return list of all subsets of length r
    # to deal with duplicate subsets use
    # set(list(combinations(arr, r)))
    return list(combinations(arr, r))


def Rectangle(listCombinatation,dataSet,weighted_points,round):
    # errors1-> in the rectangle 2 outside the rectangle 1
    # errors2-> in the rectangle 1 outside the rectangle 2
    εt =sys.float_info.max
    inside2=True
    bool=True
    # going throw all the combinations and build a rectangle on each
    for j in range(0, 2080):
        a, b = listCombinatation[j]
        p1_x = dataSet[a][0]
        p1_y = dataSet[a][1]
        p2_x = dataSet[b][0]
        p2_y = dataSet[b][1]
        errors = 0
        # checking the errors in the specific rectangle
        for i in range(0,65):
            if (True==in_the_rectangle(p1_x,p1_y,p2_x,p2_y,dataSet[i][0],dataSet[i][1])):
               if (dataSet[i][2]==1):
                   errors=errors+weighted_points[round][i]
            else:
                if (dataSet[i][2] == 2):
                    errors = errors+weighted_points[round][i]
         #checking if the errors smaller if 1 inside and 2 outside
        if(errors>(1-errors)):
            bool = False
            errors=(1-errors)
        else:
            bool = True
        # checking if the errors is smaller than what we got before and saves the rectnagle and the value
        if (εt>errors):
            εt = errors
            inside2 = bool
            p1rectangle_x = dataSet[a][0]
            p1rectangle_y = dataSet[a][1]
            p2rectangle_x = dataSet[b][0]
            p2rectangle_y = dataSet[b][1]

    return (p1rectangle_x,p1rectangle_y,p2rectangle_x,p2rectangle_y,εt,inside2)




def in_the_rectangle(p1_x,p1_y,p2_x,p2_y,pcheck_x,pcheck_y)->(bool):
    x1 = np.minimum(p1_x, p2_x)
    x2 = np.maximum(p1_x, p2_x)
    y1 = np.minimum(p1_y, p2_y)
    y2 = np.maximum(p1_y, p2_y)
    return pcheck_x >= x1 and pcheck_x <= x2 and pcheck_y >= y1 and pcheck_y <= y2
    pass



def AdaBoostForRectangle(dataSet,n,list,r):
    listRectangle = np.full((r, 6), 0, dtype=float)
    weighted_points=np.full((9, 65), 1/n, dtype=float)
    for round in range(1,r+1):
        # Use Rectangle to find a rectangle with minimum weighted error εt
        p1_x, p1_y, p2_x , p2_y, εt, inside2 = Rectangle(list, dataSet, weighted_points, round - 1)
        listRectangle[round - 1][0]=p1_x
        listRectangle[round - 1][1] = p1_y
        listRectangle[round - 1][2] = p2_x
        listRectangle[round - 1][3] = p2_y

        if(inside2==True):
            listRectangle[round - 1][4] = 2
        else:
            listRectangle[round - 1][4] = 1


        # Compute the weight
        άt = (0.5 * ln((1 - εt) / εt))
        listRectangle[round - 1][5] = άt


        # Compute new weights for the points:
        for i in range(0, 65):

            # if the point inside the rectangle
            if (True == in_the_rectangle(p1_x, p1_y,p2_x ,p2_y,dataSet[i][0],dataSet[i][1])):
                # Not an error on point xi:
                if ((inside2 == True) and (dataSet[i][2] == 2)) or ((inside2 == False) and (dataSet[i][2] == 1)):
                    #  Dt(xi) = Dt-1(xi) exp(-άt)
                    weighted_points[round][i] =( weighted_points[round - 1][i] *np.exp((-1 * άt)))

                # For an error on point xi:
                else:
                    # Dt(xi) = Dt-1(xi) exp(άt)
                    weighted_points[round][i] = ( weighted_points[round - 1][i] *np.exp(( άt)))

            # if the point is not inside the rectangle
            else:
                # Not an error on point xi:
                if ((inside2 == True) and (dataSet[i][2] == 1)) or ((inside2 == False) and (dataSet[i][2] == 2)):
                    #  Dt(xi) = Dt-1(xi) exp(-άt)
                    weighted_points[round][i] = ( weighted_points[round - 1][i] *np.exp((-1 * άt)))

                # For an error on point xi:
                else:
                    # Dt(xi) = Dt-1(xi) exp(άt)
                    weighted_points[round][i] = ( weighted_points[round - 1][i] *np.exp(( άt)))

        # Normalize these weights:
        sum = weighted_points[round].sum()

        # Dt(xi) = Dt(xi) / ∑j Dt(xj)
        for i in range(0, 65):
            weighted_points[round][i] = weighted_points[round][i] / sum
    return listRectangle

def Circle(listCombinatation, dataSet, weighted_points, round):
        εt = sys.float_info.max
        inside2 = True
        bool = True
        # going throw all the combinations and build a rectangle on each
        for j in range(0, 2080):
            a, b = listCombinatation[j]
            p1_x = dataSet[a][0]
            p1_y = dataSet[a][1]
            p2_x = dataSet[b][0]
            p2_y = dataSet[b][1]
            raduis=dis(p1_x,p1_y,p2_x,p2_y)
            errors = 0
            # checking the errors in the specific rectangle
            for i in range(0, 65):
                if (True == in_the_circle(p1_x, p1_y,raduis, dataSet[i][0], dataSet[i][1])):
                    if (dataSet[i][2] == 1):
                        errors = errors + weighted_points[round][i]
                else:
                    if (dataSet[i][2] == 2):
                        errors = errors + weighted_points[round][i]
            # checking if the errors smaller if 1 inside and 2 outside
            if (errors > (1 - errors)):
                bool = False
                errors = (1 - errors)
            else:
                bool = True
            # checking if the errors is smaller than what we got before and saves the rectnagle and the value
            if (εt > errors):
                εt = errors
                inside2 = bool
                circle_center_X = dataSet[a][0]
                circle_center_y = dataSet[a][1]
                raduis_circle = raduis

        return (circle_center_X, circle_center_y, raduis_circle, εt, inside2)


def in_the_circle(center_x, center_y,radius, pcheck_x, pcheck_y) -> (bool):
    return radius>=dis(center_x,center_y,pcheck_x,pcheck_y)

def dis(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def AdaBoostForCircle(dataSet,n,list,r):
    listCircle = np.full((r, 6), 0, dtype=float)
    weighted_points=np.full((9, 65), 1/n, dtype=float)
    for round in range(1,r+1):
        # Use Rectangle to find a rectangle with minimum weighted error εt
        p1_x, p1_y, raduis, εt, inside2 = Circle(list, dataSet, weighted_points, round - 1)
        listCircle[round - 1][0]=p1_x
        listCircle[round - 1][1] = p1_y
        listCircle[round - 1][2] = raduis

        if(inside2==True):
            listCircle[round - 1][3] = 2
        else:
            listCircle[round - 1][3] = 1


        # Compute the weight
        άt = (0.5 * ln((1 - εt) / εt))
        listCircle[round - 1][4] = άt


        # Compute new weights for the points:
        for i in range(0, 65):

            # if the point inside the rectangle
            if (True == in_the_circle(p1_x, p1_y,raduis,dataSet[i][0],dataSet[i][1])):
                # Not an error on point xi:
                if ((inside2 == True) and (dataSet[i][2] == 2)) or ((inside2 == False) and (dataSet[i][2] == 1)):
                    #  Dt(xi) = Dt-1(xi) exp(-άt)
                    weighted_points[round][i] =( weighted_points[round - 1][i] *np.exp((-1 * άt)))

                # For an error on point xi:
                else:
                    # Dt(xi) = Dt-1(xi) exp(άt)
                    weighted_points[round][i] = ( weighted_points[round - 1][i] *np.exp(( άt)))

            # if the point is not inside the rectangle
            else:
                # Not an error on point xi:
                if ((inside2 == True) and (dataSet[i][2] == 1)) or ((inside2 == False) and (dataSet[i][2] == 2)):
                    #  Dt(xi) = Dt-1(xi) exp(-άt)
                    weighted_points[round][i] = ( weighted_points[round - 1][i] *np.exp((-1 * άt)))

                # For an error on point xi:
                else:
                    # Dt(xi) = Dt-1(xi) exp(άt)
                    weighted_points[round][i] = ( weighted_points[round - 1][i] *np.exp(( άt)))

        # Normalize these weights:
        sum = weighted_points[round].sum()

        # Dt(xi) = Dt(xi) / ∑j Dt(xj)
        for i in range(0, 65):
            weighted_points[round][i] = weighted_points[round][i] / sum
    return listCircle

def main():

    #loading the dataset
    data = open("HC_Body_Temperature.txt", "r")
    data=data.read().splitlines()
    dataSet=(130,3)
    dataSet=np.ndarray(dataSet)
    for i in range(0,130):
        temperature, gender, heartrate = data[i].split()
        dataSet[i][0]=float(temperature)
        dataSet[i][1]=float(heartrate)
        dataSet[i][2]=float(gender)

    #number of combinations
    list = rSubset(range(0, 65), 2)

#-------------------rectangle-----------------------------------------
    print("----------rectangle------------")
    for r in range(1,9):
        T_sum=0
        R_sum=0
        for i in range(1,50):
            np.random.shuffle(dataSet)
            train_data = dataSet[:65]
            test_data = dataSet[65:]
            listCircle = AdaBoostForRectangle(train_data,65,list,r)

            #for test points
            for point in range(0,65):
                point_x = test_data[point][0]
                point_y = test_data[point][1]
                gender = test_data[point][2]
                h_x=0
                for numRe in range(0,r):
                    p1_x = listCircle[numRe][0]
                    p1_y = listCircle[numRe][1]
                    p2_x = listCircle[numRe][2]
                    p2_y = listCircle[numRe][3]
                    genderInRec = listCircle[numRe][4]
                    errors = listCircle[numRe][5]

                    #the point supouse to be where is classifiar
                    if(in_the_rectangle(p1_x,p1_y,p2_x,p2_y,point_x,point_y)and genderInRec==gender)or(
                            False==in_the_rectangle(p1_x,p1_y,p2_x,p2_y,point_x,point_y)and genderInRec!=gender):
                        h_x += errors
                    else:
                        h_x += errors*-1
                if(gender==2):
                    gender=-1
                T_sum+= int(h_x*gender<0)

            # for training points
            for point in range(0, 65):
                point_x = train_data[point][0]
                point_y = train_data[point][1]
                gender = train_data[point][2]
                h_x = 0
                for numRe in range(0, r):
                    p1_x = listCircle[numRe][0]
                    p1_y = listCircle[numRe][1]
                    p2_x = listCircle[numRe][2]
                    p2_y = listCircle[numRe][3]
                    genderInRec = listCircle[numRe][4]
                    errors = listCircle[numRe][5]

                    # the point supouse to be where is classifiar
                    if (in_the_rectangle(p1_x, p1_y, p2_x, p2_y, point_x, point_y) and genderInRec == gender) or (
                            False == in_the_rectangle(p1_x, p1_y, p2_x, p2_y, point_x,
                                                      point_y) and genderInRec != gender):
                        h_x += errors
                    else:
                        h_x += errors * -1
                if (gender == 2):
                    gender = -1
                R_sum += int(h_x * gender < 0)

        print("number of mistakes on T in round ",r, " : ",(T_sum/100)/65)
        print("number of mistakes on R in round ",r, " : ",(R_sum/100)/65)
        print()

    print("----------------------")




#-------------------circules-----------------------------------------
    print("-----------circules-----------")
    for r in range(1, 9):
        T_sum = 0
        R_sum = 0
        for i in range(1, 50):
            np.random.shuffle(dataSet)
            train_data = dataSet[:65]
            test_data = dataSet[65:]
            listCircle = AdaBoostForRectangle(train_data, 65, list, r)

            # for test points
            for point in range(0, 65):
                point_x = test_data[point][0]
                point_y = test_data[point][1]
                gender = test_data[point][2]
                h_x = 0
                for numRe in range(0, r):
                    p1_x = listCircle[numRe][0]
                    p1_y = listCircle[numRe][1]
                    radius = listCircle[numRe][2]
                    genderInRec = listCircle[numRe][3]
                    errors = listCircle[numRe][4]


                    # the point supouse to be where is classifiar
                    if (in_the_circle(p1_x, p1_y, radius, point_x, point_y) and genderInRec == gender) or (
                            False == in_the_circle(p1_x, p1_y, radius, point_x,
                                                      point_y) and genderInRec != gender):
                        h_x += errors
                    else:
                        h_x += errors * -1
                if (gender == 2):
                    gender = -1
                T_sum += int(h_x * gender < 0)

            # for training points
            for point in range(0, 65):
                point_x = train_data[point][0]
                point_y = train_data[point][1]
                gender = train_data[point][2]
                h_x = 0
                for numRe in range(0, r):
                    p1_x = listCircle[numRe][0]
                    p1_y = listCircle[numRe][1]
                    raduis = listCircle[numRe][2]
                    genderInRec = listCircle[numRe][3]
                    errors = listCircle[numRe][4]

                    # the point supouse to be where is classifiar
                    if (in_the_circle(p1_x, p1_y, raduis, point_x, point_y) and genderInRec == gender) or (
                            False == in_the_circle(p1_x, p1_y, radius, point_x,point_y) and genderInRec != gender):
                        h_x += errors
                    else:
                        h_x += errors * -1
                if (gender == 2):
                    gender = -1
                R_sum += int(h_x * gender < 0)

        print("number of mistakes on T in round ", r, " : ", (T_sum / 100) / 65)
        print("number of mistakes on R in round ", r, " : ", (R_sum / 100) / 65)
        print()

if __name__ == '__main__':
    main()