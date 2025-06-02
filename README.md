# 🎙️ AuroraDuke Accent Detector
![Ekran görüntüsü 2025-06-02 170128](https://github.com/user-attachments/assets/ae7f671e-7b55-4350-8f64-13500120e483)
![Ekran görüntüsü 2025-06-02 170147](https://github.com/user-attachments/assets/8f8d5a64-3d20-4afc-ae4e-0d66d9bf57cc)
![Ekran görüntüsü 2025-06-02 170217](https://github.com/user-attachments/assets/42dc32a5-9006-4700-8527-6698e2d2b7fb)
#Win

![Ekran görüntüsü 2025-06-02 170432](https://github.com/user-attachments/assets/577b31cb-0b1c-4c4b-84c7-a35a9409d674)
![Ekran görüntüsü 2025-06-02 170501](https://github.com/user-attachments/assets/fd0c1c88-b6b7-407e-b23a-2bfbcfff28b9)
![Ekran görüntüsü 2025-06-02 170526](https://github.com/user-attachments/assets/50223d28-9458-4962-b636-ecb722b8ae5b)



This project is a Python-based application that detects the **English accent** from a given audio file. It provides two interfaces:

- A modern **web interface** using [Streamlit](https://streamlit.io/)
- A classic **desktop interface** using `Tkinter`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AuroraDuke/AuroraDuke-Accent-Detector-rem.git
cd AuroraDuke-Accent-Detector-rem
```

### 2. Create a Virtual Environment and Install Requirements

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

---

## 💻 Running the Application

### ➤ For the Streamlit Web Interface

```bash
streamlit run streamlit_accent_app.py
```

This will launch a web app in your browser, where you can upload `.wav` audio files and view the predicted accent along with a confidence score.

### ➤ For the Tkinter Desktop Interface

```bash
python accent-win.py
```

A GUI window will open, allowing you to select an audio file, analyze it, and optionally export the results to a CSV file.

---

## 🧠 Model Information

This project uses the [Jzuluaga/accent-id-commonaccent_xlsr-en-english](https://huggingface.co/Jzuluaga/accent-id-commonaccent_xlsr-en-english) model from Hugging Face. The model is based on the **Wav2Vec 2.0 XLSR** architecture and is fine-tuned for English accent recognition using the CommonVoice dataset.

### ✅ Recognized Accents

The model can classify the following English accents:

- `us`
- `england`
- `australia`
- `indian`
- `canada`
- `bermuda`
- `scotland`
- `african`
- `ireland`
- `newzealand`
- `wales`
- `malaysia`
- `philippines`
- `singapore`
- `hongkong`
- `southatlandtic`

It achieves high accuracy (up to 95%) in accent classification tasks. For technical insights, refer to the [CommonAccent paper](https://arxiv.org/abs/2305.18283).

---

## 🗂️ Project Structure

| File                    | Description                               |
|-------------------------|-------------------------------------------|
| `streamlit_accent_app.py` | Streamlit web app interface              |
| `accent-win.py`          | Tkinter-based desktop interface          |
| `accent_config.yaml`     | Configuration settings for model loading |
| `requirements.txt`       | Python dependencies                      |
| `model/`                 | Folder containing optional model assets  |

---

## 📌 Features

- Upload and classify `.wav` audio files
- Real-time accent prediction with confidence scores
- CSV export functionality (in Tkinter)
- Integrated audio playback
- Scrollable results (Streamlit)

---

## 📎 Notes

- Only `.wav` audio files are supported.
- The Hugging Face model is loaded directly at runtime—no retraining is required.
- Modify `accent_config.yaml` to update paths or model settings.

---

## 📬 Contact

For suggestions, issues, or contributions, feel free to reach out at [github.com/AuroraDuke](https://github.com/AuroraDuke).

---
