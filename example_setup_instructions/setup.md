# PyTorch Fundamentals Setup Instructions

To get started with the PyTorch Fundamentals section, please follow these steps to set up your learning environment.

## 1. Install Python

Ensure you have Python 3.8 or newer installed on your system. You can download it from the official Python website: [python.org](https://www.python.org/downloads/)

To check your Python version, open a terminal or command prompt and run:

```bash
python --version
```

## 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage your project dependencies.

1.  **Create a virtual environment:**
    ```bash
    python -m venv pytorch_env
    ```

2.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\pytorch_env\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source pytorch_env/bin/activate
        ```
    You should see `(pytorch_env)` prepended to your terminal prompt, indicating that the virtual environment is active.

## 3. Install PyTorch and Other Libraries

With your virtual environment activated, install PyTorch and other necessary libraries.

1.  **Install PyTorch:**
    Visit the official PyTorch website to get the most up-to-date installation command tailored to your system (e.g., CPU or GPU version). For a CPU-only installation, you can typically use:

    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    ```
    *If you have a compatible GPU and wish to utilize it, please refer to the PyTorch website for the appropriate CUDA installation command.*

2.  **Install other common libraries:**
    ```bash
    pip install numpy matplotlib jupyterlab
    ```
    `numpy` is essential for numerical operations, `matplotlib` for plotting, and `jupyterlab` for interactive notebook development.

## 4. Verify Installation

After installation, you can quickly verify that PyTorch is correctly installed.

1.  **Open a Python interpreter or JupyterLab:**
    ```bash
    jupyter lab
    ```
    (This will open JupyterLab in your web browser.)

2.  **Run the following Python code:**

    ```python
    import torch
    print(torch.__version__)
    print(torch.cuda.is_available()) # Should be False for CPU-only, True for GPU
    ```

If the PyTorch version is printed without errors and `torch.cuda.is_available()` returns `False` (for CPU) or `True` (for GPU), your environment is set up successfully!