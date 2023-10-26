# Vehicle License Plate Recognition App

This full-stack application is designed for real-time vehicle license plate recognition, tracking, and data logging. It processes video streams, detects license plates, tracks vehicles, and logs the relevant data into a MongoDB database. The results can be viewed in the frontend interface.

## Tech Stack

- **Frontend**: Angular
- **Backend**: Flask API
- **AI**:
  - Object Tracking
  - Custom YOLO trained model
  - YOLO Tracking
  - Optical Character Recognition (OCR) using EasyOCR
  - License Plate Alignment
- **Database**: MongoDB Atlas

## Features

- Real-time vehicle license plate recognition.
- Object tracking to monitor and track vehicles.
- Custom-trained YOLO model for license plate detection.
- YOLO-based vehicle tracking.
- Optical Character Recognition (OCR) for extracting license plate text.
- License plate alignment to improve accuracy.
- Data logging into a MongoDB database.
- User-friendly Angular frontend to access and visualize results.

## Demo

[![Demo](https://github.com/tushar-max/CarLicensePlateRecognition/assets/67724196/f9c8769c-c1d7-4151-9baf-4490d99cb34e)](https://github.com/tushar-max/CarLicensePlateRecognition/raw/main/DemoVideoWorkingPrototype.mp4)

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/tushar-max/CarLicensePlateRecognition.git
   ```
2. Install the necessary dependencies for the frontend and backend.

  ```bash
   cd VNPR_UI
  npm install
   ```
  ```bash
  cd VNPR_Backend
  pip install -r requirements.txt
  ```
3. Run the application:
   ```bash
   #Frontend
   cd VNPR_UI
   ng serve
   #Backend
   cd VNPR_Backend
   python app.py
   ```
4. Access the app in your browser at `http://localhost:4200`.

## Contact

- Tushar Awasthi
- Email: [tusharawasthi722@gmail.com](mailto:tusharawasthi722@gmail.com)
- LinkedIn: [Tushar Awasthi](https://www.linkedin.com/in/tushar-awasthi)
- Twitter: [@awasthi_tusharr](https://twitter.com/awasthi_tusharr)
