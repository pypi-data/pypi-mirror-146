class Text:
    def __init__(self, renderer, size_obj = None, pos = "auto_XY", gui_obj = None ):
        self.renderer = renderer
        self.gui_obj = gui_obj
        self.pos = pos
        self.size_obj = size_obj
        self.size_txt = renderer.get_size()
        self.tmp_pos = int()

    def caclulate_pos(self):
        if self.pos == "auto_XY":
            return (self.size_obj[0] // 2 - self.size_txt[0] // 2, self.size_obj[1] // 2 - self.size_txt[1] // 2 )

        if self.pos == "auto_X":
            return self.size_obj[0] // 2 - self.size_txt[0] // 2

        if self.pos == "auto_Y":
            return self.size_obj[1] // 2 - self.size_txt[1] // 2



