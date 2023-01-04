import random

room = []
x = random.randint(10, 20)
y = random.randint(10, 20)
while x % 2 == 1 or y % 2 == 1:
    x = random.randint(10, 20)
    y = random.randint(10, 20)
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
            if j == e - 1 or j == 22 - e:
                new_room += '#'
            elif j < e or j > 22 - e:
                new_room += 'e'
            else:
                new_room += '.'
        room[i] = new_room
for i in range(5):
    building = random.randint(0, 4)
    build = (random.randint(e + 2, 22 - e - 2), random.randint(e2 + 2, 22 - e2 - 2))
    if building == 0:
        new_room = [x for x in room[build[0]]]
        new_room[build[1]] = '#'
        new_room[build[1] + 1] = '#'
        room[build[0]] = ''.join(new_room)
        new_room = [x for x in room[build[0] + 1]]
        new_room[build[1]] = '#'
        room[build[0] + 1] = ''.join(new_room)
    if building == 1:
        new_room = [x for x in room[build[0]]]
        new_room[build[1]] = '#'
        new_room[build[1] + 1] = '#'
        room[build[0]] = ''.join(new_room)
        new_room = [x for x in room[build[0] + 1]]
        new_room[build[1] + 1] = '#'
        room[build[0] + 1] = ''.join(new_room)
    if building == 2:
        new_room = [x for x in room[build[0]]]
        new_room[build[1]] = '#'
        new_room[build[1] + 1] = '#'
        room[build[0]] = ''.join(new_room)
        new_room = [x for x in room[build[0] + 1]]
        new_room[build[1]] = '#'
        new_room[build[1] + 1] = '#'
        room[build[0] + 1] = ''.join(new_room)
    if building == 3:
        new_room = [x for x in room[build[0]]]
        new_room[build[1]] = '#'
        new_room[build[1] + 1] = '#'
        new_room[build[1] + 2] = '#'
        room[build[0]] = ''.join(new_room)
        new_room = [x for x in room[build[0] + 1]]
        new_room[build[1]] = '#'
        new_room[build[1] + 1] = '#'
    if building == 4:
        new_room = [x for x in room[build[0]]]
        new_room[build[1]] = '#'
        new_room[build[1] + 1] = '#'
        new_room[build[1] + 2] = '#'
        room[build[0]] = ''.join(new_room)
        new_room = [x for x in room[build[0] + 1]]
        new_room[build[1]] = '#'
        new_room[build[1] + 1] = '#'
        new_room = [x for x in room[build[0] + 2]]
        new_room[build[1]] = '#'
for el in room:
    print(el)
