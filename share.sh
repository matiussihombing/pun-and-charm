#!/bin/bash
echo "--------------------------------------------------"
echo "🔮 Generating public link..."
echo "--------------------------------------------------"
# We use StrictHostKeyChecking=no to avoid the yes/no prompt for a first-time connection
ssh -o StrictHostKeyChecking=no -R 80:localhost:5000 localhost.run
