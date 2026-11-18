import os
from random import randint
import datetime
from PIL import Image
def my_box_blur(img, radius):
    width, height = img.size
    # Создаем пустое изображение для результата
    result = Image.new("RGB", (width, height))
    # Загружаем пиксели в память
    pixels = img.load()
    new_pixels = result.load()
    # Проходим по каждому пикселю
    for y in range(height):
        for x in range(width):
            r_sum = 0
            g_sum = 0
            b_sum = 0
            count = 0
            # Проходим по ядру вокруг пикселя
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx = x + dx
                    ny = y + dy
                    # Проверяем, не вышли ли мы за границы картинки
                    if 0 <= nx < width and 0 <= ny < height:
                        r, g, b = pixels[nx, ny][:3]
                        r_sum += r
                        g_sum += g
                        b_sum += b
                        count += 1
            # Вычисляем среднее арифметическое
            new_pixels[x, y] = (r_sum // count, g_sum // count, b_sum // count)

    return result
def my_color_correction(img, factor):
    width, height = img.size
    result = Image.new("RGB", (width, height))
    pixels = img.load()
    new_pixels = result.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            # 1. Находим серую версию (среднее арифметическое)
            gray = (r + g + b) // 3
            # 2. Формула смешивания: Новый_цвет = Серый + (Оригинал - Серый) * factor
            new_r = int(gray + (r - gray) * factor)
            new_g = int(gray + (g - gray) * factor)
            new_b = int(gray + (b - gray) * factor)
            # 3. Ограничиваем значения от 0 до 255 (чтобы не было переполнения)
            new_r = max(0, min(255, new_r))
            new_g = max(0, min(255, new_g))
            new_b = max(0, min(255, new_b))
            new_pixels[x, y] = (new_r, new_g, new_b)
    return result
name=randint(1,100)
newfile_name=f"result{name}.jpg"
tekfile=input("выберите изображение: image1.jpg, image2.png").strip()
ininput=os.path.join("Lab2_Media","data","input",tekfile)
inoutput=os.path.join("Lab2_Media","data","output",newfile_name)
logir=os.path.join("Lab2_Media","logs","history.txt")
filtr=" "
status="ошибка доступа"
try:
    with Image.open(ininput) as img:
        choise=int(input(("что применить:1.бох-фильтр или 2.цветокорекцию?введите цифру:")))
        if choise==1:
            try:
                rad=int(input("введите радиус размытия:"))
                if rad<1:
                    rad=1
            except ValueError:
                print("ошибка: неккоректный радиус.будет использован радиус 5")
                rad=5
            new_image=my_box_blur(img,rad)
            new_image.save(inoutput)
            filtr="box-filter"
            status="успешно"
            print("новый файл готов")
        elif choise==2:
            try:
                coef=float(input("введите коэффицент насыщенности:"))
            except ValueError:
                print("некорректное значение.будет использован коэффицент 2.0")
                coef=2.0
            new_image=my_color_correction(img,coef)
            new_image.save(inoutput)
            filtr="color-correction"
            status="успешно"
            print("новый файл готов")
        else:
            print("некорректный ввод")
            filtr="не выбран"
except (FileNotFoundError,FileExistsError):
    print("Ошибка: Файл не найден")
    status="не существующий файл"
except (PermissionError,IOError):
    print(f"Ошибка: Нет прав на чтение файла {tekfile}. Обратитесь к администратору")
finally:
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log=f"[{time}] Файл:<{tekfile}> | Фильтр:<{filtr}> | Статус:{status}\n"
    with open (logir,'a',encoding='UTF-8') as f:
        f.write(log)





