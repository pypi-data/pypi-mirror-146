import time
import sys
import pygame

from src.pyg_gui.helper_files.text_class import Text




class Button:
    def __init__(self,window,pos,size,colour,txt_obj, listeners, listener_atributes):
        self.window = window
        self.pos = pos
        self.size = size
        self.listeners = listeners
        self.colour = colour
        self.txt_obj = txt_obj
        self.listener_atributes = listener_atributes
        ###
        if self.txt_obj:
            self.txt_obj.size_obj = self.size
        self.surface = pygame.Surface([self.size[0],size[1]])
        self.surface.fill(colour)
        self.rect = pygame.Rect(size,pos)
        print(self.rect)

    def draw(self):
        if self.txt_obj:
            self.render_txt()
        self.window.blit(self.surface,self.pos)

    def check_press(self,e):
        if pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    for i_funcs,funcs in enumerate(self.listeners):

                        funcs(self.listener_atributes[i_funcs])


    def non_event_update(self):
        self.surface = pygame.Surface([self.size[0], self.size[1]])
        self.rect = pygame.Rect(self.pos,self.size)
        self.surface.fill(self.colour)
        self.draw()


    def event_update(self,e):
        self.check_press(e)

    def render_txt(self):
        if self.txt_obj.pos == "auto_XY":
            self.surface.blit(self.txt_obj.renderer, (self.txt_obj.caclulate_pos()))
        elif self.txt_obj.pos == "auto_X":
            self.surface.blit(self.txt_obj.renderer, (self.txt_obj.caclulate_pos(), 0))
        elif self.txt_obj.pos == "auto_Y":
            self.surface.blit(self.txt_obj.renderer, (0, self.txt_obj.caclulate_pos()))






