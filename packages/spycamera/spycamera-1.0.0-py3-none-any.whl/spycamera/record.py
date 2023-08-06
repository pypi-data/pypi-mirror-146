import cv2

def webcam(duration_in_seconds, filepath_with_filename, feedback=False):
    if isinstance(duration_in_seconds, int):
        capture = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        videoWriter = cv2.VideoWriter(f'{filepath_with_filename}', fourcc, 30.0, (640, 480))
        current = 0
        limit = 30*duration_in_seconds # bei duration 50 ca. 50 seconds

        while(True):

            ret, frame = capture.read()

            if ret:
                videoWriter.write(frame)

            if current == limit:
                break
            else:
                current += 1
                if feedback == True:
                    print(current)

        capture.release()
        videoWriter.release()

        cv2.destroyAllWindows()
    else:
        print("Pls enter a full number")