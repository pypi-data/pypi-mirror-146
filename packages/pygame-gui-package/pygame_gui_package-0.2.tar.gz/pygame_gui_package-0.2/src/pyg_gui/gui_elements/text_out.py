import sys, time, pygame

class Txt_out:
    def __init__(self,win, pos, size, color, txt_obj):
        self.win = win
        self.pos = pos
        self.size = size
        self.color = color
        self.txt_obj = txt_obj
        ###
        txt_obj.size_obj = size
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.rect = pygame.Rect(size,pos)
        self.scroll_pos = 0
        self.on_focus = False

    def draw(self):
        self.win.blit(self.surface, (self.pos))

    def check_focus(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:

            if pygame.mouse.get_pressed()[0] == True:
                if not self.on_focus:
                    self.on_focus = True
                else:
                    self.on_focus = False

    def draw_txt(self):

        if self.txt_obj.renderer.get_width() <= self.size[0]:
            self.surface.blit(self.txt_obj.renderer, self.txt_obj.calculate_pos())
        else:
            self.surface.blit(self.txt_obj.renderer, (0, self.size[1] // 2 - self.txt_obj.renderer.get_size()[1] // 2), (self.scroll_pos, 0, self.size[0], self.size[1]))

    def update_draw_pos(self, e):
        if self.on_focus:
            if e.type == pygame.MOUSEWHEEL:
                if e.y == 1:
                    if self.scroll_pos + self.size[0] <= self.txt_obj.renderer.get_width():
                        self.scroll_pos += 20

                if e.y == -1:
                    if self.scroll_pos >= 0:
                        self.scroll_pos -= 20


    def non_event_update(self):
        self.draw_txt()
        self.draw()
        self.surface.fill(self.color)


    def event_update(self, e):
        self.check_focus(e)
        self.update_draw_pos(e)





