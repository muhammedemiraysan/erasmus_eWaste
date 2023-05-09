import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QInputDialog, QPushButton, QVBoxLayout, QWidget, QListWidget, QHBoxLayout


class ScoreCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Score Calculator')
        self.setGeometry(100, 100, 400, 300)

        # Create the widgets
        self.question_list = QListWidget()
        self.question_list.setMaximumWidth(200)
        self.question_list.setMinimumHeight(150)

        add_button = QPushButton('Add Question')
        add_button.clicked.connect(self.add_question)

        remove_button = QPushButton('Remove Question')
        remove_button.clicked.connect(self.remove_question)

        score_label = QLabel('Score:')
        self.score_display = QLineEdit()
        self.score_display.setReadOnly(True)

        calculate_button = QPushButton('Calculate Score')
        calculate_button.clicked.connect(self.calculate_score)

        # Create the layout
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Questions:'))
        layout.addWidget(self.question_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        layout.addLayout(button_layout)

        layout.addWidget(score_label)
        layout.addWidget(self.score_display)

        layout.addWidget(calculate_button)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Load the questions
        self.load_questions()

    def add_question(self):
        text, ok = QInputDialog.getText(self, 'Add Question', 'Enter the question text:')
        if ok and text:
            coef, ok = QInputDialog.getDouble(self, 'Add Question', 'Enter the coefficient:')
            if ok:
                new_question = {'text': text, 'coef': coef, 'score': 0}
                self.questions.append(new_question)
                self.save_questions()
                self.question_list.addItem(text)

    def remove_question(self):
        selected_question = self.question_list.currentItem()
        if selected_question is not None:
            question_index = self.question_list.currentRow()
            del self.questions[question_index]
            self.save_questions()
            self.question_list.takeItem(question_index)

    def load_questions(self):
        try:
            with open('questions.json', 'r') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            self.questions = [{'text': 'Question 1', 'coef': 1, 'score': 0},
                              {'text': 'Question 2', 'coef': 1, 'score': 0},
                              {'text': 'Question 3', 'coef': 1, 'score': 0}]
            self.save_questions()

        for question in self.questions:
            self.question_list.addItem(f"{question['text']} ({question['score']})")

    def save_questions(self):
        with open('questions.json', 'w') as f:
            json.dump(self.questions, f)

    def calculate_score(self):
        total_score = 0
        for question in self.questions:
            score, ok = QInputDialog.getDouble(self, question['text'], 'Enter the score:')
            if ok:
                question['score'] = score
                self.question_list.item(self.questions.index(question)).setText(f"{question['text']} ({question['score']})")
                total_score += question['coef'] * question['score']
        self.score_display.setText(str(total_score))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScoreCalculator()
    ex.show()
    sys.exit(app.exec_())
