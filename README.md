# AirControl
Device that integrates air gestures to macOS commands for increased productivity and laptop interaction. Uses sensor data, arduino, and sklearn.

# Intro
The challenge was a weekend build project to learn machine learning and develope a cool human machine interaction (HMI) device. The idea was to use cheap IR sensors to recognize various hand gestures for increase work automation. Here is a preview of two gestures of the 4 programmed. They also can be programmed to different automation tasks such as music control, slide control on presentation, typing assist, or tablet application control.

![Working Gif] (https://github.com/mshah0686/AirControl/blob/master/Documentation/ezgif.com-video-to-gif.gif)

# Hardware
The prototype was three IR sensors hooked up to an Arduino that transmitted the resistance data read from the three sensors:

![Hardward](https://github.com/mshah0686/AirControl/blob/master/Documentation/Wiring.jpg)

# Software
Training was done with feature extracted from the three signal inputs. First trianing was done with several gestures and the different signals depicting the gestures are shown here:

Swipe left Gesture Signal:
![Swipe Left] (https://github.com/mshah0686/AirControl/blob/master/Documentation/Swipe%20Left.png)

Swipe Right Gesture Signal
![Swipe Right] (https://github.com/mshah0686/AirControl/blob/master/Documentation/Swipe%20Right.png)

The other signals are stored as CSV files in the TrainingData folder as well.

Training was done using `sklearn` RandomForrestClassifier with a One versus all set up. I also tested SVM, but found a lot more glitches and false positives.

# Furtherwork
I want to develope a full application maybe on swift or python based that let's you select different modes for operation (like mentioned above). I also want to try more gestures but I am limited because the hardware values are not always consistent so the model has a hard time training to such variations.
