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
        self.duration = duration  # sozdal obekty action,duration,weight
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

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
    coeff_1: float = 18
    coeff_2: float = 20

    def get_spent_calories(self) -> float:
        return (self.coeff_1 * self.get_mean_speed() - self.coeff_2) * \
            self.weight / self.M_IN_KM * (self.duration * self.M_IN_HOUR)


class SportsWalking(Training):
    coeff_3: float = 0.035
    coeff_4: float = 0.029
    coeff_5: float = 2
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # dobavil rost

    def get_spent_calories(self) -> float:
        t: float = (self.duration * self.M_IN_HOUR)
        p_1: float = self.coeff_3 * self.weight
        return (p_1 + (self.get_mean_speed()**self.coeff_5
                       // self.height) * self.coeff_4 * self.weight) * t


class Swimming(Training):
    LEN_STEP = 1.38
    coeff_6: float = 1.1
    coeff_7: float = 2
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # dobavil
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        p_2: float = self.length_pool * self.count_pool
        return p_2 / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:

        calorie_3: float = (self.get_mean_speed()
                            + self.coeff_6) * self.coeff_7 * self.weight
        return calorie_3  # proverit pravilnosti oformleniay


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_sl = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training = workout_type_sl.get(workout_type)(*data)  # chitaet dannye
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
