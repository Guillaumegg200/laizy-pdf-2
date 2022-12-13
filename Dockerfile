from python:3.10.6
expose 8501
cmd mdkir -p /app
WORKDIR /app
copy requirements.txt ./requirements.txt
run pip install --upgrade pip
run pip install -r requirements.txt
copy . .
ENTRYPOINT ["streamlit", "run"]
CMD ["streamlit_app.py"]
