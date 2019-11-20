import sys

new1_txt = open(sys.argv[1], 'r')
command_list = []
for c in new1_txt:
    x = c.split()
    command_list.append(x)  # all the comments as lists in a list
file = open('out.txt', 'w')
hall_list = []  # all halls that given with CREATEHALL command
row_and_column = []
halls = []
new_halls = []  # all halls that will be created
hall_dict = {}
all_places = []
student_sum = []
full_sum = []
student_ticket = 5
full_ticket = 10
hall_name_seats = []  # hall names and their row and columns

for a in command_list:
    if a[0] == 'CREATEHALL':
        halls.append(a[1])
        if halls.count(a[1]) == 1:
            new_halls.append(a[1])
            row_and_column.append(a[2].split('x'))
            hall_name_seats.append([a[1], a[2].split('x')])
all = []
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
           'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
hall_matris = []

def print_output(str):
    print(str)
    file.write(str+'\n')


def createhall(i):
    global all_places, abc, hall_dict, hall_matris
    hall_list.append(i[1])
    if hall_list.count(i[1]) != 1:
        print_output("Warning: Cannot create the hall for the second time. The cinema has already {}".format(i[1]))

    elif hall_list.count(i[1]) == 1:
        row_column = i[2].split('x')
        row = row_column[0]
        column = row_column[1]
        if int(row) > 26:
            print_output("Warning: Cannot create a hall that has more than 26 rows")
        else:
            print_output("Hall '{}' having {} seats has been created".format(i[1], int(row) * int(column)))
            one_hall_seat = [i[1], [['X' for c in range(int(column))] for k in range(int(row))]]  # the hall's all seats in list
        all.append(one_hall_seat)
        x = one_hall_seat[1:][0]  # the hall's seats as X without hall names
        c = []
        for p in letters[:int(row)]:
            c.append(p)
        f = sorted(c, reverse=True)  # the letters for the hall's rows
        for e in range(len(x)):
            list = [f[e], x[e]]  # matching the row names with row seats
            matris = [i[1], list]
            hall_matris.append(matris)


def sellticket(i):
    global student_sum, full_sum,student_ticket,full_ticket
    name = i[1]
    fare = i[2]
    hall = i[3]
    seats = i[4:len(i)]


    def is_hall_exists():
        is_exist=False
        for t in range(0,len(new_halls)):
            if new_halls[t] == i[3]:
                is_exist=True
            else:
                pass
        return is_exist

    def is_one(seat):
        if '-' in seat:
            return False
        else:
            return True

    def is_seat_exists(seat):
        for t in hall_matris:
                if t[0] == i[3] and t[1][0] == seat[0]:
                    if int(len(t[1][1]))<int(seat[1:len(seat)]):
                        return False
                    else:
                        return True

    def sellseat(seat,sign):
        global full_sum, student_sum
        for t in hall_matris:
            if t[0] == i[3] and t[1][0] == seat[0] and seat_is_empty(seat):
                # print(t)
                if fare == 'student':
                    t[1][1][int(seat[1:len(seat)])] = 'S'
                    student_sum.append(hall)
                    if(sign):
                        print_output('Success: {} has bought {} at {}'.format(name,seat,hall))
                    else:
                        pass

                else:
                    t[1][1][int(seat[1:len(seat)])] = 'F'
                    full_sum.append(hall)
                    if(sign):
                        print_output('Success: {} has bought {} at {}'.format(name,seat,hall))
                    else:
                        pass

            elif t[0] == i[3] and t[1][0] == seat[0] and not(seat_is_empty(seat)):
                if(sign):
                    print_output("Warning: The seat {} cannot be sold to {} since it was already sold!".format(seat,name))
                else:
                    pass

    def seat_is_empty(seat):
        for t in hall_matris:
            if is_one(seat):
                if t[0] == i[3] and t[1][0] == seat[0]:  # seat=seats[0][0]
                    if t[1][1][int(seat[1:len(seat)])] == 'X':
                        return True
                    else:
                        return False

    def sell_more(seats,sign):
        for t in range(0, len(seats)):
            if is_one(seats[t]) and is_seat_exists(seats[t]) and seat_is_empty(seats[t]):
                sellseat(seats[t],sign)
            elif not (is_one(seats[t])):
                letter = seats[t][0]
                f_l = seats[t][1:len(seats[t])]
                first_last = (f_l.split('-'))
                first = int(first_last[0])
                last = int(first_last[1])
                sell_serial(letter, first, last)
            elif not(is_seat_exists(seats[t])):
                print_output("Error: The hall '{}' has less column than the specified index {}!".format(hall,seats[t]))
            elif not(seat_is_empty(seats[t])):
                print_output("Warning: The seat {} cannot be sold to {} since it was already sold!".format(seats[t],name))

    def is_serial_exist(letter,first,last):
        for t in hall_matris:
            if t[1][0] == letter:
                if first >= 0 and last < len(t[1][1]):
                    return True
                else:
                    return False


    def sell_serial(letter, first, last):
        seat_list = []
        if is_serial_exist(letter,first,last):
            for t in range(first, last):
                seat = letter + str(t)
                if (seat_is_empty(seat)):
                    seat_list.append(seat)
            if len(seat_list) == (last - first):
                sell_more(seat_list,False)
                print_output("Success: {} has bought {}{}-{} at {}".format(name,letter,first,last,hall))
            else:
                print_output("Warning: The seats {}{}-{} cannot be sold to {} due some of them have already been sold!".format(letter,first,last,name))
        else:
            print_output("Error: The hall '{}' has less column than the specified index {}{}-{}!".format(hall,letter,first,last))

    if is_hall_exists():
        if len(seats) == 1 and is_one(seats[0]):
            if is_seat_exists(seats[0]):
                if seat_is_empty(seats[0]):
                    sellseat(seats[0],True)
                else:
                    print_output("Error: The seat {} cannot be sold to {} due the seat has already been sold!".format(seats[0],name))
            else:
                print_output("Error: The hall '{}' has less column than the specified index {}!".format(hall,seats[0]))

        elif len(seats) > 1:
                sell_more(seats,True)
        elif len(seats) == 1 and not (is_one(seats[0])):
                letter = seats[0][0]
                f_l = seats[0][1:len(seats[0])]
                first_last = (f_l.split('-'))
                first = int(first_last[0])
                last = int(first_last[1])
                sell_serial(letter, first, last)

    else:
        print_output('Error: The hall {} does not exist'.format(hall))

def cancelticket(i):
    global student_sum, full_sum,student_ticket,full_ticket
    hall = i[1]
    seats = i[2:len(i)]

    def is_hall_exists():
        is_exist=False
        for t in range(0,len(new_halls)):
            if new_halls[t] == hall:
                is_exist=True
            else:
                pass
        return is_exist

    def is_one(seat):
        if '-' in seat:
            return False
        else:
            return True

    def is_seat_exists(seat):
        for t in hall_matris:
                if t[0] == hall and t[1][0] == seat[0]:
                    if int(len(t[1][1]))<int(seat[1:len(seat)]):
                        return False
                    else:
                        return True

    def is_serial_exist(letter, first, last):
        for t in hall_matris:
            if t[1][0] == letter:
                if first >= 0 and last < len(t[1][1]):
                    return True
                else:
                    return False

    def seat_is_empty(seat):
        for t in hall_matris:
            if is_one(seat):
                if t[0] == hall and t[1][0] == seat[0]:  # seat=seats[0][0]
                    if t[1][1][int(seat[1:len(seat)])] == 'X':
                        return True
                    else:
                        return False

    def cancel_more(seats, sign):
        for t in range(0, len(seats)):
            if is_one(seats[t]) and is_seat_exists(seats[t]) and seat_is_empty(seats[t]):
                cancelseat(seats[t], sign)
            elif not (is_one(seats[t])):
                letter = seats[t][0]
                f_l = seats[t][1:len(seats[t])]
                first_last = (f_l.split('-'))
                first = int(first_last[0])
                last = int(first_last[1])
                cancel_serial(letter, first, last)
            elif not (is_seat_exists(seats[t])):
                print_output("Error: The hall '{}' has less column than the specified index {}!".format(hall, seats[t]))
            elif not (seat_is_empty(seats[t])):
                print_output("Warning: The seat {} cannot be cancelled to ince it was already empty!".format(seats[t]))


    def cancel_serial(letter, first, last):
        seat_list = []
        if is_serial_exist(letter,first,last):
            for t in range(first, last):
                seat = letter + str(t)
                if not(seat_is_empty(seat)):
                    seat_list.append(seat)
            if len(seat_list) == (last - first):
                cancel_more(seat_list,False)
                print_output("Success: has cancelled {}{}-{} at {}".format(letter,first,last,hall))
            else:
                print_output("Error: The seats {}{}-{} cancelled due some of them have already been empty!".format(letter,first,last))
        else:
            print_output("Error: The hall ’{}’ has less column than the specified index {}{}-{}!".format(hall,letter,first,last))

    def cancelseat(seat,sign):
        global full_sum, student_sum

        for t in hall_matris:
            if t[0] == hall and t[1][0] == seat[0]:
                if t[1][1][int(seat[1:len(seat)])] == 'S':
                    t[1][1][int(seat[1:len(seat)])] = 'X'
                    student_sum.remove(hall)
                    if (sign):
                        print_output('Success: The seat {} at {} has been cancelled and now ready to sell again!'.format(seat, hall))
                    else:
                        pass

                elif t[1][1][int(seat[1:len(seat)])] == 'F':
                    t[1][1][int(seat[1:len(seat)])] = 'X'
                    full_sum.remove(hall)
                    if (sign):
                        print_output('Success: The seat {} at {} has been cancelled and now ready to sell again!'.format(seat, hall))
                    else:
                        pass
                else:
                    print_output("Error: The seat {} at '{}' has already been free! Nothing to cancel".format(seat,hall))

    if is_hall_exists():
        if len(seats) == 1 and is_one(seats[0]):
            if is_seat_exists(seats[0]):
                cancelseat(seats[0], True)
            else:
                print_output("Error: The hall '{}' has less column than the specified index {}".format(hall,seats[0]))
        elif len(seats) > 1:
            cancel_more(seats, True)
        elif len(seats) == 1 and not (is_one(seats[0])):
            letter = seats[0][0]
            f_l = seats[0][1:len(seats[0])]
            first_last = (f_l.split('-'))
            first = int(first_last[0])
            last = int(first_last[1])
            cancel_serial(letter, first, last)
    else:
        print_output('Error: The hall {} does not exist'.format(hall))


def showhall(i):

    def showhall_is_exist(i):
        is_exist=False
        for y in new_halls:
            if y == i[1]:
                is_exist=True
        return is_exist

    hall_str=""
    if showhall_is_exist(i):
        print_output("Printing hall layout of {}".format(i[1]))
        for p in hall_matris:
                if p[0] == i[1]:
                    column = len(p[1][1])
                    hall_str+=p[1][0]+" "
                    for v in p[1][1]:
                        hall_str+=v+"  "
                    hall_str+='\n'
        hall_str+="  "
        for z in range(int(column)):
                if z < 9:
                    hall_str+=str(z)+"  "
                else:
                    hall_str+= str(z) + " "

        print_output(hall_str)

    else:
        print_output('The {} does not exist'.format(i[1]))

def balance(i):
    global full_ticket,student_ticket,student_sum,full_sum

    def get_balance(k):
        student=0
        full=0
        for t in range(0,len(student_sum)):
            if(student_sum[t]==k):
                student+=1
        for z in range(0,len(full_sum)):
            if (full_sum[z] == k):
                full += 1
        student*=student_ticket
        full*=full_ticket
        string="Hall report of '"+k+"'\n"
        string+="-------------------------\n"
        string+="Sum of students = "+str(student)+", Sum of full fares = "+str(full)+", Overall = "+str(student+full)
        print_output(string)

    if len(i)==2:
        get_balance(i[1])
    else:
        for d in i[1:len(i)]:
            get_balance(d)


for i in command_list:
    if i[0] == 'CREATEHALL':
        if len(i) == 3:
            createhall(i)

        elif len(i) < 3:
            print("Error: Not enough parameters for creating a hall!")

        elif len(i) > 3:
            print("Error: Too much parameters for creating a hall!")

        else:
            print("An error occured")
    elif i[0] == 'SELLTICKET':
        sellticket(i)
    elif i[0] == 'SHOWHALL':
        showhall(i)
    elif i[0] == 'BALANCE':
        balance(i)
    elif i[0] == 'CANCELTICKET':
        cancelticket(i)
