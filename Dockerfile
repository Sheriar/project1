FROM python
WORKDIR /app
COPY requirements.txt .
EXPOSE 5000
RUN pip install -r requirements.txt
ENV SECRET_KEY="isdfjnglskjdfngjksdfnkjgnsdfg"
ENV DATABASE_URI="mysql+pymysql://root:Hello123@35.246.16.218/SFIA2"
ENTRYPOINT ["/usr/local/bin/python", "app.py"]
COPY . .

