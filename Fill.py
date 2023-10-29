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
region_color = (255, 250, 240)
fill_color = (255, 215, 0)

# 定义画圆算法类型
FLOOD_ALGORITHM = 1
SCANLINE_ALGORITHM = 2
current_algorithm = FLOOD_ALGORITHM  # 默认选择中点画圆算法


# 显示算法选择提示
def show_algorithm_prompt(message):
    screen.fill((0, 0, 0))  # 清空背景
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width / 2, 20))
    screen.blit(font.render('', True, color), text_rect)
    screen.blit(text, text_rect)
    pygame.display.update()


# 种子填充算法
def FloodFill4(x, y, old_color, new_color):
    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        if screen.get_at((x, y)) == old_color:
            pygame.display.update()  # 更新显示
            pygame.time.delay(5)  # 添加延迟，使绘制慢一点
            screen.set_at((x, y), new_color)
            stack.append((x, y + 1))
            stack.append((x, y - 1))
            stack.append((x - 1, y))
            stack.append((x + 1, y))

    # 函数递归法会堆栈溢出
    # if screen.get_at((x, y)) == old_color:
    #     pygame.display.update()  # 更新显示
    #     pygame.time.delay(10)  # 添加延迟，使绘制慢一点
    #     screen.set_at((x, y), new_color)
    #     FloodFill4(x, y + 1, old_color, new_color)
    #     FloodFill4(x, y - 1, old_color, new_color)
    #     FloodFill4(x - 1, y, old_color, new_color)
    #     FloodFill4(x + 1, y, old_color, new_color)


def ScanLineFill4(x, y, old_color, new_color):
    stack = [(x, y)]
    while stack:
        pt = stack.pop()
        x, y = pt
        while screen.get_at((x, y)) == old_color:  # 向右填充
            pygame.display.update()  # 更新显示
            pygame.time.delay(5)  # 添加延迟，使绘制慢一点
            screen.set_at((x, y), new_color)
            x += 1
        xr = x - 1
        x = pt[0] - 1
        while screen.get_at((x, y)) == old_color:  # 向左填充
            pygame.display.update()  # 更新显示
            pygame.time.delay(1)  # 添加延迟，使绘制慢一点
            screen.set_at((x, y), new_color)
            x -= 1
        xl = x + 1
        # 处理上面一条扫描线
        x = xl
        y += 1
        while x <= xr:
            spanNeedFill = False
            while screen.get_at((x, y)) == old_color:
                spanNeedFill = True
                x += 1
            if spanNeedFill:
                stack.append((x - 1, y))
            while screen.get_at((x, y)) != old_color and x <= xr:
                x += 1
        x = xl
        y -= 2
        while x <= xr:
            spanNeedFill = False
            while screen.get_at((x, y)) == old_color:
                spanNeedFill = True
                x += 1
            if spanNeedFill:
                stack.append((x - 1, y))
            while screen.get_at((x, y)) != old_color and x <= xr:
                x += 1


if __name__ == '__main__':
    show_algorithm_prompt("Algorithm: FloodFill4")

    drew_region = False
    drawing = False
    # 主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_algorithm = FLOOD_ALGORITHM
                    show_algorithm_prompt("Algorithm: FloodFill4")
                elif event.key == pygame.K_2:
                    current_algorithm = SCANLINE_ALGORITHM
                    show_algorithm_prompt("Algorithm: ScanLineFill4")
            elif not drew_region:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                    path = [event.pos]
                elif event.type == pygame.MOUSEMOTION and drawing:
                    # noinspection PyUnboundLocalVariable
                    path.append(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP and drawing:
                    path.append(event.pos)
                    pygame.draw.polygon(screen, region_color, path)
                    pygame.display.update()  # 更新显示
                    drew_region = True
                    drawing = False
            elif drew_region:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_point = pygame.mouse.get_pos()
                    if current_algorithm == FLOOD_ALGORITHM:
                        FloodFill4(start_point[0], start_point[1], region_color, fill_color)
                    elif current_algorithm == SCANLINE_ALGORITHM:
                        ScanLineFill4(start_point[0], start_point[1], region_color, fill_color)
                    drew_region = False

        pygame.display.update()
