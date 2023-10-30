import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("直线的裁剪")

# 定义颜色
color = (255, 255, 255)

# 定义直线算法类型
COHEN_SUTHERLAND_ALGORITHM = 1
current_algorithm = COHEN_SUTHERLAND_ALGORITHM  # 默认选择Cohen-Sutherland裁剪算法


# 显示算法选择提示
def show_algorithm_prompt(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width / 2, 20))
    screen.fill((0, 0, 0))  # 清空背景
    screen.blit(font.render('', True, color), text_rect)
    screen.blit(text, text_rect)
    pygame.display.update()


def convert_coordinates(x, y):
    # 将右上角坐标转换为左下角坐标
    return x, screen_height - y


# 定义区域编码
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8
XL, XR, YB, YT = 200, 600, 100, 500


# 区域编码
def encode(x, y):
    c = 0
    if x < XL:
        c |= LEFT
    if x > XR:
        c |= RIGHT
    if y < YB:
        c |= BOTTOM
    if y > YT:
        c |= TOP
    return c


def CS_LineClip(x1, y1, x2, y2):
    code1 = encode(x1, y1)
    code2 = encode(x2, y2)
    while code1 != 0 or code2 != 0:
        if code1 & code2 != 0:
            return
        code = code1 if code1 != 0 else code2
        if LEFT & code != 0:
            x = XL
            y = y1 + (y2 - y1) * (XL - x1) / (x2 - x1)
        elif RIGHT & code != 0:
            x = XR
            y = y1 + (y2 - y1) * (XR - x1) / (x2 - x1)
        elif BOTTOM & code != 0:
            y = YB
            x = x1 + (x2 - x1) * (YB - y1) / (y2 - y1)
        elif TOP & code != 0:
            y = YT
            x = x1 + (x2 - x1) * (YT - y1) / (y2 - y1)
        if code == code1:
            x1, y1 = x, y
            code1 = encode(x, y)
        else:
            x2, y2 = x, y
            code2 = encode(x, y)
    x1, y1 = convert_coordinates(x1, y1)
    x2, y2 = convert_coordinates(x2, y2)
    pygame.draw.line(screen, (255, 215, 0), (x1, y1), (x2, y2))


if __name__ == '__main__':
    show_algorithm_prompt("Algorithm: Cohen-Sutherland Clipping")

    pygame.draw.rect(screen, (255, 250, 240), (200, 100, 400, 400), 1)

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
                        if current_algorithm == COHEN_SUTHERLAND_ALGORITHM:
                            x1, y1 = convert_coordinates(start_point[0], start_point[1])
                            x2, y2 = convert_coordinates(end_point[0], end_point[1])
                            CS_LineClip(x1, y1, x2, y2)
                            drawing = False

        pygame.display.update()
