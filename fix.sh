#!/bin/bash

# Move into your PX4-gazebo-models directory first
cd ~/Desktop/PX4-gazebo-models/models || { echo "Models directory not found!"; exit 1; }

echo "Flattening models..."

# For every model directory inside models/
for model in */ ; do
  cd "$model" || continue

  # Check if there is a folder named '1', '2', or '3', etc.
  for subfolder in [0-9]*/ ; do
    if [ -d "$subfolder" ]; then
      echo "Fixing model: $model ($subfolder)"
      mv "$subfolder"* . 2>/dev/null
      rmdir "$subfolder" 2>/dev/null
    fi
  done

  cd ..
done

echo "✅ All models flattened successfully!"
