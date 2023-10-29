import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("种子填充算法演示")

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


# 种子填充算法
def seed_fill(x, y, fill_color, boundary_color):
    stack = [(x, y)]

    while stack:
        x, y = stack.pop()
        current_color = screen.get_at((x, y))
        if current_color == boundary_color or current_color == fill_color:
            continue
        screen.set_at((x, y), fill_color)
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))


# 主循环
drawing = False
boundary_color = (0, 0, 0)
fill_color = (255, 0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not drawing:
                start_point = pygame.mouse.get_pos()
                seed_fill(start_point[0], start_point[1], fill_color, boundary_color)
                drawing = True

    pygame.display.update()
