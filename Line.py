import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("三种绘制直线算法")

# 定义颜色
color = (255, 255, 255)

# 定义直线算法类型
DDA_ALGORITHM = 0
MIDPOINT_ALGORITHM = 1
BRESENHAM_ALGORITHM = 2
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
    a = y0 - y1
    b = x1 - x0
    d = 2 * a + b
    d1 = 2 * a
    d2 = 2 * (a + b)
    x, y = x0, y0
    screen.set_at((x, y), color)
    while x < x1:
        pygame.display.update()  # 更新显示
        pygame.time.delay(10)  # 添加延迟，使绘制慢一点
        if d < 0:
            x += 1
            y += 1
            d += d2
        else:
            x += 1
            d += d1
        screen.set_at((x, y), color)


def Bresenham(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    e = -dx
    x, y = x0, y0
    for _ in range(dx):
        pygame.display.update()  # 更新显示
        pygame.time.delay(10)  # 添加延迟，使绘制慢一点
        screen.set_at((x, y), color)
        x += 1
        e = e + 2 * dy
        if e >= 0:
            y += 1
            e = e - 2 * dx


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
