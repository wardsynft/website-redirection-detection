# ML Based Website Redirection Detection

This repository contains the code used to generate models and data for my final year thesis project. Please note that some files have been uploaded after parameter tuning and testing, and thus do not reflect the reports made in the thesis. A decription of each file can be seen below:

### Text Classifiers.ipynb
This notebook was used to build and tune the SVM, KNN, and naive Bayes models using text components.

### Image Classifiers.ipynb
This notebook was used to build the CNN model on the image dataset

### Web Crawler.py
This file was used to retrieve URLs from the WayBack Machine. This file was developed in collaboration with another student.

### follow_urls.py
This script creates a link_follower instance which is used to retrieve text and image contents of redirections. A list of URLs are used as input, where all href elements are accessed and saved into a .csv file.

### link_follow.py
Instance created by follow_urls.py. Core component of the web-scraping script.

### translator.py
Translates a string of text input.

### Website Redirection Detection.pdf
The final report produced for this project.