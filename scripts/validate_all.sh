#!/bin/bash
# check-jsonschema les fichiers JSON
cd /home/martinfou/projects/la-minute-copilot

for f in presentations/*.json; do
  basename "$f"
  check-jsonschema --schemafile schema/la-minute-copilot.schema.json "$f" 2>&1 | tail -1
  echo ""
done
