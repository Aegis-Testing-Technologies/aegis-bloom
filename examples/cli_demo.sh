#!/bin/bash
# AEGIS Bloom CLI Demo Script
#
# This script demonstrates the command-line interface for AEGIS Bloom.
# It shows how to build bloom filters and check for copyright compliance.

set -e

echo "🛡️ AEGIS Bloom CLI Demo"
echo "======================"
echo

# Create sample training data
echo "📁 Creating sample training dataset..."
mkdir -p demo_data/training_corpus
cat > demo_data/training_corpus/shakespeare.txt << 'EOF'
To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them.
EOF

cat > demo_data/training_corpus/cooking.txt << 'EOF'
The secret to perfect chocolate chip cookies is using brown butter.
For fluffy pancakes, don't overmix the batter - lumps are okay!
When making bread, let the dough rise slowly in a cool place.
EOF

cat > demo_data/training_corpus/science.txt << 'EOF'
The theory of relativity revolutionized our understanding of space and time.
Quantum mechanics describes the behavior of matter at the atomic scale.
Natural selection is the driving force behind biological evolution.
EOF

echo "✅ Created training corpus with 3 files"
echo

# Create test content to check
echo "📝 Creating test content..."
mkdir -p demo_data/test_content

cat > demo_data/test_content/original_recipe.txt << 'EOF'
My grandmother's secret apple pie recipe uses fresh cinnamon.
EOF

cat > demo_data/test_content/suspicious_text.txt << 'EOF'
The secret to perfect chocolate chip cookies is using brown butter and vanilla.
EOF

cat > demo_data/test_content/shakespeare_quote.txt << 'EOF'
To be, or not to be, that is the question.
EOF

echo "✅ Created test content with 3 files"
echo

# Build bloom filter
echo "🔨 Building bloom filter from training data..."
aegis bloom-build demo_data/training_corpus demo_data/training.bloom --verbose
echo

# Check test files
echo "🔍 Checking test content against bloom filter..."
echo

echo "1. Checking original recipe (should be NOT_PRESENT):"
aegis bloom-check demo_data/test_content/original_recipe.txt demo_data/training.bloom
echo

echo "2. Checking suspicious text (may be MAYBE_PRESENT):"
aegis bloom-check demo_data/test_content/suspicious_text.txt demo_data/training.bloom
echo

echo "3. Checking Shakespeare quote (should be MAYBE_PRESENT):"
aegis bloom-check demo_data/test_content/shakespeare_quote.txt demo_data/training.bloom
echo

# Batch check with JSON output
echo "📊 Running batch check with JSON output..."
aegis bloom-check demo_data/test_content/*.txt demo_data/training.bloom --output demo_data/results.json
echo

echo "📋 Results summary (from JSON):"
cat demo_data/results.json | python3 -m json.tool
echo

# Check bloom filter stats
echo "📈 Bloom filter statistics:"
echo "File size: $(du -h demo_data/training.bloom | cut -f1)"
echo "Content: $(ls -la demo_data/training.bloom)"
echo

echo "🎉 Demo complete!"
echo
echo "💡 Tips:"
echo "  - Use smaller chunk sizes for better precision on short texts"
echo "  - Adjust false positive rate based on your compliance requirements"
echo "  - MAYBE_PRESENT requires manual review, NOT_PRESENT is definitive"
echo
echo "🔗 For more examples, see: https://github.com/Aegis-Testing-Technologies/aegis-bloom/examples"

# Cleanup
echo "🧹 Cleaning up demo files..."
rm -rf demo_data/
echo "✅ Cleanup complete"
