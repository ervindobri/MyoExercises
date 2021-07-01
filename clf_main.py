from services.classify import ClassifyExercises
from constants.variables import PREDEFINED_EXERCISES

if __name__ == '__main__':
    # Exercises:
    # 1. tip toe standing
    # 2. toe crunches
    # 3. toe stand - TOO similar to toe crunches
    # 4. toes UP
    # 5. rest
    # MyoService.restart_process()
    # time.sleep(1)
    # change_sample_size(100)

    dummy = ClassifyExercises(
        subject="Ervin",
        age=22,
        exercises=PREDEFINED_EXERCISES,
        batch_size=25,
        training_batch_size=16
    )

    # dummy.PrepareTrainingData()
    # dummy.TrainEMG()
    # dummy.DisplayResults()
    # dummy.PredictGestures()

    # indexes: 0 - TT,
    #          1 - TC,
    #          2 - UP,
    #          3 - R
    dummy.TestPredict(50, 1)
    # dummy.PredictAndPlay()