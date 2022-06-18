# Dogs_Breed_Prediction_WebApp
Flask Dog Breed Prediction Web App : [Link to Website](https://dogs-breed.herokuapp.com/)

# About Model
This model is developed using `Keras` with `Tensorflow 2` as the backend for `Keras`. The model consists of the `120` dog classes and is based on the `MobileNet` model. This `keras` model is a fine-tuned version of the `MobileNet` model. `MobileNet` models are small and is used fro deploying in web servers. This keras model has an accuracy rate of around `80 %` on the test set consisting of `2400` Images (20 from each class) from Stanford Dog Dataset.

# About Dataset 
The dataset was taken from [Stanford Dogs Dataset!](http://vision.stanford.edu/aditya86/ImageNetDogs/main.html). Standford Dogs Dataset consists of a photo of 120 different dogs breed. There are roughly 53000 images of dogs in this dataset. As the research suggests the state of the art accuracy for this dataset is `89%`. [Reference Link](https://www.researchgate.net/publication/325384896_Modified_Deep_Neural_Networks_for_Dog_Breeds_Identification) 
