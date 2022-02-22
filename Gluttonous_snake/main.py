# -*- coding: utf-8 -*-
import sys
from game_items import *


class Game(object):

    def __init__(self):
        # 初始化窗口
        self.main_window = pygame.display.set_mode((640, 480), 0, 32)
        # 初始化窗口名
        pygame.display.set_caption("贪吃蛇")
        # 游戏是否结束
        self.is_game_over = False
        # 游戏是否暂停
        self.is_pause = False
        # 得分的标签
        self.score_label = Label()
        # 初始化得分
        self.score = 0
        # 暂停和游戏结束的标签
        self.tip_label = Label(24, False)
        # 初始化食物
        self.food = Food()
        #创建蛇对象
        self.snake = Snake()

    '''启动并控制游戏'''

    def start(self):
        clock = pygame.time.Clock()  # 创建时钟对象
        while True:

            for event in pygame.event.get():
                # 点击 X 事件
                if event.type == pygame.QUIT:
                    sys.exit()
                # 键盘按下事件
                if event.type == pygame.KEYDOWN:
                    # ESC键
                    if event.key == pygame.K_ESCAPE:
                        pass
                    # 空格键, 触发暂停
                    if event.key == pygame.K_SPACE:
                        #若游戏结束, 重置游戏
                        if self.is_game_over:
                            self.reset_game()
                        else:
                            # 取反, 触发暂停
                            self.is_pause = not self.is_pause
                # 只有游戏没有结束 没有暂停 出发更新事件 更新食物位置
                if not self.is_pause and not self.is_game_over:
                    # 触发用户事件(自定义食物更新事件)
                    if event.type == FOOD_UPDATE_EVENT:
                        # 食物位置更新
                        self.food.random_rect()
                    elif event.type == SNAKE_UPDATE_EVENT:
                        # 蛇的位置更新,返回是否移动成功,移动失败返回false说明死亡,说明游戏应该结束了
                        # 取反, 使is_game_over为true
                        self.is_game_over = not self.snake.update()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
                            self.snake.change(event.key)

            # 设置背景颜色
            self.main_window.fill(BACKGROUND_COLOR)
            # 绘制得分(文本)
            self.score_label.draw(self.main_window, "得分:%s" % (self.snake.score))
            # 绘制暂停或游戏结束标签
            if self.is_game_over:
                self.tip_label.draw(self.main_window, "游戏结束,按空格键开启新游戏...")
            elif self.is_pause:
                self.tip_label.draw(self.main_window, "游戏暂停,按空格键继续...")
            else:
                if self.snake.has_eat(self.food):
                    '''如果返回为True说明食物已经被吃掉,刷新食物的位置'''
                    self.food.random_rect()

            # 绘制食物
            self.food.draw(self.main_window)
            #绘制贪吃蛇
            self.snake.draw(self.main_window)
            # 刷新窗口内容
            pygame.display.update()
            # 刷新帧数, 60帧/秒
            clock.tick(60)

    def reset_game(self):
        '''重置游戏参数'''
        self.is_pause = False
        self.is_game_over = False
        self.score = 0
        '''重置蛇的数据'''
        self.snake.reset_snake()
        '''重置食物位置'''
        self.food.random_rect()

if __name__ == '__main__':
    pygame.init()
    Game().start()
    pygame.quit()
