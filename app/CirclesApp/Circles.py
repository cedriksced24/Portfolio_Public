import sys
import random
import json
import math
import networkx as nx
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QDialog,
    QTextEdit,
    QInputDialog,
    QFileDialog,
    QLabel,
    QFrame,
    QMessageBox,
)
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QPoint, QPointF, QLineF, QRect


# Calculates the shortest distance from a point to a line segment.
def line_distance_to_point(line: QLineF, point: QPoint) -> float:
    """Calculate the distance from a point to a line segment."""
    p = QPointF(point)
    p1 = line.p1()
    p2 = line.p2()
    dx = p2.x() - p1.x()
    dy = p2.y() - p1.y()
    if dx == 0 and dy == 0:
        return math.hypot(p.x() - p1.x(), p.y() - p1.y())
    t = ((p.x() - p1.x()) * dx + (p.y() - p1.y()) * dy) / (dx * dx + dy * dy)
    if t < 0:
        closest = p1
    elif t > 1:
        closest = p2
    else:
        closest = QPointF(p1.x() + t * dx, p1.y() + t * dy)
    return math.hypot(p.x() - closest.x(), p.y() - closest.y())


# Returns the user-entered text from the dialog.
class TextDialog(QDialog):
    def __init__(self, headline, text="", parent=None):
        super().__init__(parent)
        self.headline = headline
        self.setWindowTitle(f"Text for {headline}")
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(text)
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def getText(self):
        return self.text_edit.toPlainText()


# Initializes a circle widget with position, text, and dragging state.
class CircleWidget(QWidget):
    def __init__(self, headline, position, text="", parent=None):
        super().__init__(parent)
        self.headline = headline
        self.text = text  # stored text for the circle
        self.selected = False
        self.setFixedSize(60, 60)
        self.dragging = False  # track dragging state

    # Draws the circle with its label and highlight if selected.
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(255, 0, 0), 2) if self.selected else QPen(QColor(0, 0, 0), 1)
        painter.setPen(pen)
        painter.setBrush(QColor(200, 200, 255))
        painter.drawEllipse(5, 5, 50, 50)
        painter.setFont(QFont("Arial", 10))
        painter.drawText(5, 5, 50, 50, Qt.AlignCenter, self.headline)

    # Opens a dialog to edit the circle's text on double-click.
    def mouseDoubleClickEvent(self, event):
        dialog = TextDialog(self.headline, self.text, self)
        if dialog.exec_() == QDialog.Accepted:
            self.text = dialog.getText()
            print(f"Text for '{self.headline}' saved: {self.text}")

    # Starts dragging (right-click) or selection (left-click) of a circle.
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.dragging = True
            self.drag_offset = event.pos()  # save offset within the widget
        elif event.button() == Qt.LeftButton:
            if self.parent():
                self.parent().selectCircle(self.headline)

    # Moves the circle as it's being dragged.
    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToParent(event.pos() - self.drag_offset)
            parent = self.parent()
            if parent is not None:
                allowed_x_min = 0
                allowed_x_max = parent.width() - self.width()
                allowed_y_min = parent.separator.geometry().bottom()
                allowed_y_max = parent.height() - self.height()
                new_x = min(max(new_pos.x(), allowed_x_min), allowed_x_max)
                new_y = min(max(new_pos.y(), allowed_y_min), allowed_y_max)
                new_pos = QPoint(new_x, new_y)
            self.move(new_pos)
            parent.update()

    # Stops dragging and updates the circle's stored position.
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.dragging = False
            if self.parent():
                for data in self.parent().circle_data:
                    if data["headline"] == self.headline:
                        data["x"] = self.x()
                        data["y"] = self.y()
                self.parent().update()


class CircleWindow(QWidget):
    # Initializes the main application window with layout and data.
    def __init__(self):
        super().__init__()
        self.circle_widgets = {}
        self.circle_data = []
        self.graph = nx.Graph()
        self.first_clicked_circle = None
        self.initUI()

    # Builds the UI layout and connects button events.
    def initUI(self):
        self.setWindowTitle("Circles")
        self.setGeometry(300, 300, 800, 600)

        # Header label with RGB color.
        self.header_label = QLabel("Circles", self)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet(
            "color: rgb(0,128,255); font-size: 24px; font-weight: bold;"
        )

        # Input field and Add Circle button.
        self.add_headline_input = QLineEdit(self)
        self.add_headline_input.setMaximumWidth(200)
        self.add_button = QPushButton("Add Circle", self)

        # Buttons for loading/saving data.
        self.load_button = QPushButton("Load Data (JSON)", self)
        self.save_txt_button = QPushButton("Save Data (TXT)", self)
        self.load_txt_button = QPushButton("Load Data (TXT)", self)
        self.save_json_button = QPushButton("Save Data (JSON)", self)
        self.help_button = QPushButton("Help", self)

        # Horizontal layout for taskbar.
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.add_headline_input)
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.load_button)
        hbox.addWidget(self.save_txt_button)
        hbox.addWidget(self.load_txt_button)
        hbox.addWidget(self.save_json_button)
        hbox.addWidget(self.help_button)
        hbox.addStretch(1)

        # Separator line.
        self.separator = QFrame(self)
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)

        # Main layout.
        vbox = QVBoxLayout()
        vbox.addWidget(self.header_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.separator)
        vbox.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        self.setLayout(vbox)

        # Connect buttons to methods.
        self.add_button.clicked.connect(self.addCircleFromInput)
        self.load_button.clicked.connect(self.loadData)
        self.save_txt_button.clicked.connect(self.saveDataTxt)
        self.load_txt_button.clicked.connect(self.loadDataTxt)
        self.save_json_button.clicked.connect(self.saveDataJson)
        self.help_button.clicked.connect(self.showHelp)

        self.show()

    # Adds a new circle with given headline and optional text.
    def addCircle(self, headline, text=""):
        if headline in self.circle_widgets:
            return
        # Choose a random position ensuring the circle starts below the separator.
        x = random.randint(50, self.width() - 60)
        y = random.randint(self.separator.geometry().bottom(), self.height() - 60)
        data = {"headline": headline, "x": x, "y": y, "text": text}
        self.circle_data.append(data)
        widget = CircleWidget(headline, QPoint(x, y), text, self)
        widget.move(x, y)
        widget.show()
        self.circle_widgets[headline] = widget
        self.graph.add_node(headline)

    # Reads the input field and adds a new circle.
    def addCircleFromInput(self):
        headline = self.add_headline_input.text()
        if headline:
            self.addCircle(headline)
            self.add_headline_input.clear()

    # Draws edges and their relation labels between circles.
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(100, 100, 100))
        for u, v, data in self.graph.edges(data=True):
            if u in self.circle_widgets and v in self.circle_widgets:
                start_widget = self.circle_widgets[u]
                end_widget = self.circle_widgets[v]
                start_center = start_widget.pos() + QPoint(30, 30)
                end_center = end_widget.pos() + QPoint(30, 30)
                painter.drawLine(start_center, end_center)
                if "relation_name" in data:
                    relation_name = data["relation_name"]
                    mid_point = (start_center + end_center) / 2
                    rect_width = 120
                    rect_height = 30
                    rect = QRect(
                        mid_point.x() - rect_width // 2,
                        mid_point.y() - rect_height // 2,
                        rect_width,
                        rect_height,
                    )
                    painter.save()
                    painter.setBrush(QColor(255, 255, 200))
                    painter.setPen(Qt.NoPen)
                    painter.drawRect(rect)
                    painter.restore()
                    font = QFont("Arial", 10, QFont.Bold)
                    painter.setFont(font)
                    painter.setPen(QPen(QColor(0, 0, 0)))
                    painter.drawText(rect, Qt.AlignCenter, relation_name)

    # Connects two selected circles and prompts for relation name.
    def connectCircles(self, circle1, circle2):
        if not self.graph.has_edge(circle1, circle2):
            relation_name, ok = QInputDialog.getText(
                self, "Relation Name", "Enter relation name:"
            )
            if ok and relation_name:
                self.graph.add_edge(circle1, circle2, relation_name=relation_name)
                self.update()

    # Selects a circle or creates a connection if two are selected.
    def selectCircle(self, headline):
        if self.first_clicked_circle:
            self.first_clicked_circle.selected = False
        if headline in self.circle_widgets:
            widget = self.circle_widgets[headline]
            widget.selected = not widget.selected
            if widget.selected:
                if self.first_clicked_circle and self.first_clicked_circle != widget:
                    self.connectCircles(
                        self.first_clicked_circle.headline, widget.headline
                    )
                    widget.selected = False
                    self.first_clicked_circle.selected = False
                    self.first_clicked_circle = None
                else:
                    self.first_clicked_circle = widget
            else:
                if self.first_clicked_circle == widget:
                    self.first_clicked_circle = None
        self.update()

    # Detects mouse clicks on circles or lines and allows renaming.
    def mousePressEvent(self, event):
        clicked_widget = None
        for widget in self.circle_widgets.values():
            if widget.geometry().contains(event.pos()):
                clicked_widget = widget
                break

        if clicked_widget:
            self.selectCircle(clicked_widget.headline)
        else:
            edge_clicked = False
            for u, v, data in self.graph.edges(data=True):
                if u in self.circle_widgets and v in self.circle_widgets:
                    start_widget = self.circle_widgets[u]
                    end_widget = self.circle_widgets[v]
                    start_center = start_widget.pos() + QPoint(30, 30)
                    end_center = end_widget.pos() + QPoint(30, 30)
                    line = QLineF(start_center, end_center)
                    if line_distance_to_point(line, event.pos()) < 5:
                        edge_clicked = True
                        relation_name, ok = QInputDialog.getText(
                            self,
                            "Rename Relation",
                            "Enter new relation name:",
                            text=data.get("relation_name", ""),
                        )
                        if ok and relation_name:
                            self.graph[u][v]["relation_name"] = relation_name
                            self.update()
                            event.accept()
                            return
            if not edge_clicked:
                if self.first_clicked_circle:
                    self.first_clicked_circle.selected = False
                    self.first_clicked_circle = None
            self.update()
        super().mousePressEvent(event)

    # Saves all circles and connections to a human-readable TXT file.
    def saveDataTxt(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Data (TXT)", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            # Update circle_data with the current text from each widget.
            for headline, widget in self.circle_widgets.items():
                for data in self.circle_data:
                    if data["headline"] == headline:
                        data["text"] = widget.text
            text = "Circles:\n"
            for circle in self.circle_data:
                text += f"Headline: {circle['headline']}, x: {circle['x']}, y: {circle['y']}, text: {circle['text']}\n"
            text += "\nEdges:\n"
            for u, v, data in self.graph.edges(data=True):
                relation_name = data.get("relation_name", "")
                text += f"{u} <-> {v}, relation: {relation_name}\n"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Data saved to {file_name}")

    # Saves all circles and connections to a structured JSON file.
    def saveDataJson(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Data (JSON)", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_name:
            # Update circle_data with the current text from each widget.
            for headline, widget in self.circle_widgets.items():
                for data in self.circle_data:
                    if data["headline"] == headline:
                        data["text"] = widget.text
            data_to_save = {
                "circles": self.circle_data,
                "edges": list(self.graph.edges(data=True)),
            }
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4)
            print(f"Data saved to {file_name}")

    # Loads circle and edge data from a JSON file.
    def loadData(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Data (JSON)", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
            for widget in self.circle_widgets.values():
                widget.deleteLater()
            self.circle_widgets.clear()
            self.circle_data = []
            self.graph = nx.Graph()
            for circle_data in data["circles"]:
                # Pass the stored text to addCircle.
                self.addCircle(circle_data["headline"], circle_data["text"])
                self.circle_widgets[circle_data["headline"]].move(
                    circle_data["x"], circle_data["y"]
                )
            for u, v, edge_data in data["edges"]:
                self.graph.add_edge(u, v, **edge_data)
            self.update()

    # Loads data from a custom-formatted TXT file.
    def loadDataTxt(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Data (TXT)", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                lines = f.readlines()
            circles = []
            edges = []
            circles_section = False
            edges_section = False
            for line in lines:
                line = line.strip()
                if line == "Circles:":
                    circles_section = True
                    edges_section = False
                    continue
                if line == "Edges:":
                    edges_section = True
                    circles_section = False
                    continue
                if circles_section:
                    if not line:
                        continue
                    if line.startswith("Headline: "):
                        content = line[len("Headline: ") :]
                        parts = content.split(",")
                        if len(parts) >= 3:
                            headline = parts[0].strip()
                            x = int(parts[1].split(":")[1].strip())
                            y = int(parts[2].split(":")[1].strip())
                            text_val = ""
                            if len(parts) > 3:
                                text_part = ", ".join(parts[3:]).strip()
                                if text_part.startswith("text:"):
                                    text_val = text_part[len("text:") :].strip()
                            circles.append(
                                {"headline": headline, "x": x, "y": y, "text": text_val}
                            )
                if edges_section:
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) >= 1:
                        nodes_part = parts[0].strip()
                        if "<->" in nodes_part:
                            nodes = nodes_part.split("<->")
                            if len(nodes) == 2:
                                u = nodes[0].strip()
                                v = nodes[1].strip()
                                relation = ""
                                if len(parts) > 1:
                                    relation_part = parts[1].strip()
                                    if relation_part.startswith("relation:"):
                                        relation = relation_part[
                                            len("relation:") :
                                        ].strip()
                                edges.append((u, v, {"relation_name": relation}))
            for widget in self.circle_widgets.values():
                widget.deleteLater()
            self.circle_widgets.clear()
            self.circle_data = []
            self.graph = nx.Graph()
            for circle in circles:
                self.addCircle(circle["headline"], circle["text"])
                self.circle_widgets[circle["headline"]].move(circle["x"], circle["y"])
                self.circle_data.append(circle)
            for u, v, edge_data in edges:
                self.graph.add_edge(u, v, **edge_data)
            self.update()

    # Displays a help message box with usage instructions.
    def showHelp(self):
        help_text = (
            "Help - Features Explanation:\n\n"
            "1. Add Circle: Use the input field and 'Add Circle' button to create a new circle with a unique headline.\n"
            "2. Move Circle: Right-click and hold on a circle, then drag it to reposition. The circle cannot be moved above the separator or outside the window.\n"
            "3. Edit Text: Double-click a circle to open a dialog and edit its text content. The stored text will be shown in the dialog.\n"
            "4. Connect Circles: Left-click on a circle to select it. When two circles are selected sequentially, a connection is created. Click near an edge to rename the connection.\n"
            "5. Save Data (TXT): Save all circles and edges to a text file.\n"
            "6. Load Data (TXT): Load circles and edges from a text file (ensure it follows the correct format).\n"
            "7. Save Data (JSON): Save the current state to a JSON file.\n"
            "8. Load Data (JSON): Load circles and edges from a JSON file.\n"
            "9. Help: Click this button to see this help message.\n\n"
            "Enjoy using the application!"
        )
        QMessageBox.information(self, "Help", help_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircleWindow()
    sys.exit(app.exec_())
