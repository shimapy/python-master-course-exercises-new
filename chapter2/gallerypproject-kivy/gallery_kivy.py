import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button


class GalleryApp(App):

    def build(self):
        # self.folder_path = "Images"
        self.folder_path = os.path.join(os.path.dirname(__file__), "Images")
        self.images = [
            os.path.join(self.folder_path, file)
            for file in os.listdir(self.folder_path)
            if file.endswith((".png", ".jpg", ".jpeg"))
        ]

        self.index = 0

        layout = BoxLayout(orientation='vertical')
        self.img = Image(source=self.images[self.index])
        btn = Button(text="Next Image", size_hint=(1, 0.2))
        btn.bind(on_press=self.next_image)

        layout.add_widget(self.img)
        layout.add_widget(btn)

        return layout

    def next_image(self, instance):

        self.index += 1
        if self.index >= len(self.images):
            self.index = 0

        self.img.source = self.images[self.index]


GalleryApp().run()