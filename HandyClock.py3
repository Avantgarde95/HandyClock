import tkinter as tk
import datetime
import math

TABLE_WEEKDAYNAMES = {
    0 : 'Mon',
    1 : 'Tue',
    2 : 'Wed',
    3 : 'Thu',
    4 : 'Fri',
    5 : 'Sat',
    6 : 'Sun'
}

FORMAT_DATE = '%04d.%02d.%02d (%3s)'
OFFSET_UTC = datetime.timedelta(hours = 9)

FONT_DATE = ('', 20, 'bold')
FONT_NUMBERS = ('', 12, 'bold')

WIDTH_CANVAS = 250
HEIGHT_CANVAS = 250

THICKNESS_FRAME = 10
THICKNESS_HOURMARK = 4
THICKNESS_MINUTEMARK = 2
THICKNESS_HOURLINE = 4
THICKNESS_MINUTELINE = 3
THICKNESS_SECONDLINE = 2

RADIUS_FRAME = 100
RADIUS_NUMBERS = 70
RADIUS_HOURMARK = 83
RADIUS_MINUTEMARK = 90
RADIUS_HOURLINE = 35
RADIUS_MINUTELINE = 50
RADIUS_SECONDLINE = 65

DT = 1000

class MainApp(tk.Frame, object):
    def __init__(self, root = None):
        self.root = root

        super(MainApp, self).__init__(self.root)

        self.year = 0
        self.month = 0
        self.day = 0
        self.weekday = 0
        self.hour = 0
        self.minute = 0
        self.second = 0

        self.init_window()
        self.init_frames()
        self.init_widgets()
        self.init_binds()

        self.update_datetime()
        self.update_date()
        self.update_time()

        self.cb_clock()

    def init_window(self):
        self.root.wm_title('HandyClock')
        self.root.resizable(0, 0)

    def init_frames(self):
        self.configure(bg = 'white')

        self.frame_main = tk.Frame(self)
        self.frame_main.pack(pady = 10)

        self.frame_date = tk.Frame(
            self.frame_main,
            bg = 'white'
        )

        self.frame_time = tk.Frame(self.frame_main)
        self.frame_date.pack(expand = tk.YES, fill = tk.BOTH)
        self.frame_time.pack()

    def init_widgets(self):
        self.label_date = tk.Label(
            self.frame_date,
            bg = 'white',
            font = FONT_DATE
        )

        self.label_date.pack()

        self.canvas_time = tk.Canvas(
            self.frame_date,
            width = WIDTH_CANVAS,
            height = HEIGHT_CANVAS,
            bg = 'white',
            highlightthickness = 0
        )

        self.canvas_time.pack()

        self.item_frame = self.canvas_time.create_oval(
            WIDTH_CANVAS / 2 - RADIUS_FRAME - THICKNESS_FRAME / 2,
            HEIGHT_CANVAS / 2 - RADIUS_FRAME - THICKNESS_FRAME / 2,
            WIDTH_CANVAS / 2 + RADIUS_FRAME + THICKNESS_FRAME / 2,
            HEIGHT_CANVAS / 2 + RADIUS_FRAME + THICKNESS_FRAME / 2,
            width = THICKNESS_FRAME,
            fill = 'gray93',
            outline = 'brown',
            tags = 'frame'
        )

        self.item_hourmarks = []
        self.item_minutemarks = []
        self.item_numbers = []

        for i in range(1, 12 + 1):
            angle = 2.0 * math.pi / 12.0 * (i - 3)
            dx = RADIUS_NUMBERS * math.cos(angle)
            dy = RADIUS_NUMBERS * math.sin(angle)

            self.item_numbers.append(
                self.canvas_time.create_text(
                    WIDTH_CANVAS / 2 + dx,
                    HEIGHT_CANVAS / 2 + dy,
                    text = '%02d' % i,
                    font = FONT_NUMBERS,
                    tags = 'number'
                )
            )

        for i in range(1, 12 + 1):
            angle = 2.0 * math.pi / 12.0 * (i - 3)

            dx_1 = RADIUS_HOURMARK * math.cos(angle)
            dy_1 = RADIUS_HOURMARK * math.sin(angle)
            dx_2 = RADIUS_FRAME * math.cos(angle)
            dy_2 = RADIUS_FRAME * math.sin(angle)

            self.item_hourmarks.append(
                self.canvas_time.create_line(
                    WIDTH_CANVAS / 2 + dx_1,
                    HEIGHT_CANVAS / 2 + dy_1,
                    WIDTH_CANVAS / 2 + dx_2,
                    HEIGHT_CANVAS / 2 + dy_2,
                    width = THICKNESS_HOURMARK,
                    tags = 'hourmark'
                )
            )

        for i in range(1, 60 + 1):
            if (i % 5 == 0):
                continue

            angle = 2.0 * math.pi / 60.0 * (i - 15)

            dx_1 = RADIUS_MINUTEMARK * math.cos(angle)
            dy_1 = RADIUS_MINUTEMARK * math.sin(angle)
            dx_2 = RADIUS_FRAME * math.cos(angle)
            dy_2 = RADIUS_FRAME * math.sin(angle)

            self.item_hourmarks.append(
                self.canvas_time.create_line(
                    WIDTH_CANVAS / 2 + dx_1,
                    HEIGHT_CANVAS / 2 + dy_1,
                    WIDTH_CANVAS / 2 + dx_2,
                    HEIGHT_CANVAS / 2 + dy_2,
                    width = THICKNESS_MINUTEMARK,
                    tags = 'minutemark'
                )
            )

        angle_hour = 2.0 * math.pi / 12.0 * (self.hour - 3) \
            + 2.0 * math.pi / (12.0 * 60.0) * self.minute \
            + 2.0 * math.pi / (12.0 * 60.0 * 60.0) * self.second

        angle_minute = 2.0 * math.pi / 60.0 * (self.minute - 15) \
            + 2.0 * math.pi / (60.0 * 60.0) * self.second

        angle_second = 2.0 * math.pi / 60.0 * (self.second - 15)

        dx_hour = RADIUS_HOURLINE * math.cos(angle_hour)
        dy_hour = RADIUS_HOURLINE * math.sin(angle_hour)

        dx_minute = RADIUS_MINUTELINE * math.cos(angle_minute)
        dy_minute = RADIUS_MINUTELINE * math.sin(angle_minute)

        dx_second = RADIUS_SECONDLINE * math.cos(angle_second)
        dy_second = RADIUS_SECONDLINE * math.sin(angle_second)

        self.item_hourline = self.canvas_time.create_line(
            WIDTH_CANVAS / 2,
            HEIGHT_CANVAS / 2,
            WIDTH_CANVAS / 2 + dx_hour,
            HEIGHT_CANVAS / 2 + dy_hour,
            width = THICKNESS_HOURLINE,
            fill = 'blue',
            tags = 'hourline'
        )

        self.item_minuteline = self.canvas_time.create_line(
            WIDTH_CANVAS / 2,
            HEIGHT_CANVAS / 2,
            WIDTH_CANVAS / 2 + dx_minute,
            HEIGHT_CANVAS / 2 + dy_minute,
            width = THICKNESS_MINUTELINE,
            fill = 'dark green',
            tags = 'minuteline'
        )

        self.item_secondline = self.canvas_time.create_line(
            WIDTH_CANVAS / 2,
            HEIGHT_CANVAS / 2,
            WIDTH_CANVAS / 2 + dx_second,
            HEIGHT_CANVAS / 2 + dy_second,
            width = THICKNESS_SECONDLINE,
            fill = 'gray32',
            tags = 'secondline'
        )

    def init_binds(self):
        self.root.bind('<Escape>', self.cb_quit)

    def update_datetime(self):
        today = datetime.datetime.utcnow() + OFFSET_UTC

        self.year = today.year
        self.month = today.month
        self.day = today.day
        self.hour = today.hour % 12
        self.minute = today.minute % 60
        self.second = today.second % 3600
        self.weekday = today.weekday()

    def update_date(self):
        self.label_date.config(
            text = FORMAT_DATE % (
                self.year, self.month, self.day,
                TABLE_WEEKDAYNAMES[self.weekday]
            )
        )

    def update_time(self):
        angle_hour = 2.0 * math.pi / 12.0 * (self.hour - 3) \
            + 2.0 * math.pi / (12.0 * 60.0) * self.minute \
            + 2.0 * math.pi / (12.0 * 60.0 * 60.0) * self.second

        angle_minute = 2.0 * math.pi / 60.0 * (self.minute - 15) \
            + 2.0 * math.pi / (60.0 * 60.0) * self.second

        angle_second = 2.0 * math.pi / 60.0 * (self.second - 15)

        dx_hour = RADIUS_HOURLINE * math.cos(angle_hour)
        dy_hour = RADIUS_HOURLINE * math.sin(angle_hour)

        dx_minute = RADIUS_MINUTELINE * math.cos(angle_minute)
        dy_minute = RADIUS_MINUTELINE * math.sin(angle_minute)

        dx_second = RADIUS_SECONDLINE * math.cos(angle_second)
        dy_second = RADIUS_SECONDLINE * math.sin(angle_second)

        self.canvas_time.coords(
            self.item_hourline,
            WIDTH_CANVAS / 2,
            HEIGHT_CANVAS / 2,
            WIDTH_CANVAS / 2 + dx_hour,
            HEIGHT_CANVAS / 2 + dy_hour,
        )

        self.canvas_time.coords(
            self.item_minuteline,
            WIDTH_CANVAS / 2,
            HEIGHT_CANVAS / 2,
            WIDTH_CANVAS / 2 + dx_minute,
            HEIGHT_CANVAS / 2 + dy_minute
        )

        self.canvas_time.coords(
            self.item_secondline,
            WIDTH_CANVAS / 2,
            HEIGHT_CANVAS / 2,
            WIDTH_CANVAS / 2 + dx_second,
            HEIGHT_CANVAS / 2 + dy_second,
        )

    def cb_clock(self):
        self.update_datetime()
        self.update_date()
        self.update_time()
        self.root.after(DT, self.cb_clock)

    def cb_quit(self, *args, **kwargs):
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MainApp(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
