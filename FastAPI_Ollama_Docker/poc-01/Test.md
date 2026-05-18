# From Browser
http://0.0.0.0:8000/ask?question=why%20sky%20is%20blue?

# From CLI

curl -X GET http://0.0.0.0:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "why is sky is blue?"}'
