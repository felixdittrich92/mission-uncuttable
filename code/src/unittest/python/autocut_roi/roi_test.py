import  cv2

def main():
	x1 = 0 #the values of the coordinates
	x2 = 0
	y1 = 0
	y2 = 0

    cap = cv2.VideoCapture("...") #path to the video

    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
 
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
 
            cv2.imshow('Frame',frame[y1:y2,x1:x2)
 
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else: 
            break
 
    cap.release()
    cv2.destroyAllWindows()
  
if __name__== "__main__":
    main()