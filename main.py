import os
from pickle import dump, load
from random import randint
from time import time
# если библиотеки не установлены, то устанавливаем
# os.system('python -m pip install --upgrade pip')
# os.system('pip install wheel')
# os.system('pip cache purge')
# os.system('pip install colorama')
# os.system('pip install playsound2')

# если возникают проблемы, то попробуйте сделать это
'''
Убедитесь, что у вас установлена последняя версия pip с помощью команды python -m pip install --upgrade pip.
Попробуйте установить библиотеку wheel с помощью команды pip install wheel.
Попробуйте очистить кэш pip с помощью команды pip cache purge.
Устанавливаем нужные библиотеки
'''
from colorama import init, deinit, Fore
from playsound import playsound
init()


def saveGame(score, reqNum, count, maxAttempts, bestScore):
    # Открываем файл 'savegame.dat' в режиме записи байтов ('wb')
    with open('savegame.dat', 'wb') as f:
        # Сохраняем список переменных [score, reqNum, count, maxAttempts, bestScore] в файл с помощью функции dump
        dump([score, reqNum, count, maxAttempts, bestScore], f)


def loadGame():
    # Проверяем, существует ли файл 'savegame.dat'
    if not os.path.exists('savegame.dat'):
        # Если файл не существует, возвращаем None
        return None
    # Открываем файл 'savegame.dat' в режиме чтения байтов ('rb')
    with open('savegame.dat', 'rb') as f:
        # Загружаем данные из файла с помощью функции load
        data = load(f)
        # Проверяем длину списка data
        if len(data) == 4:
            # Если длина списка равна 4, то распаковываем переменные score, reqNum, count и maxAttempts
            score, reqNum, count, maxAttempts = data
            # Устанавливаем значение переменной bestScore равным 0
            bestScore = 0
        else:
            # Иначе распаковываем все пять переменных
            score, reqNum, count, maxAttempts, bestScore = data
    # Возвращаем значения переменных в виде кортежа
    return score, reqNum, count, maxAttempts, bestScore


# Функция guessTheNumber запускает игру 'Отгадай число', в которой пользователь должен отгадать загаданное компьютером число.
# Пользователь может выбрать уровень сложности, диапазон чисел и количество попыток.
# Также есть возможность играть с подсказками и ограничением по времени.
# Игра может быть сохранена и загружена в любой момент.
def guessTheNumber():
    print(Fore.MAGENTA + '\t\tДобро пожаловать в игру \'Отгадай число\'!')
    difficulty = input(Fore.RESET + f'Выберите уровень сложности ({Fore.GREEN}легкий, {Fore.YELLOW}средний, {Fore.RED}сложный{Fore.RESET}): ')
    
    if difficulty.lower() == 'легкий':
        maxAttempts = 10
    elif difficulty.lower() == 'средний':
        maxAttempts = 7
    else:
        maxAttempts = 5

    minNum = int(input('Введите минимальное число: '))
    maxNum = int(input('Введите максимальное число: '))
    print(f'Я загадал натуральное число из диапазона от {minNum} до {maxNum}. У вас есть {Fore.BLUE}{maxAttempts}{Fore.RESET} попыток, чтобы отгадать его.\n')

    hints = input(f'Хотите играть с подсказками? ({Fore.GREEN}да{Fore.RESET}/{Fore.RED}нет{Fore.RESET}): ')
    timeLimitInput = input(f'Хотите играть с ограничением по времени? ({Fore.GREEN}да{Fore.RESET}/{Fore.RED}нет{Fore.RESET}): ')
    
    if timeLimitInput.lower() == 'да':
        timeLimit = int(input('Введите ограничение по времени в секундах: '))
        startTime = time()

    saveGameInput = input(F'Хотите сохранять игру? ({Fore.GREEN}да{Fore.RESET}/{Fore.RED}нет{Fore.RESET}): ')
    
    if saveGameInput.lower() == 'да':
        loadedGame = loadGame()

        if loadedGame:
            score, reqNum, count, maxAttempts, bestScore = loadedGame
            playsound('music/save.mp3')
            print(f'Загружена сохраненная игра. Ваш текущий счет: {Fore.CYAN}{score}{Fore.RESET}. Осталось попыток: {Fore.YELLOW}{maxAttempts - count + 1}{Fore.RESET}')
        else:
            reqNum = randint(minNum, maxNum)
            count = 1
            score = 0
            bestScore = 0
    
    else:
        reqNum = randint(minNum, maxNum)
        count = 1
        score = 0
        bestScore = 0

    
    while count <= maxAttempts:
        
        try:
            userNum = int(input('Ваше предположение: '))
            if userNum < minNum or userNum > maxNum:
                print(f'Пожалуйста, введите число в диапазоне от {minNum} до {maxNum}.')
                continue
        except ValueError:
            print('Пожалуйста, введите целое число.')
            continue
        
        if userNum > reqNum:
            print('Меньше...')
            count += 1
        elif userNum < reqNum:
            print('Больше...')
            count += 1
        else:
            playsound('music/win.mp3')
            print(f'Вам удалось отгадать число! Это в самом деле {reqNum}')
            score += maxAttempts - count + 1
            
            if score > bestScore:
                bestScore = score
            
            print(f'Вы затратили на отгадывание всего лишь {Fore.GREEN}{count}{Fore.RESET} попыток! Ваш текущий счет: {Fore.GREEN}{score}{Fore.RESET}')
            break

        if hints.lower() == 'да' and count == maxAttempts // 2:
            if reqNum % 2 == 0:
                print('Подсказка: загаданное число четное.')
            else:
                print('Подсказка: загаданное число нечетное.')

        if timeLimitInput.lower() == 'да' and time() - startTime > timeLimit:
            playsound('music/defeat.mp3')
            print(f'К сожалению, вы не успели отгадать число за отведенное время. Загаданное число было {reqNum}.')
            break

    else:
        playsound('music/defeat.mp3')
        print(f'К сожалению, вы не смогли отгадать число за {maxAttempts} попыток. Загаданное число было {reqNum}.')

    if saveGameInput.lower() == 'да':
        saveGame(score, reqNum, count, maxAttempts, bestScore)

    playAgain = input(f'\nХотите сыграть еще раз? ({Fore.GREEN}да{Fore.RESET}/{Fore.RED}нет{Fore.RESET}): ')

    if playAgain.lower() == 'да':
        guessTheNumber()
    else:
        print(f'Ваш итоговый счет: {Fore.YELLOW}{score}{Fore.RESET}')
        print(f'Ваш лучший счет: {Fore.GREEN}{bestScore}{Fore.RESET}')
        print('Спасибо за игру! До свидания!')
        deinit()

if __name__ == '__main__':
    guessTheNumber()