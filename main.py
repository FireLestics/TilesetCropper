import os
import configparser
from PIL import Image

def crop_tileset(config_file):
    """
    Разрезает тайлсет на отдельные тайлы и сохраняет их в папку.

    Args:
        config_file (str): Путь к INI файлу конфигурации.
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    for section in config.sections():
        try:
            tileset_name = config[section]['tileset_name']
            tileset_path = config[section]['tileset_path']
            tile_width = int(config[section]['tile_width'])
            tile_height = int(config[section]['tile_height'])
            margin = int(config[section]['margin'])
            spacing = int(config[section]['spacing'])
            transparent_color_rgb = tuple(map(int, config[section]['transparent_color_rgb'].split(','))) if config[section].get('transparent_color_rgb') else None
            output_folder = tileset_name

            print(f"Обработка тайлсета: {tileset_path}, Имя папки: {output_folder}")

            if not os.path.exists(tileset_path):
                print(f"Ошибка: Файл тайлсета не найден: {tileset_path}")
                continue

            image = Image.open(tileset_path).convert("RGBA")
            width, height = image.size

            # Создаем выходную папку, если она не существует
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            tile_count = 1
            for y in range(margin, height - margin, tile_height + spacing):
                for x in range(margin, width - margin, tile_width + spacing):
                    tile = image.crop((x, y, x + tile_width, y + tile_height))
                    
                    # Делаем прозрачным указанный цвет
                    if transparent_color_rgb:
                      tile = make_transparent(tile, transparent_color_rgb)

                    tile_filename = os.path.join(output_folder, f"{tile_count}.png") # Убрали форматирование для ведущих нулей
                    tile.save(tile_filename)
                    tile_count += 1
            print(f"   Сохранено {tile_count-1} тайлов в {output_folder}")

        except KeyError as e:
             print(f"Ошибка: Отсутствует обязательный параметр в секции {section}: {e}")
        except ValueError as e:
             print(f"Ошибка: Некорректное значение параметра в секции {section}: {e}")
        except Exception as e:
             print(f"Ошибка при обработке секции {section}: {e}")

def make_transparent(image, transparent_color_rgb):
    """Делает прозрачным указанный цвет в изображении"""

    image = image.convert("RGBA")
    pixels = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            if pixels[x, y][:3] == transparent_color_rgb:
                pixels[x, y] = (0, 0, 0, 0)  # Делаем пиксель полностью прозрачным

    return image

if __name__ == "__main__":
    config_file = "config.ini"  # Имя файла с конфигурацией
    if not os.path.exists(config_file):
        print(f"Ошибка: Файл конфигурации не найден: {config_file}")
    else:
        crop_tileset(config_file)
