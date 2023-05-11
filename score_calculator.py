import sys
import json
import hashlib
from PyQt5.QtWidgets import QApplication,  QMainWindow, QLabel, QLineEdit, QInputDialog, QPushButton, QVBoxLayout, QWidget, QListWidget, QHBoxLayout, QMessageBox, QFileDialog, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap , QImage
import os
import shutil

class PhotoViewer(QMainWindow):
    def __init__(self, photo_path):
        super().__init__()
        self.setWindowTitle('Photo Viewer')
        self.setGeometry(100, 100, 400, 300)
        
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        view.setGeometry(0, 0, 400, 300)
        
        pixmap = QPixmap(photo_path)
        image = QImage(pixmap.toImage())
        scene.addPixmap(QPixmap.fromImage(image))
class ScoreCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(400, 300)
        layout.addWidget(self.photo_label)
        self.setWindowTitle('Score Calculator')
        self.setGeometry(100, 100, 400, 300)
        self.questions = []
        self.question_list = QListWidget()
        self.question_list.setMaximumWidth(200)
        self.question_list.setMinimumHeight(150)

        add_button = QPushButton('Add Question')
        add_button.clicked.connect(self.add_question)
        self.question_list.itemClicked.connect(self.show_photo)
        remove_button = QPushButton('Remove Question')
        remove_button.clicked.connect(self.remove_question)

        load_button = QPushButton('Load Questions')
        load_button.clicked.connect(self.load_questions)

        score_label = QLabel('Score:')
        self.score_display = QLineEdit()
        self.score_display.setReadOnly(True)

        calculate_button = QPushButton('Calculate Score')
        calculate_button.clicked.connect(self.calculate_score)

        # Create the layout
        widget = QWidget()

        layout.addWidget(QLabel('Questions:'))
        layout.addWidget(self.question_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(load_button)
        layout.addLayout(button_layout)

        layout.addWidget(score_label)
        layout.addWidget(self.score_display)

        layout.addWidget(calculate_button)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Load the questions
        self.load_questions()

    def add_question(self):
        password, ok = QInputDialog.getText(self, 'Add Question', 'Enter the password:')
        if ok and hashlib.sha256(password.encode()).hexdigest() == 'db3d01adde1b61d0fe8f4bae9f555304ee515e03580d04ccf478345a7a3bdbbc':
            text, ok = QInputDialog.getText(self, 'Add Question', 'Enter the question text:')
            if ok and text:
                coef, ok = QInputDialog.getDouble(self, 'Add Question', 'Enter the coefficient:')
                if ok:
                    reply = QMessageBox.question(self, 'Add Photo', 'Do you want to add a photo to this question?',
                                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        options = QFileDialog.Options()
                        options |= QFileDialog.DontUseNativeDialog
                        file_name, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.bmp *.gif)", options=options)
                        if file_name:
                            # Copy the photo to the photos folder
                            photo_folder = 'photos'
                            os.makedirs(photo_folder, exist_ok=True)
                            photo_path = os.path.join(photo_folder, os.path.basename(file_name))
                            shutil.copyfile(file_name, photo_path)
                        else:
                            photo_path = None

                    new_question = {'text': text, 'coef': coef, 'score': 0, 'photo': photo_path}
                    self.questions.append(new_question)
                    self.save_questions()
                    self.question_list.addItem(text)

                    QMessageBox.information(self, 'Add Question', 'Question added successfully.')
        else:
            QMessageBox.warning(self, 'Add Question', 'Invalid password.')

    def remove_question(self):
        selected_question = self.question_list.currentItem()
        if selected_question is not None:
            question_index = self.question_list.currentRow()
            del self.questions[question_index]
            self.save_questions()
            self.question_list.takeItem(question_index)

    def load_questions(self):
        self.question_list.clear()
        try:
            with open('questions.json', 'r') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            self.questions = [{'text': 'Question 1', 'coef': 1, 'score': 0},
                            {'text': 'Question 2', 'coef': 1, 'score': 0},
                            {'text': 'Question 3', 'coef': 1, 'score': 0}]
            self.save_questions()
        
        for question in self.questions:
            self.question_list.addItem(question['text'])

    def save_questions(self):
        with open('questions.json', 'w') as f:
            json.dump(self.questions, f)
    def show_photo(self, item):
        selected_question = self.questions[self.question_list.currentRow()]
        photo_path = selected_question.get('photo')
        if photo_path:
            photo_folder = 'photos'
            photo_path = os.path.join(photo_folder, os.path.basename(photo_path))
            pixmap = QPixmap(photo_path)
            self.photo_label.setPixmap(pixmap)
    def calculate_score(self):
        score = 0
        for question in self.questions:
            photo_path = question.get('photo')
            pixmap = QPixmap(photo_path)
            self.photo_label.setPixmap(pixmap)
            reply, ok = QInputDialog.getInt(self, 'Answer Question', question['text'])
            if ok:
                question_score = reply * question['coef']
                question['score'] = question_score
                score += question_score
                


        self.score_display.setText(str(score))

        # Save the questions with the updated scores
        self.save_questions()
app = QApplication(sys.argv)
window = ScoreCalculator()
window.show()
sys.exit(app.exec_())
