import sys
import unittest

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from services.classify import ClassifyExercises
from constants.variables import number_of_samples, PREDEFINED_EXERCISES
from ui.tabs.tab_train import TrainWidget

app = QApplication(sys.argv)


class TrainWidgetTest(unittest.TestCase):
    """Test the tab one, train tab on the GUI"""

    def setUp(self):
        """Create the GUI"""
        self.widget = TrainWidget()
        self.widget.classifyExercises = ClassifyExercises(
            nr_of_samples=number_of_samples,
            epochs=300,
            exercises=PREDEFINED_EXERCISES,
            training_batch_size=16
        )

    def test_defaults(self):
        """Test the GUI in its default state"""
        self.assertEqual(self.widget.ui.subjectEdit.text(), "")
        self.assertEqual(self.widget.ui.nrOfExercises.value(), 2)
        self.assertEqual(self.widget.ui.checkRecording.isChecked(), False)
        self.assertEqual(self.widget.ui.calibrateButton.text(), "Calibrate new model")
        self.assertEqual(self.widget.ui.epochSlider.sliderPosition(), 6)
        self.assertEqual(self.widget.ui.subjectButton.text(), "New")
        self.assertEqual(self.widget.ui.batchSizeMenu.currentText(), '16')
        self.assertEqual(self.widget.ui.trainButton.text(), "Train Model")

    def test_nr_of_exercises(self):
        """ Testing QSpinBox min-max """
        self.assertEqual(self.widget.ui.nrOfExercises.maximum(), 6)
        self.assertEqual(self.widget.ui.nrOfExercises.minimum(), 2)

    def test_buttons(self):
        """ Testing every button """
        subjectButton = self.widget.ui.subjectButton
        QTest.mouseClick(subjectButton, Qt.MouseButtons.LeftButton)
        # trainButton = self.widget.ui.trainButton
        # QTest.mouseClick(trainButton, Qt.MouseButtons.LeftButton)
        calibrateButton = self.widget.ui.calibrateButton
        QTest.mouseClick(calibrateButton, Qt.MouseButtons.LeftButton)
        resultButton = self.widget.ui.resultButton
        QTest.mouseClick(resultButton, Qt.MouseButtons.LeftButton)

    def test_new_subject(self):
        """ Test entering a new subject and pressing the 'New' button """
        self.widget.ui.subjectEdit.setText("Jozsi4")
        subjectButton = self.widget.ui.subjectButton
        QTest.mouseClick(subjectButton, Qt.MouseButtons.LeftButton)

        # Check if subject contains at least a letter
        self.assertEqual(any(c.isalpha() for c in self.widget.subject), True)

    def test_batch_size_menu(self):
        """ Test dropdown menu_bar items """
        allItems = [self.widget.ui.batchSizeMenu.itemText(i) for i in range(self.widget.ui.batchSizeMenu.count())]
        self.assertEqual(allItems, ['2', '4', '8', '16', '32', '64', '128'])

    def test_epoch_slider(self):
        """ Test max, minimum, steps """
        self.assertEqual(self.widget.ui.epochSlider.minimum(), 2)
        self.assertEqual(self.widget.ui.epochSlider.maximum(), 10)
        self.assertEqual(self.widget.ui.epochSlider.tickInterval(), 1)

    def test_subject_list(self):
        """ Test subject list every item containing at least a letter"""
        self.assertEqual(all(self.widget.ui.listFiles.item(c).text().isalpha()
                             for c in range(0, self.widget.ui.listFiles.count())), True)

    def test_calibrate_process(self):
        """ Testing the process of opening the calibration wizard """
        QTest.mouseClick(self.widget.ui.listFiles.viewport(), Qt.MouseButtons.LeftButton)
        firstListItem = self.widget.ui.listFiles.item(0)
        self.assertEqual(firstListItem.isSelected(), True)
        calibrateButton = self.widget.ui.calibrateButton
        QTest.mouseClick(calibrateButton, Qt.MouseButtons.LeftButton)
        self.assertEqual(self.widget.ui.wizard.isVisible(), True)


if __name__ == "__main__":
    unittest.main()
