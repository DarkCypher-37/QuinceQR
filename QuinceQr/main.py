import QuinceQr as QR

from PIL import Image

from dataclasses import dataclass
from typing import Tuple

import arcade
import numpy as npa
from PIL import Image
import qrcode

@dataclass
class Colors:
    background: Tuple[int, int, int] = (30, 30, 30)
    text: Tuple[int, int, int] = (210, 210, 210)
    accent_color_1: Tuple[int, int, int] = (94, 92, 230)    # Deep purple
    accent_color_2: Tuple[int, int, int] = (246, 109, 106)  # Coral red
    accent_color_3: Tuple[int, int, int] = (0, 199, 183)    # Bright turquoise
    button_color: Tuple[int, int, int] = (59, 59, 59)
    button_text_color: Tuple[int, int, int] = (255, 255, 255)
    hover_focus_color: Tuple[int, int, int] = (76, 76, 76)
    selected_color: Tuple[int, int, int] = (34, 34, 34)
    mouse_highlighter: Tuple[int, int, int] = (255, 165, 0) # Bright orange

# import arcade
# import arcade.gui

# class MyView(arcade.View):
#     def __init__(self):
#         super().__init__()
#         self.ui_manager = arcade.gui.UIManager()
#         self.input_box = None

#     def on_show(self):
#         self.input_box = arcade.gui.UIInputText(
#             center_x=self.window.width / 2,
#             center_y=self.window.height / 2,
#             width=400,
#             height=50
#         )
#         self.ui_manager.add_view(self.input_box)

#     def on_draw(self):
#         arcade.start_render()
#         arcade.draw_text("Enter your name:", 100, 300, arcade.color.BLACK, 20)

#     def on_update(self, delta_time):
#         pass

# def main():
#     window = arcade.Window(title="My Window", width=800, height=600)
#     view = MyView()
#     window.show_view(view)
#     arcade.run()

# if __name__ == "__main__":
#     main()


# import arcade
# import arcade.gui as gui

# # --- Method 1 for handling click events,
# # Create a child class.
# class QuitButton(arcade.gui.UIFlatButton):
#     def on_click(self, event: arcade.gui.UIOnClickEvent):
#         arcade.exit()

# class MyWindow(arcade.Window):
#     def __init__(self):
#         super().__init__(400, 300, "UI Example", resizable=True)
#         self.manager = gui.UIManager()
#         self.manager.enable()

#         arcade.set_background_color(arcade.color.BEIGE)
        
#         # Create a text label
#         self.label = arcade.gui.UILabel(
#             text="look here for change",
#             text_color=arcade.color.DARK_RED,
#             width=350,
#             height=40,
#             font_size=24,
#             font_name="Kenney Future")

#         # Create an text input field
#         self.input_field = gui.UIInputText(
#           color=arcade.color.DARK_BLUE_GRAY,
#           font_size=24,
#           width=200,
#           text='')

#         # Create a button
#         submit_button = gui.UIFlatButton(
#           color=arcade.color.DARK_BLUE_GRAY,
#           text='Submit')
#         # --- Method 2 for handling click events,
#         # assign self.on_click_start as callback
#         submit_button.on_click = self.on_click 
        
#         self.v_box = gui.UIBoxLayout()
#         self.v_box.add(self.label.with_space_around(bottom=0))
#         self.v_box.add(self.input_field)
#         self.v_box.add(submit_button)
#         self.v_box.add(QuitButton(text="Quit"))
        
#         self.manager.add(
#             arcade.gui.UIAnchorWidget(
#                 anchor_x="center_x",
#                 anchor_y="center_y",
#                 child=self.v_box)
#         )


#     def update_text(self):
#         print(f"updating the label with input text '{self.input_field.text}'")
#         self.label.text = self.input_field.text    

#     def on_click(self, event):
#         print(f"click-event caught: {event}")
#         self.update_text()

        
#     def on_draw(self):
#         arcade.start_render()
#         self.manager.draw()


# window = MyWindow()
# arcade.run()

def main():
    # qr = QR.QrCode("HELLO WORLD", QR.ErrorCorrectionLevel.M)
    # img = qr.make_image()
    # img.show()
    
    qr = QR.QrCode("https://www.youtube.com/watch?v=dQw4w9WgXcQ", QR.ErrorCorrectionLevel.Q)
    
    img:Image = qr.make_image()
    img.save("QuinceQr/test.png")


if __name__ == "__main__":
    main()