import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("基本图形元素的生成算法(圆、椭圆)")

# 屏幕中心坐标
center_x = screen_width // 2
center_y = screen_height // 2

# 定义颜色
color = (255, 255, 255)

# 定义画圆算法类型
MIDPOINT_ALGORITHM = 1
BRESENHAM_ALGORITHM = 2
ELLIPTIC_MIDPOINT_ALGORITHM = 3
current_algorithm = MIDPOINT_ALGORITHM  # 默认选择中点画圆算法


# 显示算法选择提示
def show_algorithm_prompt(message):
    screen.fill((0, 0, 0))  # 清空背景
    pygame.draw.circle(screen, color, (center_x, center_y), 3)

    font = pygame.font.Font(None, 36)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width / 2, 20))
    screen.blit(font.render('', True, color), text_rect)
    screen.blit(text, text_rect)
    pygame.display.update()


# 转换坐标函数，将屏幕中心作为原点
def transform_coordinates(x, y):
    return int(x + center_x), int(center_y - y)


# 对称画圆
def CirclePoints(x, y):
    pygame.display.update()  # 更新显示
    pygame.time.delay(10)  # 添加延迟，使绘制慢一点
    if current_algorithm == MIDPOINT_ALGORITHM:
        screen.set_at(transform_coordinates(x, y), color)
        screen.set_at(transform_coordinates(x, -y), color)
        screen.set_at(transform_coordinates(-x, y), color)
        screen.set_at(transform_coordinates(-x, -y), color)
        screen.set_at(transform_coordinates(y, x), color)
        screen.set_at(transform_coordinates(y, -x), color)
        screen.set_at(transform_coordinates(-y, x), color)
        screen.set_at(transform_coordinates(-y, -x), color)
    elif (current_algorithm == BRESENHAM_ALGORITHM
          or current_algorithm == ELLIPTIC_MIDPOINT_ALGORITHM):
        screen.set_at(transform_coordinates(x, y), color)
        screen.set_at(transform_coordinates(x, -y), color)
        screen.set_at(transform_coordinates(-x, y), color)
        screen.set_at(transform_coordinates(-x, -y), color)


# 中点画圆算法
def MidPoint(r):
    x = 0
    y = r
    d = 1 - r
    CirclePoints(x, y)
    while x <= y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        CirclePoints(x, y)


# Bresenham画圆算法
def Bresenham(r):
    x, y = 0, r
    Delta = 2 * (1 - r)
    Limit = 0
    while y >= Limit:
        CirclePoints(x, y)
        if Delta < 0:
            Delta1 = 2 * (Delta + y) - 1
            direction = 1 if Delta1 <= 0 else 2
        elif Delta > 0:
            Delta2 = 2 * (Delta - x) - 1
            direction = 2 if Delta2 < 0 else 3
        else:
            direction = 2
        if direction == 1:
            x += 1
            Delta += 2 * x + 1
        elif direction == 2:
            x += 1
            y -= 1
            Delta += 2 * (x - y + 1)
        elif direction == 3:
            y -= 1
            Delta += (-2 * y + 1)


def Elliptic_MidPoint(a, b):
    x = int(a + 1 / 2)
    y = 0
    taa = a * a
    t2aa = 2 * taa
    t4aa = 2 * t2aa
    tbb = b * b
    t2bb = 2 * tbb
    t4bb = 2 * t2bb
    t2bbx = t2bb * x
    tx = x
    d1 = t2bbx * (x - 1) + tbb / 2 + t2aa * (a - tbb)
    while t2bb * tx > t2aa * y:
        CirclePoints(x, y)
        if d1 < 0:
            y += 1
            d1 += t4aa * y + t2aa
            tx = x - 1
        else:
            x -= 1
            y += 1
            d1 += -t4bb * x + t4aa * y + t2aa
            tx = x
    d2 = t2bb * (x * x + 1) - t4bb * x + t2aa * (y * y + y - tbb) + taa / 2
    while x >= 0:
        CirclePoints(x, y)
        if d2 < 0:
            x -= 1
            y += 1
            d2 += t4aa * y - t4bb * x + t2bb
        else:
            x -= 1
            d2 += -t4bb * x + t2bb


if __name__ == '__main__':
    show_algorithm_prompt("Algorithm: MidPoint")

    drawing = False
    start_point = None
    # 主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_point = pygame.mouse.get_pos()
                radius = pow(pow(start_point[0] - center_x, 2) + pow(start_point[1] - center_y, 2), 0.5)
                if current_algorithm == MIDPOINT_ALGORITHM:
                    MidPoint(radius)
                elif current_algorithm == BRESENHAM_ALGORITHM:
                    Bresenham(radius)
                elif current_algorithm == ELLIPTIC_MIDPOINT_ALGORITHM:
                    Elliptic_MidPoint(a=radius / 4, b=radius / 2)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_algorithm = MIDPOINT_ALGORITHM
                    show_algorithm_prompt("Algorithm: MidPoint")
                elif event.key == pygame.K_2:
                    current_algorithm = BRESENHAM_ALGORITHM
                    show_algorithm_prompt("Algorithm: Bresenham")
                elif event.key == pygame.K_3:
                    current_algorithm = ELLIPTIC_MIDPOINT_ALGORITHM
                    show_algorithm_prompt("Algorithm: Elliptic MidPoint")

        pygame.display.update()
