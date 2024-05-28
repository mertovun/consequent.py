#!/bin/bash

# Function to process .gitignore and create a find command exclude pattern
generate_find_exclude() {
  exclude_patterns=()
  if [[ -f ".gitignore" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
      # Skip comments and empty lines
      [[ "$line" =~ ^#.*$ ]] && continue
      [[ -z "$line" ]] && continue
      # Handle directory patterns
      if [[ "$line" =~ /$ ]]; then
        exclude_patterns+=("-path ./${line%/} -prune -o")
      else
        exclude_patterns+=("-path ./$line -prune -o")
      fi
    done < .gitignore
  fi
  # Combine exclude patterns into a single string
  find_exclude=$(printf " %s" "${exclude_patterns[@]}")
}

# Generate the find exclude patterns from .gitignore
generate_find_exclude

# Create a temporary file to store the concatenated result
temp_file=$(mktemp)

# Find and concatenate all relevant files
eval "find . ${find_exclude} \( -name '*.py' -o -name '*.cpp' -o -name '*.h' \) -print" | while read -r file; do
  echo "# $(basename "$file")" >> "$temp_file"
  cat "$file" >> "$temp_file"
  echo -e "\n" >> "$temp_file"
done

# Copy the result to the clipboard
if command -v pbcopy &> /dev/null; then
  cat "$temp_file" | pbcopy
elif command -v xclip &> /dev/null; then
  cat "$temp_file" | xclip -selection clipboard
else
  echo "Neither pbcopy nor xclip is installed. Cannot copy to clipboard."
fi

# Clean up temporary file
rm "$temp_file"

echo "All code files concatenated and copied to clipboard."
