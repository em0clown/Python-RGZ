# Морской бой на Python с Tkinter

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Status](https://img.shields.io/badge/status-complete-brightgreen)

Классическая игра "Морской бой" с графическим интерфейсом

</div>

## 📋 Содержание
- [Описание](#описание)
- [Особенности](#особенности)
- [Скриншоты](#скриншоты)
- [Структура кода](#структура-кода)

## 🎯 Описание

**Морской бой** - это полноценная реализация классической настольной игры с графическим интерфейсом на Python. Игра позволяет сразиться против компьютера с интуитивно понятным управлением и визуализацией игрового процесса.

## Особенности

### Игровые возможности
- ✅ Полноценный игровой цикл с пошаговой механикой
- ✅ Два режима расстановки кораблей (ручной/автоматический)
- ✅ Интеллектуальная система ходов компьютера
- ✅ Визуальное отображение состояния кораблей
- ✅ Определение уничтожения кораблей

### 🎨 Интерфейс
- ✅ Цветовая кодировка всех элементов
- ✅ Интерактивная подсветка при размещении
- ✅ Панель легенды с пояснениями
- ✅ Центрированное расположение элементов
- ✅ Адаптивная кнопка "В бой!"

### ⚙️ Функциональность
- ✅ Поворот кораблей клавишей `R`
- ✅ Валидация размещения кораблей
- ✅ Автоматическая расстановка компьютера
- ✅ Проверка условий победы
- ✅ Возможность новой игры без перезапуска

## 📸 Скриншоты
![alt text](../image.png)
### Игровой интерфейс
![alt text](../image1.png)


## Структура кода
flowchart TD
    Start[Начало программы] --> Init[Инициализация<br>констант и переменных]
    Init --> GUI[Создание графического<br>интерфейса]
    
    GUI --> CreatePlayerBoard[Создание доски игрока]
    GUI --> CreateComputerBoard[Создание доски компьютера]
    GUI --> CreateButtons[Создание панели кнопок]
    GUI --> CreateLegend[Создание панели легенды]
    
    CreatePlayerBoard --> BindEventsPlayer[Привязка событий к доске игрока]
    CreateComputerBoard --> BindEventsComputer[Привязка событий к доске компьютера]
    CreateButtons --> BindButtonEvents[Привязка событий к кнопкам]
    
    BindEventsPlayer --> Hover[update_hover при движении мыши]
    BindEventsPlayer --> ClickPlayer[player_click при клике]
    BindEventsComputer --> ClickComputer[computer_board_click при клике]
    
    BindButtonEvents --> BtnAuto[auto_place]
    BindButtonEvents --> BtnManual[Активация ручного режима]
    BindButtonEvents --> BtnClear[clear_board]
    BindButtonEvents --> BtnStart[start_game]
    BindButtonEvents --> BtnNew[new_game]
    
    BindEventsPlayer --> InitGame[Инициализация игры]
    InitGame --> PlaceComputerShips[Расстановка кораблей компьютера]
    InitGame --> DrawInitial[Первоначальная отрисовка]
    
    DrawInitial --> MainLoop[Запуск главного цикла Tkinter]
    
    MainLoop --> |Событие: Клик по своей доске| CheckPhase{Какая фаза игры?}
    CheckPhase --> |Фаза расстановки| ManualPlacement[Ручное размещение корабля]
    CheckPhase --> |Фаза боя| InvalidClick[Игнорировать клик]
    
    ManualPlacement --> CanPlace{Можно разместить?}
    CanPlace --> |Да| PlaceShip[Разместить корабль]
    CanPlace --> |Нет| ShowError[Показать ошибку]
    
    PlaceShip --> UpdateBoard[Обновить доску]
    UpdateBoard --> CheckAllPlaced{Все корабли размещены?}
    CheckAllPlaced --> |Да| ReadyForBattle[Готово к бою]
    CheckAllPlaced --> |Нет| NextShip[Перейти к следующему кораблю]
    
    MainLoop --> |Событие: Клик по доске компьютера| CheckGameStarted{Игра началась?}
    CheckGameStarted --> |Нет| Ignore[Игнорировать]
    CheckGameStarted --> |Да| ProcessShot[Обработать выстрел]
    
    ProcessShot --> CheckCell{Состояние клетки?}
    CheckCell --> |Пусто/Корабль| ValidShot[Валидный выстрел]
    CheckCell --> |Уже стреляли| InvalidShot[Невалидный выстрел]
    
    ValidShot --> |Попал| Hit[Отметить попадание]
    ValidShot --> |Промах| Miss[Отметить промах]
    
    Hit --> CheckDestroyed{Корабль уничтожен?}
    CheckDestroyed --> |Да| MarkDestroyed[Пометить весь корабль]
    CheckDestroyed --> |Нет| Continue[Продолжить]
    
    MarkDestroyed --> CheckWin{Все корабли противника уничтожены?}
    Miss --> CheckWin
    
    CheckWin --> |Игрок победил| PlayerWin[Показать победу]
    CheckWin --> |Еще есть корабли| ComputerTurn[Ход компьютера]
    
    ComputerTurn --> ComputerLogic[Логика хода компьютера]
    ComputerLogic --> ComputerShot[Выстрел компьютера]
    
    ComputerShot --> CheckPlayerCell{Состояние клетки игрока?}
    CheckPlayerCell --> |Корабль| ComputerHit[Попадание компьютера]
    CheckPlayerCell --> |Пусто| ComputerMiss[Промах компьютера]
    
    ComputerHit --> CheckPlayerDestroyed{Корабль игрока уничтожен?}
    CheckPlayerDestroyed --> |Да| MarkPlayerDestroyed[Пометить корабль игрока]
    CheckPlayerDestroyed --> |Нет| ShowHitMessage[Показать сообщение]
    
    MarkPlayerDestroyed --> CheckPlayerWin{Все корабли игрока уничтожены?}
    ComputerMiss --> CheckPlayerWin
    
    CheckPlayerWin --> |Компьютер победил| ComputerWin[Показать поражение]
    CheckPlayerWin --> |Еще есть корабли| PlayerTurn[Ожидание хода игрока]
    
    MainLoop --> |Событие: Нажатие клавиши R| KeyPress[Обработка нажатия]
    KeyPress --> ToggleDirection[Переключить направление корабля]
    
    MainLoop --> |Событие: Кнопка "Авторазмещение"| AutoPlace[Автоматическая расстановка]
    AutoPlace --> RandomPlacement[Случайное размещение всех кораблей]
    RandomPlacement --> UpdateDisplay[Обновить отображение]
    
    MainLoop --> |Событие: Кнопка "Очистить доску"| ClearBoard[Очистка доски]
    ClearBoard --> ResetPlacement[Сброс расстановки]
    
    MainLoop --> |Событие: Кнопка "В бой!"| StartBattle[Начать игру]
    StartBattle --> CheckReady{Все корабли размещены?}
    CheckReady --> |Да| ActivateBattle[Активировать фазу боя]
    CheckReady --> |Нет| ShowWarning[Показать предупреждение]
    
    MainLoop --> |Событие: Кнопка "Новая игра"| NewGame[Новая игра]
    NewGame --> FullReset[Полный сброс игры]
    FullReset --> Reinitialize[Повторная инициализация]