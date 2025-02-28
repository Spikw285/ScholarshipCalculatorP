import logging

# Настраиваем логирование для вывода подробной информации
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def calculate_composite_score(component_name):
    """
    Функция для расчёта составной оценки (например, RegMid или RegEnd).
    Пользователь может ввести либо одно итоговое значение, либо разбить оценку на несколько компонентов с указанием их весов.
    Если суммарный вес не равен 100%, происходит нормализация.
    """
    print(f"\nВведите оценку для {component_name}:")
    mode = input(f"Желаете ввести одно итоговое значение для {component_name}? (y/n): ").strip().lower()

    # Если пользователь вводит одно значение – используем его напрямую
    if mode == 'y':
        score = float(input(f"Введите оценку для {component_name} (0-100): "))
        return score
    else:
        n = int(input(f"Сколько компонентов включает {component_name}?: "))
        total_weight = 0
        weighted_sum = 0
        for i in range(n):
            print(f"\nКомпонент {i + 1}:")
            weight = float(input("  Введите вес компонента (в процентах): "))
            score = float(input("  Введите оценку компонента (0-100): "))
            total_weight += weight
            weighted_sum += score * weight
        # Если суммарный вес не равен 100%, нормализуем оценку
        if total_weight != 100:
            print(f"\nОбщий вес компонентов равен {total_weight}%, а ожидалось 100%. Выполняется нормализация.")
            composite_score = weighted_sum / total_weight
        else:
            composite_score = weighted_sum / 100
        logging.info(f"{component_name} composite score: {composite_score:.2f}")
        return composite_score


def calculate_required_regfinal(regterm, target):
    """
    Рассчитывает, сколько баллов нужно набрать на RegFinal exam.
    Формула: RegTotal = (Regterm * 60%) + (RegFinal * 40%)
    => RegFinal = (target - 0.6 * regterm) / 0.4
    """
    required = (target - 0.6 * regterm) / 0.4
    return required


def main():
    print("=== Калькулятор итоговой оценки для стипендии/повышенной стипендии ===")
    print("Формула расчёта: RegTotal = (Regterm * 60%) + (RegFinal * 40%)")
    print("где Regterm = (RegMid + RegEnd) / 2")

    # Ввод составных оценок для RegMid и RegEnd
    reg_mid = calculate_composite_score("RegMid (например, Midterm + Assignments)")
    reg_end = calculate_composite_score("RegEnd (например, Endterm + Assignments)")

    # Вычисляем итоговую оценку за регламентированную часть
    regterm = (reg_mid + reg_end) / 2
    logging.info(f"Вычисленный Regterm (среднее RegMid и RegEnd): {regterm:.2f}")

    # Если оценка за финальный экзамен (RegFinal) уже известна, рассчитываем общий итог
    regfinal_input = input(
        "\nЗнаете ли вы оценку за RegFinal (Final exam)?\nЕсли да, введите её (0-100), иначе оставьте пустым и программа рассчитает, что нужно набрать: ").strip()

    if regfinal_input:
        regfinal = float(regfinal_input)
        reg_total = regterm * 0.6 + regfinal * 0.4
        logging.info(f"Вычисленный RegTotal: {reg_total:.2f}")
        print(f"\nВаш итоговый балл RegTotal = {reg_total:.2f}%")
        # Проверяем, достигнут ли порог для стипендии или повышенной стипендии
        if reg_total >= 90:
            print("Поздравляем! Вы достигли показателя для повышенной стипендии (90% и выше).")
        elif reg_total >= 70:
            print("Поздравляем! Вы достигли показателя для стипендии (70% и выше).")
        else:
            print("К сожалению, итоговый балл ниже требуемого для стипендии (70%).")
    else:
        # Если оценка за RegFinal ещё не известна, спрашиваем целевой итоговой балл
        target = float(input("\nВведите целевой итоговый балл (70 для стипендии или 90 для повышенной стипендии): "))
        required_regfinal = calculate_required_regfinal(regterm, target)
        if required_regfinal > 100:
            print(f"\nПохоже, у вас не получиться набрать {required_regfinal:.2f}% а Final exam чтобы достичь цели {target}%")
        else:
            print(
            f"\nВам необходимо набрать минимум {required_regfinal:.2f}% на Final exam, чтобы достичь цели {target}%.")
        logging.info(f"Требуемый балл на RegFinal: {required_regfinal:.2f}")


if __name__ == "__main__":
    main()
