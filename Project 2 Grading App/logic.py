
#allows for comma separated values in the csv file
import csv
#imports
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from gui import Ui_MainWindow

#class Logic
class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connection to the submit button
        self.btn_submit.clicked.connect(self.handle_submit)
        #pop up label is not visible at start
        self.popup_label.setVisible(False)
        #checking if csv file exists
        self.csv_grading()
        #list for score input boxes
        self.score_boxes = [
            self.box_s1,
            self.box_s2,
            self.box_s3,
            self.box_s4,
        ]
        #list for the score labels
        self.score_labels = [
            self.score_1,
            self.score_2,
            self.score_3,
            self.score_4,
        ]
        #the controller that decides if the score boxes appear
        self.box_attempts.textChanged.connect(self.update_score_boxes)
        # at the start no boxes and labels are visible
        self.set_visible_scores(0)

    def csv_grading(self):
        """
        Create the CSV grading file with the labels above for validation on the csv file
        """
        #creating the csv files with the correct labeling for the entries
        try:
            with open('grades.csv', 'x', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'student_name',
                    'attempts',
                    'score1',
                    'score2',
                    'score3',
                    'score4',
                    'highest_score'
                ])
        # if exists it will ignore this part of code
        except FileExistsError:
            pass
        # if the file catches an exception like cannot be created, it will show this error
        except Exception:
            self.show_message('Failed')
            QMessageBox.critical(self, 'Error', 'Could not create grades.csv.')

    def update_score_boxes(self):
        """
        Show/hide score boxes based on attempts (1–4).
        """
        text = self.box_attempts.text().strip()
        #if the text has nothing in there is going to be nothing that shows
        if text == "":
            self.set_visible_scores(0)
            return
        #lables attempts for the input
        try:
            attempts = int(text)
        #exception if value errors show 0
        except ValueError:
            self.set_visible_scores(0)
            return
        # determines if input is less than 0 = 0, 4 = 4
        if attempts < 0:
            attempts = 0
        elif attempts > 4:
            attempts = 4
        #will set the visible to what the input is input = attempts
        self.set_visible_scores(attempts)

    def set_visible_scores(self, attempts):
        """
        Set the visible/not visible scores labels and boxes
        """
        #Finds 1-4 range of the inputs and applies score_box and score_labels visible to them
        for i in range(4):
            visible = i < attempts
            self.score_boxes[i].setVisible(visible)
            self.score_labels[i].setVisible(visible)
            #if not in range it will clear
            if not visible:
                self.score_boxes[i].clear()

    def handle_submit(self):
        """
        validates inputs for submission, calculates the amount of scores,
        ensures there is no errors, handles exceptions, handles the final successful submissions
        """
        #calls on get_raw_inputs and grabs the string names
        name, attempts_text, scores_texts = self.get_raw_inputs()
        #validating name,
        if not self.validate_name(name):
            return
        #validating attempts_text (1-4)
        attempts = self.validate_attempts(attempts_text)
        if attempts is None:
            return
        #only visible score boxes are used
        visible_scores_texts = scores_texts[:attempts]
        #Allows scores to return errors or 0's and if scores is none
        #than return the highest(max) score
        scores = self.convert_scores(visible_scores_texts)
        if scores is None:
            return
        highest = max(scores)
        #saves the scores, any attempts are recorded as 0's since we are finding the highest score
        all_scores_4 = self.convert_scores(scores_texts)
        if all_scores_4 is None:
            # should not happen, but prevents crashing
            all_scores_4 = [0, 0, 0, 0]
        try:
            with open("grades.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    name,
                    attempts,
                    all_scores_4[0],
                    all_scores_4[1],
                    all_scores_4[2],
                    all_scores_4[3],
                    highest
                ])
        except Exception:
            self.show_message("Failed")
            QMessageBox.critical(self, "Error", "Could not save to grades.csv.")
            return
        self.show_message("Success")
        QMessageBox.information(
            self,
            "Final Result",
            f"Highest score: {highest}\nScores used: {scores}"
        )
        self.clear_inputs()

    def get_raw_inputs(self):
        """
        Read raw text from the input fields and renames them
        """
        name = self.box_student.text().strip()
        attempts_text = self.box_attempts.text().strip()
        scores_texts = [
            self.box_s1.text().strip(),
            self.box_s2.text().strip(),
            self.box_s3.text().strip(),
            self.box_s4.text().strip(),
        ]
        return name, attempts_text, scores_texts

    def validate_name(self, name):
        """
        validates name field for any letter name has to at least have 1 character
        """
        if name == "":
            self.show_message("Failed")
            QMessageBox.critical(self, "Error", "Need a name for record keeping.")
            return False
        return True

    def validate_attempts(self, attempts_text):
        """
        Validate the number of attempts (must be 1 to 4).
        cannot be empty or error, as to be a integer
        """
        if attempts_text == "":
            self.show_message("Failed")
            QMessageBox.critical(self, "Error", "Enter a No. of Attempts.")
            return None
        attempts = int(attempts_text)
        if attempts < 1 or attempts > 4:
            self.show_message("Failed")
            QMessageBox.critical(self, "Error", "No. of Attempts must be between 1 and 4.")
            return None

        return attempts

    def convert_scores(self, scores_texts):
        """
        Convert score texts to numbers.
        Blank = 0. Non-blank must be numeric and 0-100.
        """
        #stores the scores in a list
        scores = []
        #checks text of the scores 1 - 4
        #text with nothing treated as 0
        for i, text in enumerate(scores_texts, start=1):
            if text == "":
                scores.append(0)
                continue
            #validates that the score must be a number and allows for floats to be used in the grading app
            try:
                #changes text to float = value
                value = float(text)
            except ValueError:
                self.show_message("Failed")
                QMessageBox.critical(self, "Error", "Score must be a number.")
                return None
            #checks the value between 0-100
            if value < 0 or value > 100:
                self.show_message("Failed")
                QMessageBox.critical(self, "Error", "Score must be between 0 - 100.")
                return None
            #adds value to list
            scores.append(value)
        #grabs the final list
        return scores

    def clear_inputs(self):
        """
        Clear all inputs at the end of the program so another submission can occur.
        """
        #clears student box
        self.box_student.clear()
        #clears attempts box
        self.box_attempts.clear()
        #clears box in score_boxes list
        for box in self.score_boxes:
            box.clear()
        #visible off
        self.popup_label.setVisible(False)
        #clear text
        self.popup_label.setText("")
        # back to hidden until attempts entered again
        self.set_visible_scores(0)

    def show_message(self, message):
        """
        Shows the message and the color of success or failure related to the popup label
        """
        # shows the message below for success green and will show red otherwise
        # the other functions does the showing of failed
        self.popup_label.setVisible(True)
        self.popup_label.setText(message)
        if message == "Success":
            self.popup_label.setStyleSheet("color: green;")
        else:
            self.popup_label.setStyleSheet("color: red;")