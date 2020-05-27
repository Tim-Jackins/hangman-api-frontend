docker run --name online-exam-db \
  -p 5432:5432 \
  -e POSTGRES_DB=online-exam \
  -e POSTGRES_PASSWORD=0NLIN3-ex4m \
  -d postgres
