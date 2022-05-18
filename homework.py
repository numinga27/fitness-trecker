class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    M_IN_HOUR: float = 60
    action: int
    duration: float
    weight: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    SPEED_MULTIPLIER: float = 18
    SPEED_SHIFT: float = 20

    def get_spent_calories(self) -> float:
        speed_run: float = (self.SPEED_MULTIPLIER * self.get_mean_speed()
                            - self.SPEED_SHIFT)
        time_run: float = self.duration * self.M_IN_HOUR
        return speed_run * self.weight / self.M_IN_KM * time_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_COEF: float = 0.035
    COEF_CALORIES: float = 0.029
    SPEED_COEF: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        time_sportswalking: float = self.duration * self.M_IN_HOUR
        nagruzka: float = self.WEIGHT_COEF * self.weight
        return ((nagruzka
                 + ((self.get_mean_speed()**self.SPEED_COEF
                     // self.height)

                    * self.COEF_CALORIES * self.weight))
                * time_sportswalking)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    SWIM_SPEED: float = 1.1
    SW_WEIGHT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        swim_distance: float = self.length_pool * self.count_pool
        return swim_distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:

        calorie_3: float = (self.get_mean_speed()
                            + self.SWIM_SPEED) * self.SW_WEIGHT * self.weight
        return calorie_3


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    WORKTOUTS = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training = WORKTOUTS.get(workout_type)(*data)

    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
