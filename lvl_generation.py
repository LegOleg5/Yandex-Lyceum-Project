import random


def lvl_generate(lvl_name):
    floors = ['.', ',', '!']

    def hallway_1(room):
        for i in range(len(room)):
            new_room = [x for x in room[i]]
            if i == 10 or i == 11:
                for j in range(len(new_room)):
                    new_room[j] = '.'
            if i == 9 or i == 12:
                for j in range(len(new_room)):
                    if new_room[j] == 'e':
                        new_room[j] = '#'
            room[i] = ''.join(new_room)
        return room

    def hallway_2(room):
        for i in range(len(room)):
            new_room = [x for x in room[i]]
            if new_room[9] == 'e':
                new_room[9] = '#'
            if new_room[12] == 'e':
                new_room[12] = '#'
            new_room[10] = ','
            new_room[11] = ','
            room[i] = ''.join(new_room)
        return room

    def hallway_3(room, corner):
        if corner == 1:
            for i in range(len(room)):
                new_room = [x for x in room[i]]
                if i == 10 or i == 11:
                    for j in range(len(new_room)):
                        if j > 9:
                            if j == 10 and i == 10:
                                new_room[j] = '@'
                            else:
                                new_room[j] = '!'
                if i == 9 or i == 12:
                    for j in range(len(new_room)):
                        if j > 9:
                            if new_room[j] == 'e':
                                new_room[j] = '#'
                if i > 11:
                    if new_room[9] == 'e':
                        new_room[9] = '#'
                    if new_room[12] == 'e':
                        new_room[12] = '#'
                    new_room[10] = '!'
                    new_room[11] = '!'
                room[i] = ''.join(new_room)
        if corner == 2:
            for i in range(len(room)):
                new_room = [x for x in room[i]]
                if i == 10 or i == 11:
                    for j in range(len(new_room)):
                        if j < 12:
                            new_room[j] = '!'
                if i == 9 or i == 12:
                    for j in range(len(new_room)):
                        if j < 12:
                            if new_room[j] == 'e':
                                new_room[j] = '#'
                if i > 11:
                    if new_room[9] == 'e':
                        new_room[9] = '#'
                    if new_room[12] == 'e':
                        new_room[12] = '#'
                    new_room[10] = '!'
                    new_room[11] = '!'
                room[i] = ''.join(new_room)
        if corner == 3:
            for i in range(len(room)):
                new_room = [x for x in room[i]]
                if i == 10 or i == 11:
                    for j in range(len(new_room)):
                        if j > 9:
                            new_room[j] = '!'
                if i == 9 or i == 12:
                    for j in range(len(new_room)):
                        if j > 9:
                            if new_room[j] == 'e':
                                new_room[j] = '#'
                if i < 10:
                    if new_room[9] == 'e':
                        new_room[9] = '#'
                    if new_room[12] == 'e':
                        new_room[12] = '#'
                    new_room[10] = '!'
                    new_room[11] = '!'
                room[i] = ''.join(new_room)
        if corner == 4:
            for i in range(len(room)):
                new_room = [x for x in room[i]]
                if i == 10 or i == 11:
                    for j in range(len(new_room)):
                        if j < 12:
                            new_room[j] = '!'
                if i == 9 or i == 12:
                    for j in range(len(new_room)):
                        if j < 12:
                            if new_room[j] == 'e':
                                new_room[j] = '#'
                if i < 10:
                    if new_room[9] == 'e':
                        new_room[9] = '#'
                    if new_room[12] == 'e':
                        new_room[12] = '#'
                    new_room[10] = '!'
                    new_room[11] = '!'
                room[i] = ''.join(new_room)
        return room

    def hallway_to_door(room):
        for i in range(len(room)):
            new_room = [x for x in room[i]]
            if i == 10 or i == 11:
                for j in range(len(new_room)):
                    if j < 12:
                        new_room[j] = ','
            if i == 9 or i == 12:
                for j in range(len(new_room)):
                    if j < 12:
                        if new_room[j] == 'e':
                            new_room[j] = '#'
            room[i] = ''.join(new_room)
        return room

    def enemies_spawn(room, sym, sym2):
        first_enemy = [random.randint(0, 400), random.randint(0, 400), random.randint(0, 400), random.randint(0, 400),
                       random.randint(0, 400), random.randint(0, 400), random.randint(0, 400), random.randint(0, 400),
                       random.randint(0, 400),
                       random.randint(0, 400)]
        second_enemy = [random.randint(0, 400), random.randint(0, 400), random.randint(0, 400), random.randint(0, 400),
                        random.randint(0, 400), random.randint(0, 400), random.randint(0, 400), random.randint(0, 400),
                        random.randint(0, 400),
                        random.randint(0, 400)]
        for i in range(len(room)):
            new_room = [x for x in room[i]]
            for j in range(len(room)):
                for el in first_enemy:
                    if el == i * j:
                        if room[i][j] == '#':
                            pass
                        elif room[i][j] == 'e':
                            pass
                        else:
                            new_room[j] = sym
                for el in second_enemy:
                    if el == i * j:
                        if room[i][j] == '#':
                            pass
                        elif room[i][j] == 'e':
                            pass
                        else:
                            new_room[j] = sym2
            room[i] = ''.join(new_room)
        return room

    all_rooms = []
    for _ in range(12):
        if _ == 1 or _ == 2 or _ == 9 or _ == 10:
            fl = floors[0]
        elif _ == 0 or _ == 3 or _ == 8 or _ == 11:
            fl = floors[2]
        else:
            fl = floors[1]
        room = []
        x = random.randint(10, 20)
        y = random.randint(10, 20)
        while x % 2 == 1 or y % 2 == 1:
            x = random.randint(10, 20)
            y = random.randint(10, 20)
        if _ == 5 or _ == 6:
            x = 20
            y = 20
        e = (22 - x) // 2
        e2 = (22 - y) // 2
        for i in range(22):
            if i == e2 - 1 or i == 22 - e2:
                room.append(22 * '#')
            elif i < e2 or i > 22 - e2:
                room.append(22 * 'e')
            else:
                room.append([])
        for i in range(len(room)):
            if room[i] == 22 * '#':
                new_room = ''
                for j in range(22):
                    if j == e - 1 or j == 22 - e:
                        new_room += '#'
                    elif j < e or j > 22 - e:
                        new_room += 'e'
                    else:
                        new_room += '#'
                room[i] = new_room
            if not room[i]:
                new_room = ''
                for j in range(22):
                    if j == e - 1:
                        if _ != 6:
                            new_room += '#'
                        else:
                            new_room += fl
                    elif j == 22 - e:
                        if _ != 5:
                            new_room += '#'
                        else:
                            new_room += fl
                    elif j < e or j > 22 - e:
                        new_room += 'e'
                    else:
                        new_room += fl
                room[i] = new_room
        for i in range(5):
            building = random.randint(0, 4)
            build = (random.randint(e + 2, 22 - e - 2), random.randint(e2 + 2, 22 - e2 - 2))
            if building == 0:
                new_room = [x for x in room[build[0]]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                room[build[0]] = ''.join(new_room)

                new_room = [x for x in room[build[0] + 1]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                room[build[0] + 1] = ''.join(new_room)

            if building == 1:
                new_room = [x for x in room[build[0]]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                room[build[0]] = ''.join(new_room)

                new_room = [x for x in room[build[0] + 1]]
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                room[build[0] + 1] = ''.join(new_room)

            if building == 2:
                new_room = [x for x in room[build[0]]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                room[build[0]] = ''.join(new_room)

                new_room = [x for x in room[build[0] + 1]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                room[build[0] + 1] = ''.join(new_room)

            if building == 3:
                new_room = [x for x in room[build[0]]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                if new_room[build[1] + 2] == fl:
                    new_room[build[1] + 2] = '#'
                room[build[0]] = ''.join(new_room)

                new_room = [x for x in room[build[0] + 1]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                room[build[0] + 1] = ''.join(new_room)

            if building == 4:
                new_room = [x for x in room[build[0]]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                if new_room[build[1] + 2] == fl:
                    new_room[build[1] + 2] = '#'
                room[build[0]] = ''.join(new_room)

                new_room = [x for x in room[build[0] + 1]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                if new_room[build[1] + 1] == fl:
                    new_room[build[1] + 1] = '#'
                room[build[0] + 1] = ''.join(new_room)

                new_room = [x for x in room[build[0] + 2]]
                if new_room[build[1]] == fl:
                    new_room[build[1]] = '#'
                room[build[0] + 2] = ''.join(new_room)
        all_rooms.append(room)
    all_rooms[1] = hallway_1(all_rooms[1])
    all_rooms[2] = hallway_1(all_rooms[2])
    all_rooms[9] = hallway_1(all_rooms[9])
    all_rooms[10] = hallway_1(all_rooms[10])
    all_rooms[4] = hallway_2(all_rooms[4])
    all_rooms[7] = hallway_2(all_rooms[7])
    all_rooms[7] = hallway_to_door(all_rooms[7])
    all_rooms[0] = hallway_3(all_rooms[0], 1)
    all_rooms[3] = hallway_3(all_rooms[3], 2)
    all_rooms[8] = hallway_3(all_rooms[8], 3)
    all_rooms[11] = hallway_3(all_rooms[11], 4)
    for i in range(len(all_rooms)):
        if i == 5 or i == 6:
            pass
        elif i == 1 or i == 2 or i == 9 or i == 10:
            all_rooms[i] = enemies_spawn(all_rooms[i], '=', 'b')
        elif i == 0 or i == 3 or i == 8 or i == 11:
            all_rooms[i] = enemies_spawn(all_rooms[i], '+', '-')
        else:
            all_rooms[i] = enemies_spawn(all_rooms[i], 'f', 'l')

    with open('lvl4', mode='w') as lvl:
        for i in range(22):
            lvl.write(all_rooms[0][i])
            lvl.write(all_rooms[1][i])
            lvl.write(all_rooms[2][i])
            lvl.write(all_rooms[3][i])
            lvl.write('\n')
        for i in range(22):
            lvl.write(all_rooms[4][i])
            lvl.write(all_rooms[5][i])
            lvl.write(all_rooms[6][i])
            lvl.write(all_rooms[7][i])
            lvl.write('\n')
        for i in range(22):
            lvl.write(all_rooms[8][i])
            lvl.write(all_rooms[9][i])
            lvl.write(all_rooms[10][i])
            lvl.write(all_rooms[11][i])
            lvl.write('\n')


lvl_generate('lvl4')
