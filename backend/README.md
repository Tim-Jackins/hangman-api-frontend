## User Actions

curl -X POST -H 'Content-Type: application/json' -d '{
  "username": "tim_jackins",
  "password": "12345678"
}' http://localhost:5000/register

curl -u tim_jackins:12345678 -i -X GET localhost:5000/login

curl -X DELETE -H 'Content-Type: application/json' -d '{
  "id": "1"
}' http://localhost:5000/users

## Game Actions

curl -X POST -H "Content-Type:application/json"\
  -H "x-access-tokens:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJhNzQzZGJlZC0xMzcxLTRjNWYtODdkYS02ZDVlOTVhNjJlNDgiLCJleHAiOjE1ODg2NTk2ODl9.2qU7LmguASvMbVaH06W5F5zT8X4bvhRkNxXkE2oD3yk" \
  -d '{
    "name": "New Game",
    "secret_word": "banana",
    "passphrase": "candy"
  }' http://localhost:5000/game

curl localhost:5000/games





docker run --name hangman-db \
  -p 5432:5432 \
  -e POSTGRES_DB=hangman \
  -e POSTGRES_PASSWORD=0NLIN3-ex4m \
  -d postgres
