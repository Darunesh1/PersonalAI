from dotenv import load_dotenv
load_dotenv()
from kivy import app,clock
from charles import Charles


class MykivyApp(app.App):
    def build(self):
        charles = Charles()
        charles.start_listening()
        
        self.update_event = clock.Clock.schedule_interval(charles.update_circle,1/60)
        self.btn_rotation_event = clock.Clock.schedule_interval(charles.circle.rotate_button,1/60)
        
        return charles
    
if __name__ == "__main__":
    MykivyApp().run()