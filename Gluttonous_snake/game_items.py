# -*- coding: utf-8 -*-
import pygame
from random import randint

'''全局变量'''
BACKGROUND_COLOR = (232, 232, 232)
SCORE_TEXT_COLOR = (192, 192, 192)
TIP_TEXT_COLOR = (64, 64, 64)
SCREEN_RECT = pygame.Rect(0, 0, 640, 480)  # 使用pygame.Rect, 才能调用其中的w和h,元组要指定下标
CELL_SIZE = 20
FOOD_UPDATE_EVENT = pygame.USEREVENT  # 食物更新事件标志
SNAKE_UPDATE_EVENT = pygame.USEREVENT + 1  # 蛇更新事件标志


class Label(object):
    '''标签文本类'''

    def __init__(self, size=32, is_score=True):
        '''初始化标签信息
        :param size 文字大小
        :param is_score 是否得分
        '''
        self.font = pygame.font.SysFont("simhei", size)
        self.is_score = is_score

    def draw(self, window, text):
        '''绘制当前对象的内容'''
        # 判断是否得分, 用不同的颜色
        color = SCORE_TEXT_COLOR if self.is_score else TIP_TEXT_COLOR
        # 渲染文本
        text_surface = self.font.render(text, True, color)
        # 获取文本的矩阵
        text_rect = text_surface.get_rect()
        # 修改文本矩阵的位置,文本左下角位置=窗口左下角位置
        # 如果时得分的时候,文本内容与窗口左下角对齐, 其他:文本中心与窗口中心对齐
        if self.is_score:
            text_rect.bottomleft = window.get_rect().bottomleft
        else:
            text_rect.center = window.get_rect().center
        # 绘制文本内容到窗口
        window.blit(text_surface, text_rect)


class Food(object):
    '''食物类'''

    def __init__(self):
        '''初始化食物数据'''
        self.color = (255, 0, 0)  # 红色
        self.score = 10  # 默认得分为10分
        self.rect = (0, 0, CELL_SIZE, CELL_SIZE)
        # 随机食物初始的位置和宽高
        self.random_rect()

    def draw(self, window):
        if self.rect.w < CELL_SIZE:
            # 向四周放大2个像素
            self.rect.inflate_ip(2, 2)
        '''使用当前食物的矩阵,绘制实心圆形'''
        pygame.draw.ellipse(window, self.color, self.rect)

    def random_rect(self):
        '''计算可用的行数和列数'''
        col = SCREEN_RECT.w / CELL_SIZE - 1
        row = SCREEN_RECT.h / CELL_SIZE - 1
        '''随机分配x,y轴的位置'''
        x = randint(0, col) * CELL_SIZE
        y = randint(0, row) * CELL_SIZE
        '''重新给出食物的位置'''
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.rect.inflate_ip(-CELL_SIZE, -CELL_SIZE)  # 将矩阵修改为0, 各自减去CELL_SIZE大小
        # 设置定时, 时间到了之后重新设置食物位置, 10s
        pygame.time.set_timer(FOOD_UPDATE_EVENT, 30000)


class Snake(object):
    def __init__(self):
        '''初始化蛇的数据'''
        self.dir = pygame.K_RIGHT  # 运动方向
        self.time_interval = 500  # 运动事件间隔
        self.score = 0  # 游戏得分
        self.color = (64, 64, 64)  # 身体颜色
        self.body_list = []  # 身体列表
        '''初始化蛇的数据'''
        self.reset_snake()

    def reset_snake(self):
        '''重置蛇的数据'''
        self.dir = pygame.K_RIGHT
        self.time_interval = 300
        self.score = 0
        self.body_list = []
        '''清空蛇的身体列表'''
        self.body_list.clear()
        '''初始创建三个身体'''
        for _ in range(3): self.add_node()

    def add_node(self):
        '''添加蛇的身体'''
        if self.body_list:
            '''已经有身体, 生成新的矩形对象'''
            head = self.body_list[0].copy()
        else:
            '''还没有身体'''
            head = pygame.Rect(-CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

        # 根据移动方向, 将新生成的head放到合适的位置
        if self.dir == pygame.K_LEFT:
            head.x -= CELL_SIZE
        elif self.dir == pygame.K_RIGHT:
            head.x += CELL_SIZE
        elif self.dir == pygame.K_UP:
            head.y -= CELL_SIZE
        elif self.dir == pygame.K_DOWN:
            head.y += CELL_SIZE

        # 把新生成的头部放到列表的最前面
        self.body_list.insert(0, head)
        # 定时更新身体
        pygame.time.set_timer(SNAKE_UPDATE_EVENT, self.time_interval)

    def draw(self, window):
        '''画蛇的每一节身体'''
        for idx, rect in enumerate(self.body_list):
            # idx==0, true=1 false=0
            pygame.draw.rect(window, self.color, rect.inflate(-2, -2), idx == 0)

    def update(self):
        '''备份移动之前的身体位置'''
        body_list_copy = self.body_list.copy()
        '''移动蛇的身体'''
        self.add_node()
        self.body_list.pop()
        '''判断是否死亡'''
        if self.is_dead():
            '''如果死亡将身体还原为上一步的样子'''
            self.body_list = body_list_copy
            return False
        return True

    def change(self, to_dir):
        '''修改蛇的移动方向'''
        # 水平方向
        hor_dirs = (pygame.K_LEFT, pygame.K_RIGHT)
        #垂直方向
        ver_dirs = (pygame.K_UP, pygame.K_DOWN)
        '''如果当前方向水平方向, 则修改的移动方向不能为水平方向, 垂直方向同理'''
        if (self.dir in hor_dirs and to_dir not in hor_dirs) \
            or (self.dir in ver_dirs and to_dir not in ver_dirs):
            self.dir = to_dir

    def has_eat(self, food):
        '''判断是否吃到了食物'''
        if self.body_list[0].contains(food.rect):
            '''如果蛇头和食物的位置重叠, 修改得分'''
            self.score += food.score
            '''修改移动间隔'''
            if self.time_interval > 50:
                self.time_interval -= 5
            '''增加一节身体'''
            self.add_node()
            return True
        return False

    def is_dead(self):
        '''判断是否死亡, 死亡返回True'''
        head = self.body_list[0] #获取蛇头
        '''判断蛇头是否不在窗口里'''
        if not SCREEN_RECT.contains(head):
            return True
        '''判断蛇头是否与身体重叠'''
        for body in self.body_list[1:]:
            if head.contains(body):
                return True
        return False