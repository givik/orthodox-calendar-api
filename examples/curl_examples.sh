#!/bin/bash
# Orthodox Calendar API Example cURL Requests

BASE_URL="http://localhost:8000"

echo "1. Health Check:"
curl -s "${BASE_URL}/health" | jq .

echo -e "\n2. Today's Commemorations (Georgian):"
curl -s "${BASE_URL}/api/v1/today?lang=ka" | jq .

echo -e "\n3. Svetitskhovloba / Mtskhetoba (2026-10-14):"
curl -s "${BASE_URL}/api/v1/day?date=2026-10-14&lang=ka" | jq .

echo -e "\n4. Pascha and Movable Cycle (2026):"
curl -s "${BASE_URL}/api/v1/pascha/2026?lang=ka" | jq .

echo -e "\n5. Great Feasts of 2026:"
curl -s "${BASE_URL}/api/v1/feasts/2026?lang=ka" | jq .
