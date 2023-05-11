class Quizz():

    def __init__(self):
        pass

    def create_buttons(self, buttons_content:list=["content"], buttons_value = "value", buttons_color:list=["btn btn-primary"]):
        self.buttons = []
        if len(buttons_color) == 1:
            buttons_color = [buttons_color[0] for _ in range(len(buttons_content))]
        print(buttons_color)
        for i in range(len(buttons_content)):
            self.buttons.append({"content": buttons_content[i], "value":buttons_value[i], "color":buttons_color[i]})
        return self.buttons