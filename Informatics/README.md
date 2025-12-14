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
![alt text](image.png)
### Игровой интерфейс
![alt text](image1.png)


## Структура кода

```mermaid
flowchart TD
    Start[Запуск игры] --> Config[Загрузка настроек]
    Config --> CreateGUI[Создание интерфейса]
    CreateGUI --> InitBoards[Инициализация досок]
    
    InitBoards --> PlacementPhase[Фаза расстановки]
    PlacementPhase --> ManualMode[Ручной режим]
    PlacementPhase --> AutoMode[Автоматический режим]
    
    ManualMode --> PlaceShip[Разместить корабль]
    AutoMode --> RandomPlace[Случайная расстановка]
    
    PlaceShip --> CheckPlacement{Все корабли размещены?}
    RandomPlace --> CheckPlacement
    
    CheckPlacement -->|Нет| PlacementPhase
    CheckPlacement -->|Да| BattlePhase[Фаза боя]
    
    BattlePhase --> PlayerTurn[Ход игрока]
    PlayerTurn --> ProcessShot[Обработка выстрела]
    
    ProcessShot --> Hit{Попадание?}
    Hit -->|Да| MarkHit[Пометить попадание]
    Hit -->|Нет| MarkMiss[Пометить промах]
    
    MarkHit --> CheckDestroyed{Корабль уничтожен?}
    CheckDestroyed -->|Да| MarkDestroyed[Пометить корабль]
    CheckDestroyed -->|Нет| ComputerTurn[Ход компьютера]
    
    MarkMiss --> ComputerTurn
    MarkDestroyed --> CheckWin{Все корабли противника уничтожены?}
    
    ComputerTurn --> ComputerShot[Выстрел компьютера]
    ComputerShot --> CheckPlayerWin{Все корабли игрока уничтожены?}
    
    CheckWin -->|Да| GameWin[Игрок победил!]
    CheckWin -->|Нет| PlayerTurn
    
    CheckPlayerWin -->|Да| GameLose[Компьютер победил!]
    CheckPlayerWin -->|Нет| PlayerTurn
    
    GameWin --> End[Конец игры]
    GameLose --> End
```