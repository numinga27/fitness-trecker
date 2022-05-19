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

    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        speed_run: float = (self.SPEED_MULTIPLIER * self.get_mean_speed()
                            - self.SPEED_SHIFT)
        time_run: float = self.duration * self.M_IN_HOUR

        return speed_run * self.weight / self.M_IN_KM * time_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTIPLIER: float = 0.035
    WEIGHT_INREASE: float = 0.029
    SPEED_INCREASE = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        time_sportswalking: float = self.duration * self.M_IN_HOUR
        workload: float = self.WEIGHT_MULTIPLIER * self.weight

        return ((workload
                 + ((self.get_mean_speed()**self.SPEED_INCREASE
                     // self.height)
                    * self.WEIGHT_INREASE * self.weight))
                * time_sportswalking)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MULTY_SPEED: float = 1.1
    WEIGHT_MULTYPLICATION = 2

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
        calorie_swim: float = ((self.get_mean_speed()
                                + self.MULTY_SPEED)
                               * self.WEIGHT_MULTYPLICATION * self.weight)

        return calorie_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    WORKTSOUT = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training = WORKTSOUT.get(workout_type)(*data)

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
