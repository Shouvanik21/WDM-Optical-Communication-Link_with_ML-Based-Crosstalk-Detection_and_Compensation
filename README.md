# 📡 Intelligent WDM Optical Communication Link

### ML-Based Crosstalk Detection and Compensation

An intelligent **Wavelength Division Multiplexing (WDM) optical communication system** that simulates multi-channel optical transmission, models fiber impairments and optical crosstalk, calculates communication-quality metrics, detects link conditions using a **Machine Learning model**, and applies signal compensation to improve the received signal.

The project combines **optical communication, digital signal processing, Python-based simulation, Machine Learning, signal analysis, backend development, database storage, and React visualization** into a single end-to-end system.

The main objective is to demonstrate how Machine Learning can be integrated with an optical communication system to automatically identify whether the communication link is operating under **NORMAL, WARNING, or CRITICAL** crosstalk conditions.

---

# 🎯 Project Overview

In a WDM system, multiple optical signals are transmitted simultaneously through the same optical fiber using different wavelengths.

For example:

```text
λ1 ─────────┐
λ2 ─────────┤
λ3 ─────────┼──► WDM MUX ──► Optical Fiber ──► DEMUX ──► Receiver
λ4 ─────────┘
```

Although WDM significantly increases the capacity of an optical fiber, the channels can interfere with each other.

One important impairment is **optical crosstalk**.

Crosstalk occurs when part of the optical signal from one wavelength/channel unintentionally affects another channel.

This project simulates that behavior and builds an intelligent monitoring layer around it.

The complete system follows:

```text
Signal Generation
       ↓
WDM Multiplexing
       ↓
Optical Fiber Transmission
       ↓
Attenuation + Dispersion
       ↓
Crosstalk + Noise
       ↓
Optical Reception
       ↓
Communication Metrics
       ↓
Machine Learning Detection
       ↓
Signal Compensation
       ↓
Performance Comparison
       ↓
Dashboard Visualization
```

---

# 🚀 Features

## 🌈 1. Multi-Channel WDM Simulation

The system simulates multiple optical channels operating at different wavelengths.

The current implementation uses:

```text
Number of Channels : 4
```

Represented conceptually as:

```text
λ1
λ2
λ3
λ4
```

Each channel contains its own digital information.

The signals are independently generated before being combined for transmission.

```text
Channel 1 → Digital Signal
Channel 2 → Digital Signal
Channel 3 → Digital Signal
Channel 4 → Digital Signal
```

The individual signals are then combined into a WDM transmission system.

---

# 📡 2. Digital Signal Generation

The simulation begins by generating binary information for each channel.

Example:

```text
Channel 1:
1 0 1 1 0 0 1 0 ...

Channel 2:
0 1 1 0 1 0 0 1 ...

Channel 3:
1 1 0 0 1 1 0 1 ...

Channel 4:
0 0 1 1 0 1 1 0 ...
```

The binary information is converted into numerical waveforms that can be processed using NumPy.

The number of samples used to represent each bit can be controlled through:

```text
samples_per_bit
```

This allows the simulation to represent the digital signal at a higher resolution than simply storing the original binary sequence.

---

# 🔀 3. WDM Multiplexing

The individual wavelength channels are combined before entering the optical fiber.

Conceptually:

```text
λ1 ───────┐
λ2 ───────┤
λ3 ───────┼──► WDM MUX
λ4 ───────┘
             │
             ▼
      Combined Optical Signal
```

The multiplexer allows multiple channels to share the same fiber.

This represents the basic principle behind **Wavelength Division Multiplexing**, where different wavelengths carry independent information simultaneously.

---

# 🧵 4. Optical Fiber Model

The project includes a software-based optical fiber model.

The fiber introduces physical impairments that affect the transmitted signal.

The main parameters include:

* Fiber length
* Attenuation
* Dispersion

Example simulation parameters:

```text
Fiber Length : 50 km
Attenuation  : 0.2 dB/km
Dispersion   : 17 ps/nm/km
```

These parameters can be modified to experiment with different transmission conditions.

---

# 📉 5. Fiber Attenuation

As an optical signal travels through a fiber, its power decreases.

The simulation models this reduction using fiber attenuation.

For a simplified attenuation calculation:

```text
Fiber Loss = Fiber Length × Attenuation
```

For example:

```text
Fiber Length = 50 km
Attenuation  = 0.2 dB/km

Fiber Loss = 50 × 0.2
           = 10 dB
```

The resulting loss affects the received optical signal.

---

# 🌊 6. Dispersion Modeling

Optical dispersion causes different components of the transmitted signal to spread as they travel through the fiber.

The project includes a dispersion parameter in the simulation to represent this degradation.

Conceptually:

```text
Transmitted Pulse

       │
       ▼

    ████

       │
       │ Fiber
       ▼

   ████████
```

As propagation distance increases, dispersion can cause signal broadening and distortion.

The dispersion value is also included as an input feature for the Machine Learning model.

---

# 🔀 7. Optical Crosstalk Modeling

Crosstalk is one of the primary problems investigated by this project.

In a WDM system, unwanted signal leakage can occur between channels.

For example:

```text
Channel 1 ────────────────►
                   ╲
                    ╲
Channel 2 ──────────╲────► Interference
                      ╲
Channel 3 ────────────╲──►
```

The `crosstalk.py` module models the interference introduced between channels.

The amount of coupling between channels determines how strongly one channel affects another.

A higher coupling level can result in stronger interference.

The simulation calculates crosstalk-related measurements that are later used by the ML model.

---

# 🔊 8. Noise Modeling

Real communication systems are affected by noise.

To make the simulation more realistic, controlled noise is added to the received signal.

The signal therefore becomes:

```text
Received Signal
=
Original Signal
+
Crosstalk
+
Noise
+
Fiber Effects
```

Noise level is also included as one of the features used during Machine Learning prediction.

---

# 📥 9. Optical Receiver

After transmission through the simulated optical link, the receiver processes the degraded signal.

The receiver attempts to recover the original digital information.

The basic process is:

```text
Received Optical Signal
          │
          ▼
      Detection
          │
          ▼
   Recovered Bits
          │
          ▼
 Compare with Original
          │
          ▼
      Bit Errors
```

The recovered data is compared against the original transmitted bits.

This allows the system to calculate the **Bit Error Rate (BER)**.

---

# 📊 10. Communication Metrics

The simulation calculates multiple measurements describing the quality of the optical link.

These measurements are important because the Machine Learning model does not rely on only one parameter.

The current feature set includes:

```text
SNR
Received Power
Noise Level
Fiber Loss
Dispersion
Average Crosstalk
Crosstalk
BER
```

---

## 📈 Signal-to-Noise Ratio

SNR represents the relationship between useful signal power and noise power.

Conceptually:

```text
Higher SNR
    ↓
Better signal quality
```

A lower SNR generally indicates that the signal has become more difficult to recover.

---

## ❌ Bit Error Rate

BER measures how many transmitted bits were incorrectly detected.

The basic relationship is:

```text
BER = Number of Bit Errors / Total Number of Bits
```

For example:

```text
Total Bits  = 1000
Bit Errors  = 50

BER = 50 / 1000
    = 0.05
```

BER is one of the most important indicators of communication quality in the simulation.

---

## 📉 Fiber Loss

Fiber loss represents the reduction in optical power caused by transmission through the fiber.

Example:

```text
Fiber Length = 50 km
Attenuation  = 0.2 dB/km

Loss = 10 dB
```

---

## 🔀 Crosstalk

Crosstalk represents unwanted interference between optical channels.

The system calculates crosstalk-related measurements and represents the result in dB.

A stronger unwanted interference level indicates a more degraded communication environment.

---

## ⚡ Received Power

Received power represents the optical signal power available at the receiver after transmission through the fiber and other simulated impairments.

A reduction in received power can affect the ability of the receiver to correctly recover the transmitted data.

---

# 🤖 Machine Learning Layer

The main intelligence of the project is provided by a **Random Forest Classifier**.

Instead of manually checking individual thresholds for every metric, the ML model receives multiple communication parameters simultaneously.

```text
              ┌───────────────┐
              │      SNR      │
              ├───────────────┤
              │Received Power │
              ├───────────────┤
              │  Noise Level  │
              ├───────────────┤
              │  Fiber Loss   │
              ├───────────────┤
              │   Dispersion  │
              ├───────────────┤
              │Avg Crosstalk  │
              ├───────────────┤
              │   Crosstalk   │
              ├───────────────┤
              │      BER      │
              └───────┬───────┘
                      │
                      ▼
              Random Forest
                 Classifier
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       NORMAL      WARNING     CRITICAL
```

---

# 🧠 ML Classification

The model classifies the optical communication link into three conditions:

| Class      | Meaning                                                      |
| ---------- | ------------------------------------------------------------ |
| `NORMAL`   | Communication link is operating within acceptable conditions |
| `WARNING`  | Communication quality is degrading and requires monitoring   |
| `CRITICAL` | Communication link is experiencing severe degradation        |

The labels are represented internally as:

```text
0 → NORMAL
1 → WARNING
2 → CRITICAL
```

---

# 🌲 Why Random Forest?

A Random Forest classifier is used because it can work effectively with multiple numerical features and can model non-linear relationships between communication parameters.

For example, a link may not become critical because of only one parameter.

Instead, the condition could result from a combination such as:

```text
Lower SNR
      +
Higher Crosstalk
      +
Higher BER
      +
Lower Received Power
      ↓
CRITICAL
```

The Random Forest model learns relationships between these features from the generated dataset.

---

# 📚 Dataset Generation

The project includes a dedicated dataset-generation stage.

The simulator is repeatedly executed with different communication conditions to create training examples.

Conceptually:

```text
Simulation Scenario 1
        ↓
Metrics
        ↓
Label

Simulation Scenario 2
        ↓
Metrics
        ↓
Label

Simulation Scenario 3
        ↓
Metrics
        ↓
Label

        ...

        ↓

wdm_dataset.csv
```

The dataset contains the communication measurements along with their corresponding severity class.

---

# 🗂️ Dataset Features

Each training sample contains parameters similar to:

```text
SNR
Received Power
Noise Level
Fiber Loss
Dispersion
Average Crosstalk
Crosstalk
BER
Severity
```

Example structure:

```text
snr,received_power,noise_level,fiber_loss,
dispersion,average_crosstalk,crosstalk,ber,severity
```

The generated dataset is stored in:

```text
python/wdm_dataset.csv
```

---

# 🏋️ Model Training

The `train_model.py` script loads the generated dataset and trains the Random Forest classifier.

The training pipeline follows:

```text
CSV Dataset
     │
     ▼
Load Data
     │
     ▼
Separate Features and Labels
     │
     ▼
Train/Test Split
     │
     ▼
Random Forest Training
     │
     ▼
Model Evaluation
     │
     ▼
Save Trained Model
```

The trained model is stored as:

```text
wdm_crosstalk_model.pkl
```

This allows the trained model to be reused during simulation without retraining every time.

---

# 🔮 Prediction During Simulation

During a normal simulation run, the system does not need to retrain the model.

Instead:

```text
New Simulation
      │
      ▼
Calculate Metrics
      │
      ▼
Create Feature Vector
      │
      ▼
Load .pkl Model
      │
      ▼
Random Forest Prediction
      │
      ▼
NORMAL / WARNING / CRITICAL
```

This allows the simulation to behave like an intelligent monitoring system.

---

# 📊 Prediction Probabilities

The model also provides class probabilities.

For example:

```text
NORMAL     : 1.82%
WARNING    : 4.34%
CRITICAL   : 93.84%
```

This provides more information than simply displaying the predicted class.

The probability distribution gives an indication of how strongly the model favors each condition.

---

# 🔧 Signal Compensation

After analyzing the received signal, the project applies a compensation process intended to reduce the effects of signal degradation.

The system evaluates the signal before and after compensation.

```text
             Original Signal
                    │
                    ▼
             Optical Channel
                    │
                    ▼
            Fiber Transmission
                    │
                    ▼
             Crosstalk + Noise
                    │
                    ▼
             Received Signal
                    │
                    ▼
              Calculate BER
                    │
                    ▼
              Compensation
                    │
                    ▼
          Compensated Signal
                    │
                    ▼
        Calculate Compensated BER
```

The two BER values can then be compared.

---

# 📉 BER Improvement

The compensation performance can be represented as:

```text
BER Improvement =
Original BER - Compensated BER
```

If:

```text
Original BER       = 0.064
Compensated BER    = 0.040
```

then:

```text
Improvement = 0.064 - 0.040
            = 0.024
```

This provides a quantitative measurement of the effect of compensation.

---

# 🖥️ Web Dashboard

The project includes a React-based monitoring dashboard.

The dashboard provides a visual representation of the optical communication system and its current simulation results.

The interface contains sections for:

* WDM channels
* Optical communication flow
* Communication metrics
* ML detection
* ML probabilities
* Compensation results
* Simulation controls

---

# 🔄 Frontend-to-Python Architecture

The frontend does not directly execute the Python simulation.

Instead, Node.js acts as the bridge.

```text
React
 │
 │ HTTP Request
 ▼
Express Backend
 │
 │ Child Process
 ▼
Python Simulation
 │
 ▼
Simulation Result
 │
 ▼
Express Backend
 │
 ▼
MongoDB
 │
 ▼
React Dashboard
```

This separation keeps the frontend, backend, and simulation logic independent.

---

# ▶️ Run Simulation Flow

When the user clicks **Run Simulation**:

```text
1. User clicks Run Simulation
             │
             ▼
2. React sends POST request
             │
             ▼
3. Express receives request
             │
             ▼
4. Node.js starts Python process
             │
             ▼
5. Python executes simulation
             │
             ▼
6. WDM channels are generated
             │
             ▼
7. Fiber effects are simulated
             │
             ▼
8. Crosstalk and noise are added
             │
             ▼
9. Receiver calculates recovered data
             │
             ▼
10. Metrics are calculated
             │
             ▼
11. ML model predicts severity
             │
             ▼
12. Compensation is performed
             │
             ▼
13. Result is returned to Node.js
             │
             ▼
14. Result is stored in MongoDB
             │
             ▼
15. React displays the result
```

---

# 🔌 Backend API

The Express backend exposes endpoints for controlling and retrieving simulations.

| Method | Endpoint                   | Description                                |
| ------ | -------------------------- | ------------------------------------------ |
| `POST` | `/api/auth/runsimulation`       | Run a new optical communication simulation |
| `GET`  | `/api/auth/getsimulations`      | Retrieve stored simulations                |
| `GET`  | `/api/auth/getlatestsimulation` | Retrieve the latest simulation             |

---

# 📡 Simulation API Request

The frontend starts a simulation using:

```http
POST /api/auth/runsimulation
```

The backend then launches the Python simulation process.

The Python output is parsed by the Node.js service and converted into structured data.

---

# 🗄️ MongoDB Storage

MongoDB is used to store simulation results.

A stored simulation can contain:

```text
SNR
Crosstalk
BER
Fiber Loss
Dispersion
Received Power
Bit Errors
Average Crosstalk
ML Prediction
ML Probabilities
Compensated BER
Timestamp
```

This makes it possible to retrieve previous simulation results rather than only displaying the current run.

---

# 📁 Project Structure

```text
WDM-Optical-Communication-Link/
│
├── client/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CompensationCard.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── InfoSection.jsx
│   │   │   ├── MLDetection.jsx
│   │   │   ├── OpticalFlow.jsx
│   │   │   └── ResultCard.jsx
│   │   │
│   │   ├── pages/
│   │   │   └── Dashboard.jsx
│   │   │
│   │   ├── App.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── .env
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
│
├── python/
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── analyze_dataset.py
│   │   ├── dataset_generator.py
│   │   ├── train_model.py
│   │   ├── wdm_crosstalk_model.pkl
│   │   └── wdm_dataset.csv
│   │
│   ├── simulation/
│   │   ├── __init__.py
│   │   ├── crosstalk.py
│   │   ├── fiber.py
│   │   ├── metrics.py
│   │   ├── receiver.py
│   │   ├── signal_generator.py
│   │   ├── simulation.py
│   │   └── wdm_system.py
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── visualization.py
│   │
│   ├── main.py
│   ├── python_api.py
│   └── requirements.txt
│
├── server/
│   ├── config/
│   │   └── db.js
│   │
│   ├── controllers/
│   │   └── simulationController.js
│   │
│   ├── models/
│   │   └── Simulation.js
│   │
│   ├── routes/
│   │   └── simulationRoutes.js
│   │
│   ├── services/
│   │   └── simulationService.js
│   │
│   ├── .env
│   ├── .gitignore
│   ├── package-lock.json
│   ├── package.json
│   └── server.js
│
├── .gitignore
└── README.md
```

---

# 🧩 Python Module Responsibilities

The Python simulation is intentionally divided into multiple modules.

### `simulation.py`

Acts as the main simulation entry point.

It coordinates the complete simulation process.

---

### `wdm_system.py`

Handles the overall WDM system and coordinates the optical communication channels.

---

### `signal_generator.py`

Generates the digital information and corresponding signal waveforms.

---

### `fiber.py`

Models optical fiber transmission effects such as:

* Attenuation
* Dispersion
* Signal loss

---

### `crosstalk.py`

Models optical interference between WDM channels.

---

### `receiver.py`

Processes the received signal and performs signal/bit detection.

---

### `metrics.py`

Calculates communication-quality parameters such as:

* BER
* SNR
* Fiber loss
* Crosstalk
* Received power

---

### `dataset_generator.py`

Generates simulation samples for Machine Learning.

---

### `train_model.py`

Trains the Random Forest classifier using the generated dataset.

---

### `visualization.py`

Runs the simulation and visualizes signal behavior and compensation results.

---

# 🔄 Complete System Architecture

```text
                    ┌───────────────────────┐
                    │    React Dashboard    │
                    └───────────┬───────────┘
                                │
                                │ REST API
                                ▼
                    ┌───────────────────────┐
                    │    Node.js / Express  │
                    └───────────┬───────────┘
                                │
                         Start Python
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Python Simulation   │
                    └───────────┬───────────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
      Signal Generator      Fiber Model      Crosstalk Model
             │                  │                  │
             └──────────────────┼──────────────────┘
                                │
                                ▼
                       Optical Receiver
                                │
                                ▼
                       Metrics Calculation
                                │
                                ▼
                      Machine Learning Model
                                │
                                ▼
                       Severity Prediction
                                │
                         ┌──────┴──────┐
                         │             │
                         ▼             ▼
                    Detection     Compensation
                         │             │
                         └──────┬──────┘
                                │
                                ▼
                       Simulation Result
                                │
                                ▼
                           MongoDB
                                │
                                ▼
                       React Dashboard
```

---

# 🛠️ Tech Stack

## Frontend

* **React.js**
* **Vite**
* **Tailwind CSS**
* **JavaScript**

## Backend

* **Node.js**
* **Express.js**
* **REST APIs**

## Database

* **MongoDB**
* **Mongoose**
* **MongoDB Atlas**

## Simulation

* **Python**
* **NumPy**

## Data Processing

* **Pandas**
* **NumPy**

## Machine Learning

* **Scikit-learn**
* **Random Forest Classifier**

## Machine Learning Deployment

* **Joblib**

## Visualization

* **Matplotlib**

## Development Tools

* **VS Code**
* **Git**
* **GitHub**
* **Thunder Client / Postman**

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/WDM-Optical-Communication-Link_with_ML-Based-Crosstalk-Detection_and_Compensation.git
```

---

## 2. Navigate into the project

```bash
cd WDM-Optical-Communication-Link_with_ML-Based-Crosstalk-Detection_and_Compensation
```

---

## 3. Install backend dependencies

```bash
cd server
npm install
```

Return to the root:

```bash
cd ..
```

---

## 4. Install frontend dependencies

```bash
cd client
npm install
```

Return to the root:

```bash
cd ..
```

---

## 5. Install Python dependencies

```bash
cd python
```

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

Return to the root:

```bash
cd ..
```

---

# 🗄️ MongoDB Configuration

Create a MongoDB database or use MongoDB Atlas.

Add your connection string to `.env`:

```env
MONGO_URI="YOUR_MONGODB_CONNECTION_STRING"
PORT=5000
```

Do not commit `.env` to GitHub.

---

# ▶️ Running the Project

## Start the backend

From the project root:

```bash
node server.js
```

The backend will run at:

```text
http://localhost:5000
```

---

## Start the frontend

Open another terminal:

```bash
cd client
npm run dev
```

Open the local URL provided by Vite.

---

# 🧪 Running the Python Simulation

The Python simulation can also be executed independently.

```bash
cd python
python simulation.py
```

This allows the optical communication system to be tested without the React dashboard.

---

# 📚 Machine Learning Workflow

The ML workflow can be performed in three main stages.

## Step 1 — Generate Dataset

From the root first do this :
 ```
 cd python
 ```

 Then:

```bash
python ml/dataset_generator.py
```

This creates:

```text
wdm_dataset.csv
```

---

## Step 2 — Train Model

From the root first do this :
 ```
 cd python
 ```

 Then:

```bash
python ml/train_model.py
```

This trains the Random Forest classifier and creates:

```text
wdm_crosstalk_model.pkl
```

---

## Step 3 — Run Prediction

The trained model is loaded by the simulation:

```text
New Simulation
      ↓
Communication Metrics
      ↓
Feature Vector
      ↓
Trained Random Forest
      ↓
Severity Prediction
```

---

# 🧪 Example Simulation Output

A simulation run can produce results such as:

```text
========== SIMULATION OUTPUT ==========

SNR             : 11.07 dB
Crosstalk       : -6.13 dB
BER             : 0.0640
Fiber Loss      : 10.00 dB

========== ML DETECTION ==========

Prediction      : CRITICAL

NORMAL          : 1.82%
WARNING         : 4.34%
CRITICAL        : 93.84%
```

The exact values depend on the randomly generated signal and simulation parameters.

---

# 📈 Example Processing Pipeline

A single simulation can be represented as:

```text
4 WDM Channels
      │
      ▼
Digital Bit Generation
      │
      ▼
Waveform Generation
      │
      ▼
WDM Multiplexing
      │
      ▼
50 km Optical Fiber
      │
      ├── Attenuation
      ├── Dispersion
      └── Signal Loss
      │
      ▼
Crosstalk Injection
      │
      ▼
Noise Addition
      │
      ▼
Optical Receiver
      │
      ▼
Bit Detection
      │
      ▼
BER / SNR / Crosstalk
      │
      ▼
Feature Vector
      │
      ▼
Random Forest
      │
      ▼
Severity Classification
      │
      ▼
Compensation
      │
      ▼
BER Comparison
```

---

# 📚 What I Learned

This project provided hands-on experience across both **engineering simulation and Artificial Intelligence**.

### Optical Communication

* Understanding WDM systems
* Understanding wavelength-based multiplexing
* Understanding optical channel interference
* Understanding optical fiber transmission
* Understanding attenuation
* Understanding dispersion
* Understanding crosstalk
* Understanding optical receivers
* Understanding communication-system performance metrics

### Python

* Building modular Python applications
* Working with NumPy arrays
* Generating digital signals
* Performing numerical calculations
* Structuring simulation modules
* Working with CSV datasets
* Running repeated simulations

### Signal Processing

* Digital waveform generation
* Signal degradation
* Noise modeling
* Crosstalk modeling
* Signal detection
* BER calculation
* Signal comparison
* Signal compensation

### Machine Learning

* Dataset generation
* Feature engineering
* Preparing training data
* Train/test splitting
* Random Forest classification
* Multi-class classification
* Model evaluation
* Saving trained models
* Loading trained models
* Probability-based prediction

### Data Science

* Working with Pandas
* Creating structured datasets
* Analyzing simulation parameters
* Understanding relationships between features
* Visualizing simulation data

### Full-Stack Development

* Building REST APIs
* Connecting React with Express
* Executing Python from Node.js
* Passing simulation results between applications
* Storing results in MongoDB
* Building an interactive monitoring dashboard

---

# 🎓 Engineering + AI Integration

The main learning outcome of this project is understanding how an engineering system can be combined with Machine Learning.

Traditional simulation:

```text
Input
  ↓
Physical Model
  ↓
Output
```

This project extends that concept:

```text
Input
  ↓
Optical Communication Simulation
  ↓
Measurements
  ↓
Machine Learning
  ↓
Fault/Severity Detection
  ↓
Compensation
  ↓
Performance Evaluation
```

Therefore, the project is not simply an ML classification project.

It demonstrates an **AI-assisted optical communication monitoring system**.

---

# 📌 Project Purpose

The purpose of this project is to demonstrate an intelligent approach to monitoring a WDM optical communication link.

The system combines:

```text
Optical Communication
        +
Signal Processing
        +
Simulation
        +
Machine Learning
        +
Backend Development
        +
Database
        +
Frontend Visualization
```

The final system can simulate an optical link, measure its communication quality, identify the severity of degradation, and evaluate the effect of compensation.

---

# 📄 License

This project is intended for **learning, research, experimentation, and educational purposes**.