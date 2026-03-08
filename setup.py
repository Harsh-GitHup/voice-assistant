from setuptools import find_packages, setup

setup(
    name="voice_vision_assistant",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["main"],
    include_package_data=True,
    install_requires=[
        "fastapi==0.133.1",
        "uvicorn>=0.34.0",
        "openai>=1.60.0",
        "langchain-openai>=0.3.0",
        "langchain-community>=0.3.0",
        "chromadb>=0.6.0",
        "SpeechRecognition>=3.10.4",
        "pyttsx3>=2.90",
        "deepface>=0.0.92",
        "opencv-python-headless~=4.10.0",
        "python-dotenv>=1.0.1",
        "wikipedia>=1.4.0",
    ],
    entry_points={
        "console_scripts": [
            "assistant-start=main:main",
        ],
    },
)
