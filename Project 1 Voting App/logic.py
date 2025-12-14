
#allows for comma separated values in the csv file
import csv
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from gui import Ui_MainWindow

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connection to the submit button
        self.btn_submit.clicked.connect(self.handle_submit)
        # Hides the pop-up label for errors or status of submission.
        self.Popup_label.setVisible(False)
        #ID needs to meet the 4 digit requirement
        self.ID_box.setMaxLength(4)
        #checking to see if the csv exists
        self.csv_voting()


    def csv_voting(self):
        """
        Create the votes.csv file if it doesn't exist already, stops the program for errors
        """
        #creates votes.csv to store the votes
        try:
            with open('votes.csv', 'x', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['voter_id', 'candidate'])
        #handles the errors internally
        except FileExistsError:
            pass
        except FileNotFoundError:
            self.show_message('Failed')
            QMessageBox.critical(self, 'Error', 'Could not create votes.csv.')


    def handle_submit(self):
        """
        Get the vote id from ID_box
        ensure ID is using validate_id()
        candidate needs to be selected on the radio button.
        ID gets only one vote per ID
        Save the vote to CSV or text file.
        show status of submission
        reset the radio button and ID
        """
        #Grabs voter 4 digit ID
        voter_id = self.ID_box.text().strip()
        #Validates ID
        if not self.validate_id(voter_id):
            return
        #Grabs candidate
        candidate = self.get_selected_candidate()
        #Prompts QMessageBox and shows on bottom 'Failed'
        if candidate is None:
            self.show_message('Failed')
            QMessageBox.critical(self, 'Error', 'Select a candidate.')
            self.Popup_label.setVisible(False)
            return
        #Checking for ID submission
        if self.double_vote(voter_id):
            self.show_message('Failed')
            QMessageBox.critical(self, 'Error', 'You cannot vote twice.')
            self.Popup_label.setVisible(False)
            return
        #saves the correct (only one) vote entry
        if not self.save_vote(voter_id, candidate):
            return
        #Shows success only if no double vote, no errors, candidate is selected
        self.show_message('Success')
        QMessageBox.information(self, 'Success', f'You voted successfully for candidate: {candidate}.')
        #resets the process
        self.reset_form()


    def validate_id(self, voter_id):
        """
        validates the voter ID.
        if statement for to ensure radio button is checked, return True
        ID needs to be 4 digits (int only)
        returns True/False
        """
        #Fails if not a 4 digit input
        if len(voter_id) != 4:
            self.show_message('Failed')
            QMessageBox.critical(self, 'Error', 'ID must be a 4 digit voter ID.')
            self.Popup_label.setVisible(False)
            return False
        #Checks ID input is integer
        try:
            int(voter_id)
        except ValueError:
            self.show_message("Failed")
            QMessageBox.critical(self, "Error", "ID must contain numbers only.")
            self.Popup_label.setVisible(False)
            return False
        # True means the ID is valid with these parameters 4 digits,
        # and only numbers was in the input
        return True


    def get_selected_candidate(self):
        """
        returns the selected candidate's name.
        """
        #returns Jane if clicked
        if self.rdo_jane.isChecked():
            return 'Jane'
        #returns john if clicked
        if self.rdo_john.isChecked():
            return 'John'
        return None


    def double_vote(self, voter_id):
        """
        checks to see if voter ID already exists in your CSV or text file.
        """
        #reads csv for voter if already written to it
        with open('votes.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('voter_id') == voter_id:
                    return True
        return False


    def save_vote(self, voter_id, candidate):
        """
        Save the vote to a CSV file.
        """
        #saves vote to csv file
        with open('votes.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([voter_id, candidate])
        return True

    def show_message(self, message):
        """
        Shows the message connected to the pop-up label
        """
        #shows the message below for success green and will show red otherwise
        # the other functions does the showing of failed
        self.Popup_label.setVisible(True)
        self.Popup_label.setText(message)
        if message == 'Success':
            self.Popup_label.setStyleSheet('color: green;')
        else:
            self.Popup_label.setStyleSheet('color: red;')

    def reset_form(self):
        """
        Reset the form after a successful vote.
        """
        #clears the id box
        self.ID_box.clear()
        #clears the radio buttons
        self.rdo_jane.setAutoExclusive(False)
        self.rdo_john.setAutoExclusive(False)
        self.rdo_jane.setChecked(False)
        self.rdo_john.setChecked(False)
        self.rdo_jane.setAutoExclusive(True)
        self.rdo_john.setAutoExclusive(True)
        self.Popup_label.setVisible(False)
