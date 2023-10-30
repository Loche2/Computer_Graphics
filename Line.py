import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("基本图形元素的生成算法(直线)")

# 定义颜色
color = (255, 255, 255)

# 定义直线算法类型
DDA_ALGORITHM = 1
MIDPOINT_ALGORITHM = 2
BRESENHAM_ALGORITHM = 3
current_algorithm = DDA_ALGORITHM  # 默认选择DDA算法


# DDA绘制直线函数
def DDA(x0, y0, x1, y1):
    steps = abs(x1 - x0) if abs(x1 - x0) > abs(y1 - y0) else abs(y1 - y0)
    increment_x = (x1 - x0) / steps
    increment_y = (y1 - y0) / steps
    x, y = x0, y0
    for _ in range(1, steps + 1):
        pygame.display.update()  # 更新显示
        pygame.time.delay(10)  # 添加延迟，使绘制慢一点
        screen.set_at((int(x), int(y)), color)
        x += increment_x
        y += increment_y


def MidPoint(x0, y0, x1, y1):
    # a = y0 - y1
    # b = x1 - x0
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    step_x = 1 if x0 < x1 else -1
    step_y = 1 if y0 < y1 else -1
    # d1 = 2 * a
    # d2 = 2 * (a + b)
    x, y = x0, y0
    screen.set_at((x, y), color)
    if dx > dy:
        # 斜率小于1，沿 x 轴移动
        d = 2 * dy - dx
        d1 = 2 * dy
        d2 = 2 * (dy - dx)
        while x != x1:
            pygame.display.update()  # 更新显示
            pygame.time.delay(10)  # 添加延迟，使绘制慢一点
            screen.set_at((x, y), color)
            x += step_x
            if d < 0:
                d += d1
            else:
                d += d2
                y += step_y
    else:
        # 斜率大于1，沿 y 轴移动
        d = 2 * dx - dy
        d1 = 2 * dx
        d2 = 2 * (dx - dy)
        while y != y1:
            pygame.display.update()  # 更新显示
            pygame.time.delay(10)  # 添加延迟，使绘制慢一点
            screen.set_at((x, y), color)
            y += step_y
            if d < 0:
                d += d1
            else:
                d += d2
                x += step_x
    # 最后一个点
    screen.set_at((x1, y1), color)

    # while x < x1:
    #     pygame.display.update()  # 更新显示
    #     pygame.time.delay(10)  # 添加延迟，使绘制慢一点
    #     if d < 0:
    #         x += 1
    #         y += 1
    #         d += d2
    #     else:
    #         x += 1
    #         d += d1
    #     screen.set_at((x, y), color)


def Bresenham(x0, y0, x1, y1):
    # dx = x1 - x0
    # dy = y1 - y0
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    if x0 < x1:
        x_step = 1
    else:
        x_step = -1
    if y0 < y1:
        y_step = 1
    else:
        y_step = -1
    # e = -dx
    # x, y = x0, y0
    # for _ in range(dx):
    #     pygame.display.update()  # 更新显示
    #     pygame.time.delay(10)  # 添加延迟，使绘制慢一点
    #     screen.set_at((x, y), color)
    #     x += 1
    #     e = e + 2 * dy
    #     if e >= 0:
    #         y += 1
    #         e = e - 2 * dx
    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx):
            pygame.display.update()  # 更新显示
            pygame.time.delay(10)  # 添加延迟，使绘制慢一点
            screen.set_at((x0, y0), color)
            if p >= 0:
                y0 += y_step
                p -= 2 * dx
            x0 += x_step
            p += 2 * dy
    else:
        p = 2 * dx - dy
        for _ in range(dy):
            pygame.display.update()  # 更新显示
            pygame.time.delay(10)  # 添加延迟，使绘制慢一点
            screen.set_at((x0, y0), color)
            if p >= 0:
                x0 += x_step
                p -= 2 * dy
            y0 += y_step
            p += 2 * dx


# 显示算法选择提示
def show_algorithm_prompt(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width / 2, 20))
    screen.fill((0, 0, 0))  # 清空背景
    screen.blit(font.render('', True, color), text_rect)
    screen.blit(text, text_rect)
    pygame.display.update()


if __name__ == '__main__':
    show_algorithm_prompt("Algorithm: DDA")

    drawing = False
    start_point = None
    # 主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not drawing:
                    start_point = pygame.mouse.get_pos()
                    pygame.draw.circle(screen, color, start_point, 3)
                    drawing = True
                else:
                    end_point = pygame.mouse.get_pos()
                    pygame.draw.circle(screen, color, end_point, 3)
                    if start_point != end_point:
                        if current_algorithm == DDA_ALGORITHM:
                            DDA(start_point[0], start_point[1], end_point[0], end_point[1])
                        elif current_algorithm == MIDPOINT_ALGORITHM:
                            MidPoint(start_point[0], start_point[1], end_point[0], end_point[1])
                        elif current_algorithm == BRESENHAM_ALGORITHM:
                            Bresenham(start_point[0], start_point[1], end_point[0], end_point[1])
                        drawing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_algorithm = DDA_ALGORITHM
                    show_algorithm_prompt("Algorithm: DDA")
                elif event.key == pygame.K_2:
                    current_algorithm = MIDPOINT_ALGORITHM
                    show_algorithm_prompt("Algorithm: MidPoint")
                elif event.key == pygame.K_3:
                    current_algorithm = BRESENHAM_ALGORITHM
                    show_algorithm_prompt("Algorithm: Bresenham")

        pygame.display.update()
